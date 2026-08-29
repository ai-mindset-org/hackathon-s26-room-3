# Контракты canon-lens

Предложение HA59 для комнаты. Два интерфейса: формат канона и форма записи
нарушения. На них опираются `judge/`, `report/`, `rewrite/`, `lens/`.

---

## 1. Формат `canon.md`

Markdown-документ с **одним** fenced-блоком ` ```toml `. Всё вне блока —
пояснения для человека. Меняется без правки кода.

```toml
[meta]
name = "..."            # человекочитаемое имя канона
source = "..."          # откуда семантика (опц.)

[[rule]]
id = "no-emoji"         # уникальный идентификатор правила
point = 1               # номер пункта канона; 0 = вне нумерации (redaction)
kind = "emoji"          # см. таблицу видов ниже
severity = "error"      # error | warning
category = "canon"      # canon | redaction   (по умолчанию canon)
message = "эмодзи запрещены (п.1)"
fix = "убрать эмодзи"   # подсказка правки (опц.)
judgment_extends = false # true → буквальное ловит canon-lens, вариации — judge/
# kind-специфичные поля:
patterns = ['regex', ...]   # regex_forbidden  (TOML literal strings!)
stems    = ["основа", ...]  # stem_forbidden   — слово, начинающееся с основы
phrases  = ["фраза", ...]   # phrase_forbidden — буквально, регистронезависимо
forms    = ["словоформа"]   # form_forbidden   — точная форма
max      = 1200             # paragraph_max_lines | doc_max_chars
```

### Виды правил (`kind`)

| kind | параметр | нарушение = |
|---|---|---|
| `emoji` | — | символ из диапазонов эмодзи |
| `regex_forbidden` | `patterns[]` | совпадение любого паттерна |
| `stem_forbidden` | `stems[]` | слово, начинающееся с основы |
| `phrase_forbidden` | `phrases[]` | буквальная фраза (регистронезависимо) |
| `form_forbidden` | `forms[]` | точная словоформа |
| `headline_case` | — | первый `#`-заголовок не со строчной буквы |
| `paragraph_max_lines` | `max` | абзац длиннее `max` строк |
| `doc_max_chars` | `max` | документ длиннее `max` знаков |
| `number_without_source` | — | число в строке без `(…)` рядом |

Новый вид правила = код в `canon_lens/check.py` (`_DISPATCH`). Всё остальное —
данными.

---

## 2. Форма записи нарушения (`Violation`)

Один объект на нарушение. JSON-выход `check --json`: `{file, summary, violations[]}`.

```json
{
  "rule": "forbidden-words",     // id правила из канона
  "point": 4,                    // пункт канона (0 = redaction)
  "category": "canon",           // canon | redaction
  "severity": "error",           // error | warning
  "kind": "mechanical",          // mechanical | redaction | judgment-literal
  "line": 3,                     // 1-based
  "col": 42,                     // 1-based
  "end_col": 51,
  "offset": [86, 95],            // [start, end) абсолютный сдвиг в тексте
  "quote": "прорывной",          // точный фрагмент
  "message": "запрещённое слово (п.4)",
  "fix": "убрать или заменить нейтральным словом"
}
```

`summary`: `{total, errors, warnings, points[], clean}`.

### Как этим пользуются другие модули

- **`judge/`** — выдаёт объекты той же формы для смысловых правил
  (`kind: "judgment"`), `report/` их объединяет с механическими по `offset`.
- **`rewrite/`** — берёт `offset` + `fix`, правит текст, каждую правку линкует
  на `rule`/`point`.
- **`lens/`** — рисует `offset`-спаны поверх текста, панель по `point`.

### Стабильность

`rule`, `point`, `offset`, `quote`, `severity` — не меняются. Новые поля
добавляются только опциональными.
