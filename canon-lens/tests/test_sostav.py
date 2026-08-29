"""Мини-тест канона Sostav: плохой черновик ловится, хороший — чистый по error.

Запуск (из любой папки):  python canon-lens/tests/test_sostav.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))            # canon-lens/ → import canon_lens

from canon_lens.rules import load_canon             # noqa: E402
from canon_lens.check import check_text, summary    # noqa: E402

CANON = HERE.parents[1] / "canon.sostav.md"
BAD = HERE.parent / "fixtures" / "sostav-draft-bad.md"
OK = HERE.parent / "fixtures" / "sostav-draft-ok.md"


def run() -> int:
    canon = load_canon(CANON)
    bad = check_text(BAD.read_text(encoding="utf-8"), canon)
    ok = check_text(OK.read_text(encoding="utf-8"), canon)
    bad_rules = {v.rule for v in bad}
    ok_s = summary(ok)

    checks = {
        "плохой: эмодзи":              "no-emoji" in bad_rules,
        "плохой: Заголовок Капсом":    "headline-lowercase" in bad_rules,
        "плохой: слово-штамп":         "forbidden-words" in bad_rules,
        "плохой: нет блока кейса":     "case-block-present" in bad_rules,
        "плохой: нет FAQ":            "faq-present" in bad_rules,
        "плохой: нет CTA на клуб":     "club-cta-present" in bad_rules,
        "плохой: продажа курса в лоб": "no-hard-course-sell" in bad_rules,
        "плохой: гарантия результата": "no-result-guarantee" in bad_rules,
        "хороший: нет error-нарушений": ok_s["errors"] == 0,
    }
    passed = all(checks.values())
    for name, ok_ in checks.items():
        print(f"  {'OK  ' if ok_ else 'FAIL'} {name}")
    print(f"\n{'PASS' if passed else 'FAIL'} — {sum(checks.values())}/{len(checks)}")
    print(f"  плохой: {summary(bad)}  ")
    print(f"  хороший: {ok_s}")
    if ok_s["errors"]:
        for v in ok:
            if v.severity == "error":
                print(f"    ! {v.rule}: {v.message}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(run())
