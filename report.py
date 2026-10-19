"""Step 2 of the hitter report workflow: one model call that writes the report.

    .venv/bin/python report.py "Pete Crow-Armstrong"
    .venv/bin/python report.py "Pete Crow-Armstrong" --prompt v1 --effort high

Flow: system prompt (prompts/system_<version>.md with the method inserted)
      + data packet (data.py) -> Claude (streamed) -> reports/<player>_<time>.md

Every report is saved with a .json record of exactly what produced it (prompt
version, model, effort, the packet, token use and cost). The evals use that record.
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
    glossary = (HERE / "metrics.md").read_text().strip()
    return template.replace("{{METHOD}}", method).replace("{{GLOSSARY}}", glossary)


def build_user_message(player, packet):
    # Data first, the request last: the model reads the long material before the task.
    return (f"<data_packet>\n{packet}</data_packet>\n\n"
            f"Write the hitter report on {player}.")


def write_report(player, version="v2", effort="high"):
    system = build_system_prompt(version)
    packet = data.get_hitter_data(player)
    full_name = packet.splitlines()[0].removeprefix("# Data packet: ").strip()
    user = build_user_message(full_name, packet)

    client = anthropic.Anthropic()
    print(f"Writing report on {full_name} — {MODEL}, effort {effort}, prompt {version}\n", file=sys.stderr)

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
            if event.type == "content_block_start" and event.content_block.type == "thinking":
                print("[thinking…]\n", file=sys.stderr, flush=True)
            elif event.type == "content_block_delta" and event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        message = stream.get_final_message()
    print()

    if message.stop_reason == "refusal":
        sys.exit(f"The model declined: {message.stop_details}")
    if message.stop_reason == "max_tokens":
        print("Warning: hit max_tokens; the report is cut off.", file=sys.stderr)

    text = "".join(b.text for b in message.content if b.type == "text").strip()
    thinking = "\n\n".join(b.thinking for b in message.content if b.type == "thinking" and b.thinking)
    usage = message.usage
    cost = (usage.input_tokens * PRICE_PER_MTOK["input"] + usage.output_tokens * PRICE_PER_MTOK["output"]) / 1e6

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")
    out_dir = HERE / "reports"
    out_dir.mkdir(exist_ok=True)
    md_path = out_dir / f"{slug}_{stamp}.md"
    md_path.write_text(text + "\n")
    record = {
        "player": full_name,
        "created": datetime.now().isoformat(timespec="seconds"),
        "prompt_version": version,
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
    md_path.with_suffix(".json").write_text(json.dumps(record, indent=2))

    print(f"\nSaved {md_path.relative_to(HERE)} (+ .json) · {usage.input_tokens:,} in / "
          f"{usage.output_tokens:,} out tokens · ${cost:.3f} · {record['report_words']} words",
          file=sys.stderr)
    return md_path


def main():
    p = argparse.ArgumentParser(description="Write a hitter report with Claude.")
    p.add_argument("player")
    p.add_argument("--prompt", default="v2", help="system prompt version (prompts/system_<v>.md)")
    p.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    args = p.parse_args()
    try:
        write_report(args.player, args.prompt, args.effort)
    except ValueError as e:  # name not found / ambiguous
        sys.exit(str(e))


if __name__ == "__main__":
    main()
