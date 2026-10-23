"""The eval: are the reports good, and did a change make them better or worse?

    .venv/bin/python evals/run_eval.py                 # full run: 8 hitters x 3 reports (~$5)
    .venv/bin/python evals/run_eval.py --runs 1        # one report per hitter (~$2)
    .venv/bin/python evals/run_eval.py --hitters "Kyle Schwarber"   # just one hitter
    .venv/bin/python evals/run_eval.py --prompt v10    # score another prompt version

The test hitters and the answer key are read from evals/eval_plan.md, so editing that
file changes the eval. Each report is scored two ways:
  A. code checks: free, automatic, pass/fail (numbers traceable, length, sections, wording, stat walk)
  B. an AI grader: one call per report, pass/fail with a one-line reason per check

Eval reports are written to evals/runs/<time>/ only. They never reuse a saved report,
never go into reports/ and never touch the website (docs/).
"""

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import anthropic

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import data    # noqa: E402
import report  # noqa: E402

PLAN = HERE / "eval_plan.md"
RUNS = HERE / "runs"
GRADER_EFFORT = "medium"
PARALLEL = 4  # reports written at the same time

WORDS = (600, 800)  # agreed 2026-10-22: ~750 is the right length
MAX_NUMBERS = 25    # numbers cited, title and Sample notes not counted; the prompt asks for about 20
MAX_METRIC_LED = 0.15  # provisional, 2026-10-23: v8 reports ran 9-37%; share of sentences whose subject is a metric ("His EV90 was..."): a stat walk

# Sentence openings that make a metric the subject. Built from the glossary's metric names plus
# the plain-English names reports use for them.
GLOSSARY_METRICS = [m for line in re.findall(r"^- \*\*([^*]+)\*\*", (HERE.parent / "metrics.md").read_text(), re.M)
                    for m in line.split(", ")
                    if m not in {"PA", "BBE", "Pitches", "Qualified", "Qualified avg", "Rank", "Percentile", "Age",
                                 "Platoon splits", "Season-over-season change", "Pitch groups",
                                 "Two ways of counting.", "Share", "PA ending", "AVG", "OBP", "SLG"}]
PLAIN_METRICS = ["walk rate", "strikeout rate", "chase rate", "whiff rate", "swing-and-miss rate", "exit velocity",
                 "launch angle", "launch spread", "launch median", "in-zone swing rate", "popup rate", "barrel rate",
                 "ground-ball rate", "hard-hit rate", "sweet-spot rate", "sprint speed", "expected"]
METRIC_LED = re.compile(r"^(?:his |the )?(?:" + "|".join(re.escape(m) for m in GLOSSARY_METRICS + PLAIN_METRICS)
                        + r")(?![\w])", re.I)

# Wording the system prompt rules out. (pattern, what it catches)
BANNED = [
    (r"swing[- ]decision|decision score|decision quality", '"swing decision(s)"'),
    (r"\bforce\b", '"force" instead of exit velocity'),
    (r"Interpretation:", '"Interpretation:" label'),
    (r"^\s*[-*•] ", "bullet list"),
    (r"20[-–]80|\bgrades?\b", "scouting grades"),
    # ranks are described in words from v10 on; "90th-percentile" (EV90's definition) is not matched
    (r"\b\d+(?:st|nd|rd|th) (?:of \d+|percentile|among|in the league)"
     r"|\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)"
     r"(?: in the league| among|-highest|-lowest|-best|-worst)"
     r"|\branked (?:\d+(?:st|nd|rd|th)|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b",
     "rank cited as a number"),
]
# Signs the report is talking about its own instructions instead of the hitter.
META = [
    (r"\bmethod\b", '"method"'),
    (r"\bthresholds?\b", '"threshold"'),
    (r"\bpacket\b", '"packet"'),
]
NUMBER = re.compile(r"(?<![\w.])[-+]?(?:\d+(?:\.\d+)?|\.\d+)%?")


# ---------- the test set, read from eval_plan.md ----------

def load_plan():
    """[(name, type it tests, answer key)] from the tables and list in eval_plan.md."""
    text = PLAN.read_text()
    hitters = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", text, re.M)
    keys = dict(re.findall(r"^\d+\.\s*\*\*([^*]+)\*\*:\s*(.+)$", text, re.M))
    plan = []
    for name, kind in hitters:
        key = next((v for k, v in keys.items() if k.strip() in name), None)
        if key is None:
            sys.exit(f"eval_plan.md: no answer key for {name} (looked for **{name.split()[-1]}**: ...)")
        plan.append((name, kind, key.strip()))
    return plan


