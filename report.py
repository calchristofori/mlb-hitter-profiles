"""Step 2 of the hitter report workflow: one model call that writes the report.

    .venv/bin/python report.py "Pete Crow-Armstrong"
    .venv/bin/python report.py "Pete Crow-Armstrong" --prompt v1 --effort high

Flow: system prompt (prompts/system_<version>.md with the method inserted)
      + data packet (data.py) -> Claude (streamed) -> reports/<player>_<time>.md
      -> interactive page with charts (html_report.py) -> docs/<player>.html (the website)

Every report is saved with a .json record of exactly what produced it (prompt
version, model, effort, the packet, token use and cost). The evals use that record.

Reuse: if a saved report was made from the same instructions, data and settings, it is
reused instead of calling Claude again (no cost). --fresh always writes a new one.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

import data
import html_report

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")  # ANTHROPIC_API_KEY

MODEL = "claude-opus-5-5"
PRICE_PER_MTOK = {"input": 4.00, "output": 20.00}  # Opus 5.5, $ per million tokens
MAX_TOKENS = 64000  # ceiling for thinking + report; a report uses far less


def build_system_prompt(version):
    """The system prompt file with the method in place of {{METHOD}} and, from v2 on,
    the metric glossary in place of {{GLOSSARY}}."""
    template = (HERE / "prompts" / f"system_{version}.md").read_text()
    if "{{METHOD}}" not in template:
        sys.exit(f"prompts/system_{version}.md has no {{{{METHOD}}}} placeholder.")
    method = (HERE / "hitter_evaluation.md").read_text().strip()
    # Open questions to the author ("> **[Your call ...") are notes, not instructions.
    method = "\n".join(l for l in method.splitlines() if not l.startswith("> **[Your call"))
    glossary = (HERE / "metrics.md").read_text().strip()
    return template.replace("{{METHOD}}", method).replace("{{GLOSSARY}}", glossary)


def build_user_message(player, packet):
    # Data first, the request last: the model reads the long material before the task.
    return (f"<data_packet>\n{packet}</data_packet>\n\n"
            f"Write the hitter report on {player}.")


def fingerprint(system, packet, model, effort):
    """Identifies everything that shapes a report: instructions, data, model and effort.
    The roster check date changes every day without changing the data, so it is left out."""
    packet = re.sub(r"as of \d{4}-\d{2}-\d{2}, ", "", packet)
    return hashlib.sha256("\n\0".join([system, packet, model, effort]).encode()).hexdigest()[:16]


def find_saved(slug, fp):
    """The newest saved report with this fingerprint, or None. Fingerprints are recomputed
    from the prompt and packet each record saved, so older records match too."""
    for path in sorted((HERE / "reports").glob(f"{slug}_*.json"), reverse=True):
        r = json.loads(path.read_text())
        saved = fingerprint(r["system_prompt"], r["packet"], r["model_requested"], r["effort"])
        if saved == fp and path.with_suffix(".md").exists():
            return path.with_suffix(".md")
    return None


def write_report(player, version="v8", effort="high", fresh=False):
    system = build_system_prompt(version)
    packet = data.get_hitter_data(player)
    full_name = packet.splitlines()[0].removeprefix("# Data packet: ").strip()
    slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
    fp = fingerprint(system, packet, MODEL, effort)

    saved = None if fresh else find_saved(slug, fp)
    if saved:
        print(saved.read_text())
        print(f"Reused {saved.relative_to(HERE)}: same instructions, data and settings, so no new "
              "call to Claude ($0). Use --fresh to write a new one.", file=sys.stderr)
        page = html_report.write(full_name, saved)
        print(f"Page: {page.relative_to(HERE)}", file=sys.stderr)
        return saved

    user = build_user_message(full_name, packet)
    print(f"Writing report on {full_name} — {MODEL}, effort {effort}, prompt {version}\n", file=sys.stderr)
    message, text, thinking, cost = generate(system, user, effort)
    usage = message.usage

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = HERE / "reports"
    out_dir.mkdir(exist_ok=True)
    md_path = out_dir / f"{slug}_{stamp}.md"
    md_path.write_text(text + "\n")
    record = make_record(full_name, version, fp, system, effort, message, cost, text, thinking, packet)
    md_path.with_suffix(".json").write_text(json.dumps(record, indent=2))

    print(f"\nSaved {md_path.relative_to(HERE)} (+ .json) · {usage.input_tokens:,} in / "
          f"{usage.output_tokens:,} out tokens · ${cost:.3f} · {record['report_words']} words",
          file=sys.stderr)

    # The page: charts and tables drawn by code from the database, with the report's text.
    page = html_report.write(full_name, md_path)
    print(f"Page: {page.relative_to(HERE)}", file=sys.stderr)
    return md_path


def generate(system, user, effort, echo=True):
    """The one call to Claude. Returns (message, report text, thinking summary, cost in $).
    echo=False keeps it quiet (the evals run several at once)."""
    client = anthropic.Anthropic()

    # Streaming: text is printed as it is generated. Thinking happens first (a
    # summary is kept for the record, not printed). fallbacks="default" retries on
    # Anthropic's recommended backup model if a safety classifier declines.
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        thinking={"type": "adaptive", "display": "summarized"},
        output_config={"effort": effort},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        for event in stream:
            if not echo:
                continue
            if event.type == "content_block_start" and event.content_block.type == "thinking":
                print("[thinking…]\n", file=sys.stderr, flush=True)
            elif event.type == "content_block_delta" and event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        message = stream.get_final_message()
    if echo:
        print()

    if message.stop_reason == "refusal":
        raise RuntimeError(f"The model declined: {message.stop_details}")
    if message.stop_reason == "max_tokens":
        print("Warning: hit max_tokens; the report is cut off.", file=sys.stderr)

    text = "".join(b.text for b in message.content if b.type == "text").strip()
    thinking = "\n\n".join(b.thinking for b in message.content if b.type == "thinking" and b.thinking)
    usage = message.usage
    cost = (usage.input_tokens * PRICE_PER_MTOK["input"] + usage.output_tokens * PRICE_PER_MTOK["output"]) / 1e6
    return message, text, thinking, cost


def make_record(full_name, version, fp, system, effort, message, cost, text, thinking, packet):
    """The .json record of exactly what produced a report."""
    usage = message.usage
    return {
        "player": full_name,
        "created": datetime.now().isoformat(timespec="seconds"),
        "prompt_version": version,
        "fingerprint": fp,
        "system_prompt_sha256": hashlib.sha256(system.encode()).hexdigest()[:12],
        "system_prompt": system,  # the assembled prompt, method and glossary included
        "model_requested": MODEL,
        "model_used": message.model,  # differs only if the fallback ran
        "effort": effort,
        "stop_reason": message.stop_reason,
        "message_id": message.id,
        "usage": {"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens},
        "cost_usd": round(cost, 4),
        "report_words": len(text.split()),
        "thinking_summary": thinking,
        "packet": packet,
    }


def main():
    p = argparse.ArgumentParser(description="Write a hitter report with Claude.")
    p.add_argument("player")
    p.add_argument("--prompt", default="v8", help="system prompt version (prompts/system_<v>.md)")
    p.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--fresh", action="store_true", help="write a new report even if a matching one is saved")
    args = p.parse_args()
    try:
        write_report(args.player, args.prompt, args.effort, args.fresh)
    except (ValueError, RuntimeError) as e:  # name not found / ambiguous, or the model declined
        sys.exit(str(e))


if __name__ == "__main__":
    main()
