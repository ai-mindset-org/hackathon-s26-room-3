"""Сквозная команда: статья -> факты -> сценарий рилза + отчёт.

    python reels/run.py reels/input/sostav-86369.md
    python reels/run.py 86369                       # сначала скачает статью
    python reels/run.py reels/input/               # все статьи папки

Между шагами руками ничего не делается — это и есть конвейер.

Добытчик фактов выбирается сам: если в репозитории есть `reels/extract`
(ведёт meta1ex), берётся он; иначе включается запасной разбор из
`reels/compose/stopgap_extract.py` — беднее, но конвейер целый. Каким
добытчиком собрано, печатается в выводе и пишется в отчёт.
"""

import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reels.compose import build, lens  # noqa: E402
from reels.tools import fetch_article  # noqa: E402

try:
    from reels.extract import extract as _extract  # noqa: F401
    EXTRACTOR = "reels.extract"
except Exception:
    from reels.compose.stopgap_extract import extract as _extract
    EXTRACTOR = "stopgap"


def one(path, canon, out_root):
    data = _extract(path)
    article_id = data["source"]["id"]
    out_dir = os.path.join(out_root, article_id)
    os.makedirs(out_dir, exist_ok=True)

    facts_path = os.path.join(out_dir, "facts.json")
    io.open(facts_path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(data, ensure_ascii=False, indent=2))

    source_text = io.open(path, encoding="utf-8").read()
    try:
        script, used, template_cta = build.render(data, canon)
    except build.Refusal as refusal:
        text = build.report(data, canon, refusal=str(refusal),
                            source_text=source_text, extractor=EXTRACTOR)
        io.open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8",
                newline="\n").write(text)
        script_path = os.path.join(out_dir, "script.md")
        if os.path.exists(script_path):
            os.remove(script_path)
        return article_id, None, len(data["facts"])

    io.open(os.path.join(out_dir, "script.md"), "w", encoding="utf-8",
            newline="\n").write(script)
    text = build.report(data, canon, script=script, used=used,
                        template_cta=template_cta, source_text=source_text,
                        extractor=EXTRACTOR)
    io.open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8",
            newline="\n").write(text)
    return article_id, used, len(data["facts"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="статья -> сценарий рилза")
    ap.add_argument("target", help="файл статьи, папка со статьями или id статьи sostav")
    ap.add_argument("--canon", default="examples/canon.md")
    ap.add_argument("-o", "--out", default="reels/out")
    ap.add_argument("--input-dir", default="reels/input")
    args = ap.parse_args(argv)

    try:
        canon = lens.load(args.canon)
    except (OSError, ValueError, lens.CanonUnreadable) as exc:
        print(f"канон не прочитан: {exc}", file=sys.stderr)
        return 2

    target = args.target
    if not os.path.exists(target):
        print(f"качаю статью {target}")
        target, _, _ = fetch_article.fetch(target, args.input_dir)

    paths = ([os.path.join(target, n) for n in sorted(os.listdir(target)) if n.endswith(".md")]
             if os.path.isdir(target) else [target])
    if not paths:
        print("статей не найдено", file=sys.stderr)
        return 2

    print(f"добытчик фактов: {EXTRACTOR} · движок канона: {lens.ENGINE}")
    for path in paths:
        article_id, used, total = one(path, canon, args.out)
        where = os.path.join(args.out, article_id)
        if used is None:
            print(f"  {article_id}: контента нет · фактов {total} · {where}/report.md")
        else:
            print(f"  {article_id}: сценарий из {len(used)} фактов "
                  f"(добыто {total}) · {where}/script.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