# ---------- A. code checks ----------

def expected_sections(system):
    """The section headings the prompt asks for, in order, read from its output format."""
    return re.findall(r"`## (.+?)`", system.split("<output_format>")[-1])


def sentences(text):
    """Prose sentences of the report body, Sample notes left out."""
    body = re.sub(r"^## Sample notes.*", "", body_of(text), flags=re.M | re.S)
    prose = " ".join(l for l in body.splitlines() if l.strip() and not l.startswith("#"))
    return [s for s in re.split(r"(?<=[.!?])\s+", prose) if s]


def body_of(text):
    """The report without its title line (the title holds the name, age and position only)."""
    return text.split("\n", 1)[1] if "\n" in text else text


def code_checks(text, packet, sections):
    """{check: (passed, detail)}"""
    out = {}

    # Signs are dropped on purpose ("-10.1 pts" in the packet is "fell 10.1 pts" in prose), and
    # EV90's own definition ("90th-percentile exit velocity") isn't a stat.
    unsigned = lambda nums: {n.lstrip("+-") for n in nums}
    packet_numbers = unsigned(NUMBER.findall(packet))
    prose = re.sub(r"90th[- ]percentile", "", text)
    missing = sorted(unsigned(NUMBER.findall(prose)) - packet_numbers)
    out["numbers_traceable"] = (not missing, "not in packet: " + ", ".join(missing) if missing else "")

    cited = NUMBER.findall(re.sub(r"90th[- ]percentile", "", re.sub(r"^## Sample notes.*", "", body_of(text), flags=re.M | re.S)))
    out["number_count"] = (len(cited) <= MAX_NUMBERS, f"{len(cited)} numbers")

    words = len(text.split())
    out["length"] = (WORDS[0] <= words <= WORDS[1], f"{words} words")

    found = re.findall(r"^##\s+(.+?)\s*$", text, re.M)
    out["sections"] = (found == sections, "" if found == sections else "found: " + " / ".join(found))

    led = [s for s in sentences(text) if METRIC_LED.match(s)]
    share = len(led) / max(len(sentences(text)), 1)
    out["metric_led"] = (share <= MAX_METRIC_LED, f"{len(led)}/{len(sentences(text))} sentences open with a metric")

    body = body_of(text)
    hits = [label for pat, label in BANNED if re.search(pat, body, re.M | re.I)]
    out["banned_wording"] = (not hits, ", ".join(hits))

    hits = [label for pat, label in META if re.search(pat, body, re.I)]
    out["no_method_talk"] = (not hits, ", ".join(hits))

    unlabeled = []
    for metric in ["xwOBA", "xBA", "xSLG"]:
        m = re.search(rf"\b{metric}\b", body)
        if m and "house model" not in body[m.start():m.start() + 80]:
            unlabeled.append(metric)
    out["house_model_label"] = (not unlabeled, "first use unlabeled: " + ", ".join(unlabeled) if unlabeled else "")
    return out


# ---------- B. the AI grader ----------

GRADER_CHECKS = {
    "top_line_right": "The Top line names the same hitter type and value driver as the answer key.",
    "claims_supported": "Every factual claim is supported by the data packet. Nothing comes from outside "
                        "knowledge (contracts, injuries, awards, news, stats not in the packet).",
    "sample_sizes": "Sample sizes are handled: a season or split under 100 PA gets no read; 100-200 PA is "
                    "flagged as tentative; pitch-group results with under 50 PA ending get no read. Pass if "
                    "no small sample is relevant and none is misused.",
    "platoon_by_share": "The platoon discussion (Platoon profile, or How he's used) judges his role by his share of PA against lefties compared with "
                        "same-handed hitters, not by the raw PA count.",
    "combinations_read": "Metrics are read together correctly (e.g. low chase with high whiff is not good "
                         "discipline; high EV90 with low xISO is power that isn't playing). Fail on any misread.",
    "no_filler": "No metric is singled out just to say it is average or unremarkable. One sentence saying a whole "
                 "area is unremarkable is fine; listing several average metrics by name is filler.",
    "change_over_time": "When two or more slowing-bat signals move together across seasons (EV90 down, Whiff% "
                        "up, Pulled Air% down), the report flags it. Pass if no such pattern is in the data.",
    "reads_like_profile": "It reads like a scout's profile, not a stat list: each sentence makes a point about the "
                          "hitter and uses at most one or two numbers as evidence. Fail if sentences string several "
                          "stats together or walk through numbers one after another.",
    "synthesis_connects": "The report connects findings into how he drives value (in the Synthesis, or for a "
                          "report without one, in How he does damage), showing how one skill explains another, "
                          "rather than repeating numbers and sentences from other sections.",
}

