#!/usr/bin/env python3
"""Summarise an executed Markdown test plan into a Markdown test report.

Usage: summarise_plan.py --input plan.md [--output report.md] [--html report.html]
       [--title T] [--context C] [--json]
Standard library only. Layout comes from ../templates/report.md.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path
from string import Template

FIXED_COLUMNS = {"#", "test case", "expected", "notes", "source", "severity"}
CLOSURE_ROWS = {
    "time-boxed exploratory session",
    "element and layout check",
    "accessibility check",
    "localisation check",
}
UNCONFIRMED = "not stated: confirm with owner"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "report.md"


def normalise(value):
    v = value.strip().lower()
    if v == "":
        return "blank"
    if v in {"n/a", "na", "-", "—"}:
        return "na"
    for word in ("pass", "fail", "blocked"):
        if v == word or v.startswith(word + " "):
            return word
    return "other"


def row_status(results):
    values = list(results.values())
    if "fail" in values:
        return "fail"
    if "blocked" in values:
        return "blocked"
    if "pass" in values:
        return "pass"
    if values and all(v == "na" for v in values):
        return "out of scope"
    return "not run"


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse(text):
    title, section, header, rows, closure = "", "(no section)", None, [], 0
    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            section, header = line[3:].strip(), None
        elif not line.strip().startswith("|"):
            header = None
        elif header is None:
            cells = [c.lower() for c in split_row(line)]
            header = cells if "test case" in cells else []
        elif not header or re.fullmatch(r"[\s|:-]+", line):
            continue
        else:
            cells = split_row(line) + [""] * len(header)
            record = dict(zip(header, cells))
            name = record["test case"]
            if name.lower() in CLOSURE_ROWS:
                closure += 1
                continue
            envs = [h for h in header if h not in FIXED_COLUMNS]
            results = {e: normalise(record[e]) for e in envs}
            rows.append({
                "section": section,
                "id": record.get("#", ""),
                "test": name,
                "notes": record.get("notes", ""),
                "unconfirmed": record.get("expected", "").lower().startswith(UNCONFIRMED),
                "results": results,
                "raw": {e: record[e] for e in envs},
                "status": row_status(results),
            })
    if not rows:
        sys.exit("No table with a 'Test case' column found. Is this a Markdown test plan?")
    return title, rows, closure


def metrics(rows, closure):
    statuses = ["pass", "fail", "blocked", "out of scope", "not run"]
    count = {s: sum(r["status"] == s for r in rows) for s in statuses}
    executed = count["pass"] + count["fail"]
    envs = list(rows[0]["results"])
    by_env = {e: {v: sum(r["results"].get(e) == v for r in rows)
                  for v in ("pass", "fail", "blocked", "na", "blank", "other")} for e in envs}
    sections = {}
    for r in rows:
        sections.setdefault(r["section"], {s: 0 for s in statuses})[r["status"]] += 1
    if count["fail"]:
        verdict = "Failures present"
    elif count["blocked"] or count["not run"]:
        verdict = "In progress"
    else:
        verdict = "All passed"
    return {
        "total": len(rows), "closure_rows": closure, "count": count, "executed": executed,
        "pass_rate": f"{round(count['pass'] / executed * 100)}%" if executed else "n/a (nothing executed)",
        "verdict": verdict, "by_env": by_env, "sections": sections,
        "unconfirmed": sum(r["unconfirmed"] for r in rows),
        "unrecognised": [f"#{r['id']} {e}: `{v}`" for r in rows for e, v in r["raw"].items()
                         if r["results"][e] == "other"],
    }


def listing(rows, status):
    hits = [f"- #{r['id']} {r['test']} ({r['section']})" + (f": {r['notes']}" if r["notes"] else "")
            for r in rows if r["status"] == status]
    return "\n".join(hits) or "None."


def render(title, context, m, rows):
    c = m["count"]
    section_rows = "\n".join(
        f"| {name} | {sum(s.values())} | {s['pass']} | {s['fail']} | {s['blocked']} | {s['out of scope']} | {s['not run']} |"
        for name, s in m["sections"].items())
    env_rows = "\n".join(
        f"| {e} | {v['pass']} | {v['fail']} | {v['blocked']} | {v['na']} | {v['blank']} |"
        for e, v in m["by_env"].items())
    summary = (f"{c['pass']}/{m['executed']} executed cases passed across {len(m['sections'])} areas; "
               f"{c['fail']} failed, {c['blocked']} blocked, {c['not run']} not run. Verdict: {m['verdict']}.")
    return Template(TEMPLATE.read_text().split("<!-- report -->", 1)[1].strip()).substitute(
        title=title, context=context or "none given", verdict=m["verdict"], total=m["total"],
        closure=m["closure_rows"], executed=m["executed"], pass_rate=m["pass_rate"],
        passed=c["pass"], failed=c["fail"], blocked=c["blocked"], oos=c["out of scope"],
        not_run=c["not run"], unconfirmed=m["unconfirmed"], section_rows=section_rows,
        env_rows=env_rows, failures=listing(rows, "fail"), blocked_list=listing(rows, "blocked"),
        oos_list=listing(rows, "out of scope"),
        unrecognised="\n".join(f"- {u}" for u in m["unrecognised"]) or "None.", summary=summary,
    ) + "\n"


HTML_CSS = """
:root{--ink:#1a1a1a;--ink2:#55585f;--ink3:#8a8f98;--line:#e6e8eb;--panel:#f7f8f9;--green:#1a7f4b;
--green-bg:#e8f5ee;--blue:#1f6feb;--amber:#9a6a00;--amber-bg:#fdf3e2;--red:#b3261e;--red-bg:#fbeae8;}
*{box-sizing:border-box}body{margin:0;background:#eef0f2;color:var(--ink);padding:32px 16px;
font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.page{max-width:960px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:12px;padding:32px}
h1{font-size:22px;margin:0}h2{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);margin:28px 0 12px}
.head{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.tiny{font-size:12px;color:var(--ink3);margin-top:6px}
.badge{font-weight:600;font-size:12px;padding:4px 10px;border-radius:999px}
.green{color:var(--green)}.red{color:var(--red)}.amber{color:var(--amber)}
.badge.green{background:var(--green-bg)}.badge.red{background:var(--red-bg)}.badge.amber{background:var(--amber-bg)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-top:20px}
.kpi{border:1px solid var(--line);border-radius:10px;padding:14px}.kpi b{display:block;font-size:26px}
.kpi span{font-size:12px;color:var(--ink3)}
.cols{display:grid;grid-template-columns:3fr 2fr;gap:28px}@media(max-width:720px){.cols{grid-template-columns:1fr}}
.bar{display:grid;grid-template-columns:minmax(110px,200px) 1fr 40px;align-items:center;gap:10px;margin-bottom:7px}
.bar .n{font-size:13px;color:var(--ink2);text-align:right}.track{background:var(--panel);border-radius:5px;height:18px}
.fill{height:100%;border-radius:5px;background:var(--blue);opacity:.85}.fill.ok{background:var(--green)}
.v{font-size:12px;font-weight:600;color:var(--ink2)}
.callouts{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:720px){.callouts{grid-template-columns:1fr}}
.callout{border-radius:10px;padding:12px 14px;border:1px solid var(--line);background:var(--panel)}
.callout.red{background:var(--red-bg)}.callout.amber{background:var(--amber-bg)}.callout.green{background:var(--green-bg)}
.callout b{display:block;font-size:13px;margin-bottom:4px}.callout ul{margin:0;padding-left:18px;font-size:13px;color:var(--ink2)}
.callout p{margin:0;font-size:13px;color:var(--ink2)}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);font-size:13px}
th{color:var(--ink3);font-size:12px;text-transform:uppercase}td.n,th.n{text-align:right}
@media print{body{background:#fff;padding:0}.page{border:0}}
"""


def render_html(title, context, m, rows):
    c = m["count"]

    def e(text):  # escape, and drop Markdown emphasis and code markers from plan text
        return html.escape(re.sub(r"\*\*|`", "", str(text)))

    tone = {"Failures present": "red", "In progress": "amber"}.get(m["verdict"], "green")

    def tile(value, label, cls=""):
        return f'<div class="kpi"><b class="{cls}">{e(str(value))}</b><span>{e(label)}</span></div>'

    tiles = [tile(m["pass_rate"], "Pass rate", tone), tile(m["executed"], "Executed (passed + failed)"),
             tile(c["fail"], "Failed", "red" if c["fail"] else "green")]
    if c["blocked"]:
        tiles.append(tile(c["blocked"], "Blocked", "amber"))
    if c["not run"]:
        tiles.append(tile(c["not run"], "Not run", "amber"))
    if m["unconfirmed"]:
        tiles.append(tile(m["unconfirmed"], "Expected result unconfirmed", "amber"))
    tiles.append(tile(len(m["sections"]), "Areas"))

    def bars(pairs, cls=""):
        top = max((n for _, n in pairs), default=1) or 1
        return "".join(
            f'<div class="bar"><div class="n">{e(name)}</div><div class="track">'
            f'<div class="fill {cls}" style="width:{n / top * 100:.1f}%"></div></div><div class="v">{n}</div></div>'
            for name, n in pairs)

    area_bars = bars([(name, sum(s.values())) for name, s in m["sections"].items()])
    env_bars = bars([(env, v["pass"]) for env, v in m["by_env"].items()], "ok")

    def callout(tone_cls, heading, hits):
        items = "".join(
            f"<li>#{e(r['id'])} {e(r['test'])}" + (f" - {e(r['notes'])}" if r["notes"] else "") + "</li>" for r in hits)
        return f'<div class="callout {tone_cls}"><b>{e(heading)} ({len(hits)})</b><ul>{items}</ul></div>'

    boxes = []
    for status, tone_cls, heading in (("fail", "red", "Failures"), ("blocked", "amber", "Blocked"),
                                      ("out of scope", "", "Out of scope")):
        hits = [r for r in rows if r["status"] == status]
        if hits:
            boxes.append(callout(tone_cls, heading, hits))
    if not c["fail"]:
        boxes.insert(0, '<div class="callout green"><b>No failures</b><p>Every executed case met its expected result.</p></div>')
    if m["unconfirmed"]:
        boxes.append(callout("amber", "Expected result not confirmed",
                             [r for r in rows if r["unconfirmed"]]))
    if m["unrecognised"]:
        boxes.append('<div class="callout amber"><b>Unrecognised result values</b><ul>'
                     + "".join(f"<li>{e(u)}</li>" for u in m["unrecognised"]) + "</ul></div>")

    area_rows = "".join(
        f"<tr><td>{e(name)}</td><td class='n'>{sum(s.values())}</td><td class='n'>{s['pass']}</td>"
        f"<td class='n'>{s['fail']}</td><td class='n'>{s['blocked']}</td><td class='n'>{s['not run']}</td></tr>"
        for name, s in m["sections"].items())
    summary = (f"{c['pass']}/{m['executed']} executed cases passed across {len(m['sections'])} areas; "
               f"{c['fail']} failed, {c['blocked']} blocked, {c['not run']} not run. Verdict: {m['verdict']}.")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}: test report</title><style>{HTML_CSS}</style></head><body><div class="page">
<div class="head"><h1>{e(title)}</h1><span class="badge {tone}">{e(m['verdict'])}</span></div>
<p class="tiny">{e(context or 'No context given')} · {m['total']} test rows ({m['closure_rows']} closure rows excluded)</p>
<div class="kpis">{''.join(tiles)}</div>
<div class="cols"><div><h2>Cases per area</h2>{area_bars}</div>
<div><h2>Passing cases per environment</h2>{env_bars}</div></div>
<h2>Findings</h2><div class="callouts">{''.join(boxes)}</div>
<h2>By area</h2><table><thead><tr><th>Area</th><th class="n">Cases</th><th class="n">Passed</th>
<th class="n">Failed</th><th class="n">Blocked</th><th class="n">Not run</th></tr></thead><tbody>{area_rows}</tbody></table>
<h2>Summary</h2><p>{e(summary)}</p>
</div></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True)
    ap.add_argument("--output")
    ap.add_argument("--html", help="also write a self-contained HTML one-pager of the same numbers")
    ap.add_argument("--title", default="")
    ap.add_argument("--context", default="")
    ap.add_argument("--json", action="store_true", help="also print metrics as JSON to stderr")
    args = ap.parse_args()
    plan_title, rows, closure = parse(Path(args.input).read_text(encoding="utf-8"))
    m = metrics(rows, closure)
    report = render(args.title or plan_title or "Test plan", args.context, m, rows)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    if args.html:
        Path(args.html).write_text(
            render_html(args.title or plan_title or "Test plan", args.context, m, rows), encoding="utf-8")
    if args.json:
        print(json.dumps(m, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
