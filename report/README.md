# report

Модуль участника **MG7S**. Единый отчёт из находок разных модулей по общему
контракту `Violation` (`canon-lens/CONTRACTS.md §2`).

## Что делает

`canon-lens` даёт механические/redaction-нарушения, `judge` — смысловые, оба в
форме `{file, summary, violations[]}`. `report` их **мёржит по `offset`**,
дедуплицирует по `(rule, offset)`, сортирует по месту в тексте и печатает один
отчёт — по пунктам канона, с пометкой источника (механика / судья / редакция).
Детерминированно, без LLM.

## Запуск

```bash
# получить выходы модулей:
PYTHONPATH=canon-lens python -m canon_lens.cli check post.md --json > mech.json
PYTHONPATH=judge      python -m judge.cli      check post.md --offline --json > judge.json

# слить в единый отчёт:
PYTHONPATH=report python -m report.cli merge mech.json judge.json          # человекочитаемо
PYTHONPATH=report python -m report.cli merge mech.json judge.json --json   # единый контракт

# тесты:
python report/tests/test_merge.py    # PASS 7/7
```

Код возврата `merge`: `1` если есть `severity=error`, иначе `0`.

## Итоговый summary

К полям контракта добавлена разбивка `by_kind` (сколько находок механических,
судейских, redaction) — видно, какой слой что поймал:

```json
{"total": 3, "errors": 3, "warnings": 0, "points": [3, 4],
 "by_kind": {"mechanical": 1, "judgment-literal": 1, "judgment": 1}, "clean": false}
```

Только stdlib (Python ≥ 3.11). Папка изолирована. Секретов нет.

## Отношение к другим модулям

- вход — выходы `canon-lens` (HA59) и `judge` (MG7S);
- `report` — то, что делает из набора линтеров один продукт: одна картина
  нарушений по всему тексту, независимо от того, каким слоем найдено.
