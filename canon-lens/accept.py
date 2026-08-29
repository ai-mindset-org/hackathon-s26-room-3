#!/usr/bin/env python3
"""accept — приёмочная проверка одного каталога example/ движком canon-lens.

Каталог примера: `input/` (один или несколько файлов) + `expected.md`.
Скрипт запускает `check` по каждому файлу input/, собирает пойманные пункты
канона и сверяет с номерами пунктов, упомянутыми в `expected.md` как «(п.N)».
Печатает `прошло N из M` + список промахов. Код возврата 0/1.

    python canon-lens/accept.py examples/01-вычитка [--canon canon-lens/canon.md]

Для runner'а комнаты: импортировать `run(example_dir, canon_path) -> dict`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from canon_lens.rules import load_canon          # noqa: E402
from canon_lens.check import check_text, summary  # noqa: E402

DEFAULT_CANON = HERE.parent / "canon.md"
_POINT_RE = re.compile(r"\(п\.\s*(\d+)\)")


def _expected_points(expected_md: Path) -> set[int]:
    return {int(n) for n in _POINT_RE.findall(expected_md.read_text(encoding="utf-8"))}


def run(example_dir: str | Path, canon_path: str | Path = DEFAULT_CANON) -> dict:
    d = Path(example_dir)
    exp_file = d / "expected.md"
    inputs = sorted((d / "input").glob("*")) if (d / "input").is_dir() else []
    if not exp_file.exists() or not inputs:
        return {"dir": str(d), "ok": False, "error": "нет expected.md или input/"}

    canon = load_canon(canon_path)
    want = _expected_points(exp_file)
    got: set[int] = set()
    per_file = []
    for f in inputs:
        vs = check_text(f.read_text(encoding="utf-8"), canon)
        pts = {v.point for v in vs}
        got |= pts
        per_file.append({"file": f.name, "summary": summary(vs)})

    hit = want & got
    missed = sorted(want - got)
    return {
        "dir": str(d),
        "canon": str(canon_path),
        "expected_points": sorted(want),
        "caught_points": sorted(got),
        "passed": len(hit),
        "of": len(want),
        "missed": missed,
        "ok": not missed,
        "per_file": per_file,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="accept", description="приёмка одного example/ движком canon-lens")
    p.add_argument("example_dir")
    p.add_argument("--canon", default=str(DEFAULT_CANON))
    a = p.parse_args(argv)

    r = run(a.example_dir, a.canon)
    if r.get("error"):
        print(f"{r['dir']}: {r['error']}")
        return 2
    print(f"{r['dir']}  (канон: {Path(r['canon']).name})")
    print(f"  ожидались пункты: {r['expected_points']}")
    print(f"  поймано:          {r['caught_points']}")
    if r["of"] == 0:
        print("\n  в expected.md нет ссылок «(п.N)» — приёмка этого примера не через canon-lens\n"
              "  (рилз/дайджест — генерация, не нарушения канона)")
        return 0
    if r["missed"]:
        print(f"  ПРОМАХ по пунктам: {r['missed']}")
    print(f"\nпрошло {r['passed']} из {r['of']}  →  {'OK' if r['ok'] else 'FAIL'}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
