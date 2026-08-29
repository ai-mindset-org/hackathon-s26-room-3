# Канон контента — структурная версия

Человекочитаемый документ с одним машинным блоком ```toml``` ниже.
Меняешь блок → меняется поведение линтера. Кода трогать не нужно.

Смысловые правила (вариации антитезы, тон, «событие ли это для читателя»)
здесь ловятся только в буквальной форме: поле `judgment_extends = true`
помечает, что вариации должен добрать модуль `judge/`.

Семантика повторяет `examples/canon.md` (приёмка комнаты) плюс блок
`redaction` — безопасность публикации (кейс заказчика: лог сессии наружу).

```toml
[meta]
name = "Канон контента (synthetic, приёмка room-3) + redaction"
source = "examples/canon.md"

# ── п.1 ──────────────────────────────────────────────────────────────
[[rule]]
id = "no-emoji"
point = 1
kind = "emoji"
severity = "error"
message = "эмодзи запрещены (п.1)"
fix = "убрать эмодзи"

# ── п.2 ──────────────────────────────────────────────────────────────
[[rule]]
id = "headline-lowercase"
point = 2
kind = "headline_case"
severity = "error"
message = "заголовок должен начинаться со строчной буквы (п.2)"
fix = "начать заголовок со строчной буквы"

# ── п.3 ── (буквальные формы; вариации → judge/) ─────────────────────
[[rule]]
id = "no-antithesis"
point = 3
kind = "regex_forbidden"
severity = "error"
judgment_extends = true
patterns = [
  '(?i)\bне\s+(?:просто\s+|только\s+)?[^,.\n]{1,40},\s+а\s+\S',
  '(?i)\bэто\s+не\s+[^—\n]{1,50}\s*—\s*это\b',
  '(?i)\bне\s+[^,.\n]{1,40}\s+—\s+а\s+',
]
message = "антитеза «не X, а Y» (п.3)"
fix = "переформулировать без противопоставления"

# ── п.4 ──────────────────────────────────────────────────────────────
[[rule]]
id = "forbidden-words"
point = 4
kind = "stem_forbidden"
severity = "error"
stems = ["уникальн", "инновацион", "прорывн", "синерги"]
message = "запрещённое слово (п.4)"
fix = "убрать или заменить нейтральным словом"

# ── п.5 ──────────────────────────────────────────────────────────────
[[rule]]
id = "paragraph-max-lines"
point = 5
kind = "paragraph_max_lines"
severity = "warning"
max = 4
message = "абзац длиннее 4 строк (п.5)"
fix = "разбить абзац"

[[rule]]
id = "post-max-chars"
point = 5
kind = "doc_max_chars"
severity = "warning"
max = 1200
message = "пост длиннее 1200 знаков (п.5)"
fix = "сократить"

# ── п.6 ──────────────────────────────────────────────────────────────
[[rule]]
id = "number-needs-source"
point = 6
kind = "number_without_source"
severity = "error"
message = "утверждение с числом без источника в скобках (п.6)"
fix = "добавить источник в скобках: … (источник)"

# ── п.7 ──────────────────────────────────────────────────────────────
[[rule]]
id = "cta-no-subscribe"
point = 7
kind = "stem_forbidden"
severity = "error"
stems = ["подписывайт", "подпишит", "подписыва"]
message = "CTA «подписывайтесь» запрещён (п.7)"
fix = "заменить одним конкретным действием для читателя"

# ── п.8 ──────────────────────────────────────────────────────────────
[[rule]]
id = "clericalese-phrases"
point = 8
kind = "phrase_forbidden"
severity = "error"
phrases = ["в рамках", "на сегодняшний день", "в связи с этим"]
message = "канцелярит (п.8)"
fix = "убрать или сказать проще"

[[rule]]
id = "clericalese-stems"
point = 8
kind = "stem_forbidden"
severity = "error"
stems = ["осуществл"]
message = "канцелярит (п.8)"
fix = "сказать проще: «делать», «идёт»"

[[rule]]
id = "clericalese-danniy"
point = 8
kind = "form_forbidden"
severity = "warning"
forms = ["данный", "данная", "данное", "данного", "данной", "данном", "данным"]
message = "канцелярит «данный» (п.8)"
fix = "убрать или заменить на «этот»"
note = "формы данные/данных/данными не проверяются — коллизия со словом «данные»"

# ── redaction ── (вне нумерации канона; безопасность публикации) ─────
[[rule]]
id = "redact-abs-path"
point = 0
kind = "regex_forbidden"
category = "redaction"
severity = "error"
patterns = ['(?:/home/|/Users/|/root/|/opt/)[\w./-]{2,}', '[A-Za-z]:\\[\w.\\-]{2,}']
message = "абсолютный путь машины — вычистить перед публикацией"
fix = "заменить условным путём или убрать"

[[rule]]
id = "redact-secret"
point = 0
kind = "regex_forbidden"
category = "redaction"
severity = "error"
patterns = ['\b(?:ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})\b']
message = "секрет или токен — вычистить, при утечке ротировать"
fix = "убрать секрет из текста"

[[rule]]
id = "redact-email"
point = 0
kind = "regex_forbidden"
category = "redaction"
severity = "warning"
patterns = ['\b[\w.+-]+@[\w-]+\.[A-Za-z]{2,}\b']
message = "e-mail — проверить перед публикацией"
fix = "обезличить, если адрес не публичный"
```
