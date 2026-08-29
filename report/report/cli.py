"""CLI: report merge <out1.json> <out2.json> ... [--json]

Читает JSON-выходы модулей (`canon-lens check --json`, `judge check --json`),
мёржит в один отчёт. Человекочитаемо — по пунктам канона с пометкой источника;
`--json` — единый контракт {file, summary, violations[]}.
Код возврата: 1 если есть severity=error, иначе 0.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .merge import merge_reports

_KIND_MARK = {
    "mechanical": "механика",
    "judgment": "судья",
    "judgment-literal": "механика",
    "redaction": "редакция",
}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass
    p = argparse.ArgumentParser(prog="report", description="единый отчёт из находок модулей")
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge", help="слить JSON-выходы модулей в один отчёт")
    m.add_argument("inputs", nargs="+", help="файлы JSON-выходов (canon-lens/judge)")
    m.add_argument("--json", action="store_true", help="выдать единый JSON-контракт")
    a = p.parse_args(argv)

    if a.cmd != "merge":
        return 2

    reports = [json.loads(Path(f).read_text(encoding="utf-8")) for f in a.inputs]
    rep = merge_reports(reports)

    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        _pretty(rep)
    return 1 if any(v.get("severity") == "error" for v in rep["violations"]) else 0


def _pretty(rep: dict) -> None:
    vs = rep["violations"]
    s = rep["summary"]
    if not vs:
        print(f"{rep['file']}: нарушений не найдено")
        return
    kinds = ", ".join(f"{k}: {n}" for k, n in sorted(s["by_kind"].items()))
    print(f"{rep['file']}: {s['total']} нарушений "
          f"({s['errors']} error, {s['warnings']} warning)  [{kinds}]\n")
    by_pt: dict[int, list] = {}
    for v in vs:
        by_pt.setdefault(v.get("point", 0), []).append(v)
    for pt in sorted(by_pt):
        head = f"п.{pt} канона" if pt else "редакция (безопасность публикации)"
        print(f"── {head} ──")
        for v in by_pt[pt]:
            mark = "✗" if v.get("severity") == "error" else "•"
            src = _KIND_MARK.get(v.get("kind", "mechanical"), v.get("kind", ""))
            off = v.get("offset", [0, 0])
            loc = f"{v.get('line', 1)}:{v.get('col', 1)}" if off != [0, 0] else "весь текст"
            print(f"  {mark} [{src}] {loc}\t«{v.get('quote', '')}»\t{v.get('message', '')}")
            if v.get("fix"):
                print(f"       → {v['fix']}")
        print()


if __name__ == "__main__":
    sys.exit(main())
