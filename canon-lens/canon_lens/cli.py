"""CLI: canon-lens check <файл> [--canon canon.md] [--json]

Выход:
  человекочитаемо — нарушения, сгруппированные по пунктам канона;
  --json         — список записей нарушений (контракт для judge/ и lens/).
Код возврата: 1 если есть нарушения severity=error, иначе 0.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .rules import load_canon
from .check import check_text, summary

DEFAULT_CANON = Path(__file__).resolve().parent.parent / "canon.md"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="canon-lens", description="проверка текста против канона")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="проверить файл против канона")
    c.add_argument("file", help="текстовый файл для проверки")
    c.add_argument("--canon", default=str(DEFAULT_CANON), help=f"канон (по умолчанию {DEFAULT_CANON.name})")
    c.add_argument("--json", action="store_true", help="выдать JSON-список нарушений")
    a = p.parse_args(argv)

    if a.cmd == "check":
        text = Path(a.file).read_text(encoding="utf-8")
        canon = load_canon(a.canon)
        vs = check_text(text, canon)
        if a.json:
            print(json.dumps({"file": a.file, "summary": summary(vs),
                              "violations": [v.as_dict() for v in vs]},
                             ensure_ascii=False, indent=2))
        else:
            _pretty(a.file, vs)
        return 1 if any(v.severity == "error" for v in vs) else 0
    return 2


def _pretty(fname: str, vs) -> None:
    if not vs:
        print(f"{fname}: нарушений канона не найдено")
        return
    s = summary(vs)
    print(f"{fname}: {s['total']} нарушений ({s['errors']} error, {s['warnings']} warning)\n")
    by_pt: dict[int, list] = {}
    for v in vs:
        by_pt.setdefault(v.point, []).append(v)
    for pt in sorted(by_pt):
        head = f"п.{pt} канона" if pt else "редакция (безопасность публикации)"
        print(f"── {head} ──")
        for v in by_pt[pt]:
            mark = "✗" if v.severity == "error" else "•"
            print(f"  {mark} {v.line}:{v.col}\t«{v.quote}»\t{v.message}")
            if v.fix:
                print(f"       → {v.fix}")
        print()


if __name__ == "__main__":
    sys.exit(main())