GRADER_SYSTEM = """You grade hitter profiles written by another model. You are strict and specific.

You get the data packet the writer was given, an answer key written by a baseball analyst, and the report.
For each check, decide pass or fail and give a one-sentence reason that quotes or points to the exact
words in the report. Judge only what each check asks. Do not reward or penalize style beyond the checks.

The checks:
""" + "\n".join(f"- {k}: {v}" for k, v in GRADER_CHECKS.items())

GRADER_SCHEMA = {
    "type": "object",
    "properties": {k: {"type": "object",
                       "properties": {"pass": {"type": "boolean"}, "reason": {"type": "string"}},
                       "required": ["pass", "reason"], "additionalProperties": False}
                   for k in GRADER_CHECKS},
    "required": list(GRADER_CHECKS),
    "additionalProperties": False,
}


def grade(text, packet, answer_key):
    """{check: (passed, reason)}, and the cost of the call."""
    user = (f"<data_packet>\n{packet}</data_packet>\n\n<answer_key>\n{answer_key}\n</answer_key>\n\n"
            f"<report>\n{text}\n</report>\n\nGrade the report on every check.")
    client = anthropic.Anthropic()
    with client.messages.stream(
        model=report.MODEL,
        max_tokens=16000,
        system=GRADER_SYSTEM,
        messages=[{"role": "user", "content": user}],
        thinking={"type": "adaptive"},
        output_config={"effort": GRADER_EFFORT,
                       "format": {"type": "json_schema", "schema": GRADER_SCHEMA}},
    ) as stream:
        message = stream.get_final_message()
    result = json.loads(next(b.text for b in message.content if b.type == "text"))
    u = message.usage
    cost = (u.input_tokens * report.PRICE_PER_MTOK["input"] + u.output_tokens * report.PRICE_PER_MTOK["output"]) / 1e6
    return {k: (v["pass"], v["reason"]) for k, v in result.items()}, cost


# ---------- one report, end to end ----------

def run_one(job):
    """Write, check and grade one report. Each step is saved as it finishes, so a run that
    stops partway (out of credit, network) can be resumed without paying twice."""
    name, kind, key, i, system, version, effort, out_dir = job
    try:
        packet = data.get_hitter_data(name)
        full_name = packet.splitlines()[0].removeprefix("# Data packet: ").strip()
        slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
        path = out_dir / f"{slug}_{i}.md"
        cost_file, result_file = path.with_suffix(".cost"), path.with_suffix(".json")
        if result_file.exists():
            return json.loads(result_file.read_text())

        if path.exists():  # written on an earlier attempt; only the grading is left
            text = path.read_text().strip()
            cost = float(cost_file.read_text()) if cost_file.exists() else 0.0
        else:
            message, text, thinking, cost = report.generate(
                system, report.build_user_message(full_name, packet), effort, echo=False)
            path.write_text(text + "\n")
            cost_file.write_text(f"{cost:.4f}")

        checks = code_checks(text, packet, expected_sections(system))
        graded, grade_cost = grade(text, packet, key)
        result = {"hitter": full_name, "type": kind, "run": i, "file": path.name,
                  "words": len(text.split()), "report_cost": round(cost, 4), "grade_cost": round(grade_cost, 4),
                  "code": {k: list(v) for k, v in checks.items()},
                  "grader": {k: list(v) for k, v in graded.items()}}
        result_file.write_text(json.dumps(result, indent=2))
        print(f"  done: {full_name} #{i}  (${cost + grade_cost:.2f})", file=sys.stderr, flush=True)
        return result
    except Exception as e:  # one failure shouldn't sink the run; it is listed at the end
        print(f"  FAILED: {name} #{i}: {e}", file=sys.stderr, flush=True)
        return {"hitter": name, "run": i, "error": str(e)}


# ---------- the scorecard ----------

def pct(results, group, check):
    vals = [r[group][check][0] for r in results]
    return f"{sum(vals)}/{len(vals)}"


