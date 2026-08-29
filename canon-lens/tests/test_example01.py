"""Мини-тест: линтер ловит все нарушения из examples/01-вычитка/expected.md.

Запуск (из любой папки):  python canon-lens/tests/test_example01.py
Выход — одна строка PASS/FAIL. Нужен для приёмки без запуска pytest.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))            # canon-lens/ → import canon_lens
REPO = HERE.parents[2]

from canon_lens.rules import load_canon             # noqa: E402
from canon_lens.check import check_text             # noqa: E402

INPUT = REPO / "examples" / "01-вычитка" / "input" / "черновик-поста.md"
CANON = HERE.parents[1] / "canon.md"


def run() -> int:
    text = INPUT.read_text(encoding="utf-8")
    vs = check_text(text, load_canon(CANON))
    points = [v.point for v in vs]
    quotes = " ".join(v.quote.lower() for v in vs)

    # ожидаемое из examples/01-вычитка/expected.md
    checks = {
        "п.1 эмодзи в заголовке":        1 in points,
        "п.2 заголовок с заглавных":     2 in points,
        "п.3 антитеза «не X, а Y»":      3 in points,
        "п.4 три запрещённых слова":     points.count(4) >= 3,
        "п.6 «40%» без источника":       6 in points and "40" in quotes,
        "п.7 CTA «подписывайтесь»":      7 in points,
        "п.8 канцелярит (рамках/осущ.)": 8 in points and ("рамках" in quotes or "осуществ" in quotes),
    }
    ok = all(checks.values())
    for name, passed in checks.items():
        print(f"  {'OK  ' if passed else 'FAIL'} {name}")
    print(f"\n{'PASS' if ok else 'FAIL'} — {sum(checks.values())}/{len(checks)} "
          f"(всего нарушений: {len(vs)}, пункты: {sorted(set(points))})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
