"""Turns the lab agent's answer into a report and rejects quotes that are not on screen.

Usage: report.py <tester.json> <screens.log> <title> <scenario> <tester model>
Prints the report as Markdown. Exit code 0 = pass, 1 = fail, 2 = no usable answer.
"""
import json
import re
import sys
from datetime import datetime

raw_path, screens_path, title, scenario, model = sys.argv[1:6]


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def load_answer(path):
    try:
        data = json.load(open(path))
    except Exception as err:  # the lab agent crashed or printed no JSON
        return None, f"could not read the lab agent's output: {err}"
    answer = data.get("structured_output")
    if answer is None:
        text = re.sub(r"^```(?:json)?|```$", "", str(data.get("result", "")).strip(), flags=re.M).strip()
        try:
            answer = json.loads(text)
        except Exception:
            return None, f"the lab agent returned no structured answer: {text[:300]}"
    return answer, data


answer, meta = load_answer(raw_path)
print(f"# Lab report: {title}\n")
print(f"- When: {datetime.now():%Y-%m-%d %H:%M}")
print(f"- Lab agent model: {model}")

if answer is None:
    print(f"\n**Verdict: NO RESULT.** {meta}")
    sys.exit(2)

if isinstance(meta, dict) and meta.get("total_cost_usd") is not None:
    print(f"- Lab agent usage: ${meta['total_cost_usd']:.3f} at API prices, {meta.get('num_turns', '?')} turns")

screen = norm(open(screens_path, errors="replace").read())
failed = False
rows = []
for i, step in enumerate(answer.get("steps", []), 1):
    quote = step.get("quote", "")
    on_screen = bool(norm(quote)) and norm(quote) in screen
    ok = bool(step.get("pass")) and on_screen
    note = ""
    if step.get("pass") and not norm(quote):
        note = "Rejected: no quote from the screen."
    elif step.get("pass") and not on_screen:
        note = "Rejected: this quote is not in anything the lab read from a screen."
    failed = failed or not ok
    rows.append((i, ok, step, note))

if not rows:
    failed = True
verdict = "FAIL" if failed or answer.get("verdict") != "pass" else "PASS"
print(f"\n**Verdict: {verdict}**\n")

for i, ok, step, note in rows:
    print(f"## Step {i}: {'pass' if ok else 'FAIL'}\n")
    print(f"- I tried: {step.get('tried', '')}")
    print(f"- Expected: {step.get('expected', '')}")
    print(f"- Got: {step.get('got', '')}")
    print(f"- Screen quote: `{step.get('quote', '')}`")
    if note:
        print(f"- {note}")
    print()

if answer.get("lost"):
    print(f"## Where the lab agent got lost\n\n{answer['lost']}\n")

print("## The check as written\n")
print("```\n" + scenario.strip() + "\n```")
sys.exit(0 if verdict == "PASS" else 1)