def scorecard(results, version, effort, runs):
    hitters = list(dict.fromkeys(r["hitter"] for r in results))
    checks = [("code", c) for c in results[0]["code"]] + [("grader", c) for c in GRADER_CHECKS]
    total = sum(r["report_cost"] + r["grade_cost"] for r in results)
    passed = sum(r[g][c][0] for r in results for g, c in checks)
    lines = [f"# Eval scorecard: prompt {version}, effort {effort}",
             "",
             f"{datetime.now():%Y-%m-%d %H:%M} · {len(hitters)} hitters × {runs} runs = {len(results)} reports · "
             f"cost ${total:.2f}",
             "",
             f"**Overall: {passed}/{len(results) * len(checks)} checks passed "
             f"({100 * passed / (len(results) * len(checks)):.0f}%)**",
             "",
             "## By check", "", "| Check | Kind | Passed |", "|---|---|---|"]
    lines += [f"| {c} | {'code' if g == 'code' else 'AI grader'} | {pct(results, g, c)} |" for g, c in checks]

    lines += ["", "## By hitter", "",
              "| Hitter | Tests | " + " | ".join(c for _, c in checks) + " |",
              "|---|---|" + "---|" * len(checks)]
    for h in hitters:
        rs = [r for r in results if r["hitter"] == h]
        lines.append(f"| {h} | {rs[0]['type']} | " + " | ".join(pct(rs, g, c) for g, c in checks) + " |")

    lines += ["", "## Every failure, with the reason", ""]
    for r in results:
        fails = [(c, r[g][c][1]) for g, c in checks if not r[g][c][0]]
        if fails:
            lines.append(f"**{r['hitter']} #{r['run']}** ({r['file']}, {r['words']} words)")
            lines += [f"- {c}: {why}" for c, why in fails]
            lines.append("")
    return "\n".join(lines) + "\n"


def my_scores_template(results):
    """A sheet for the gold standard: my own score on one report per hitter."""
    seen, lines = set(), ["# My scores", "",
                          "One report per hitter. Read it, then fill in: would I publish this? (1-5) and why.",
                          "Compare with the AI grader's verdict in scorecard.md. If we disagree, fix the grader.", ""]
    for r in results:
        if r["hitter"] not in seen:
            seen.add(r["hitter"])
            lines += [f"## {r['hitter']} ({r['file']})", "Score (1-5): ", "Why: ", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Score hitter reports against the eval plan.")
    p.add_argument("--runs", type=int, default=3, help="reports per hitter")
    p.add_argument("--hitters", nargs="*", help="only these hitters (default: all in eval_plan.md)")
    p.add_argument("--prompt", default="v8")
    p.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--resume", metavar="RUN_DIR", help="finish a run that stopped partway, e.g. evals/runs/20261022_160114_v5")
    args = p.parse_args()

    plan = load_plan()
    if args.hitters:
        plan = [h for h in plan if any(x.lower() in h[0].lower() for x in args.hitters)]
    system = report.build_system_prompt(args.prompt)
    if args.resume:
        out_dir = Path(args.resume).resolve()
        if not out_dir.is_dir():
            sys.exit(f"No run folder at {args.resume}")
    else:
        out_dir = RUNS / f"{datetime.now():%Y%m%d_%H%M%S}_{args.prompt}"
        out_dir.mkdir(parents=True)

    jobs = [(n, k, key, i, system, args.prompt, args.effort, out_dir)
            for n, k, key in plan for i in range(1, args.runs + 1)]
    print(f"Eval: {len(plan)} hitters × {args.runs} runs = {len(jobs)} reports, prompt {args.prompt}. "
          f"Writing to {out_dir.relative_to(HERE.parent)}/", file=sys.stderr)
    with ThreadPoolExecutor(PARALLEL) as pool:
        results = list(pool.map(run_one, jobs))

    failed = [r for r in results if "error" in r]
    results = [r for r in results if "error" not in r]
    if failed:
        print(f"\n{len(failed)} of {len(jobs)} reports failed (first error: {failed[0]['error'][:200]}).\n"
              f"Finish them with: .venv/bin/python evals/run_eval.py --resume {out_dir.relative_to(HERE.parent)}",
              file=sys.stderr)
        if not results:
            sys.exit(1)

    (out_dir / "results.json").write_text(json.dumps(
        {"prompt": args.prompt, "effort": args.effort, "system_prompt": system,
         "answer_keys": {n: key for n, _, key in plan}, "results": results}, indent=2))
    card = scorecard(results, args.prompt, args.effort, args.runs)
    (out_dir / "scorecard.md").write_text(card)
    (out_dir / "my_scores.md").write_text(my_scores_template(results))
    print(card)
    print(f"Saved {out_dir.relative_to(HERE.parent)}/scorecard.md", file=sys.stderr)


if __name__ == "__main__":
    main()
