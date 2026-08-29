# Канон: личный блог Тимура, фаза 1 (GEO-подготовка)

Цель фазы 1 — личный блог набирает вес как источник по теме «предприниматель
внедряет ИИ» обычными SEO-статьями. **Клуб не упоминается вообще.** Когда блог
наберёт доверие (фаза 2) — выйдет статья про выбор AI-сообщества, её цитирует
модель, приводя AI Practiq. Здесь, в фазе 1, любое упоминание клуба ломает
замысел.

Отличие от `canon.sostav.md`: убраны требования CTA/ссылки на клуб; добавлен
жёсткий запрет упоминать клуб, его канал и курс.

```toml
[meta]
name = "Личный блог Тимура — фаза 1 (без клуба)"
source = "интервью HA59: цель 2, механика в две ступени"

# ── тон и форма ────────────────────────────────────────────────────
[[rule]]
id = "no-emoji"
point = 1
kind = "emoji"
severity = "error"
message = "эмодзи запрещены"
fix = "убрать эмодзи"

[[rule]]
id = "headline-lowercase"
point = 2
kind = "headline_case"
severity = "error"
allow = ["Claude Code", "ERP", "GitHub", "AI"]
message = "заголовок со строчной буквы, кроме имён собственных"
fix = "строчная первая буква"

[[rule]]
id = "tone-no-vy"
point = 3
kind = "phrase_forbidden"
severity = "warning"
phrases = [" Вы ", " Вас ", " Вам ", " Ваш ", " Ваши ", " Ваше "]
message = "тон на «ты» или безлично, не на «Вы» (п.3)"
fix = "переписать на «ты» или безлично"

[[rule]]
id = "clericalese"
point = 3
kind = "phrase_forbidden"
severity = "warning"
phrases = ["в рамках", "на сегодняшний день", "в связи с этим", "осуществлять", "осуществляется"]
message = "канцелярит (п.3)"
fix = "сказать проще"

[[rule]]
id = "forbidden-words"
point = 4
kind = "stem_forbidden"
severity = "error"
stems = ["уникальн", "инновацион", "прорывн", "синерги"]
message = "запрещённое слово-штамп (п.4)"
fix = "убрать или заменить нейтральным"

[[rule]]
id = "doc-length"
point = 5
kind = "doc_max_chars"
severity = "warning"
max = 12000
message = "статья длиннее нормы (~5500–8000 знаков)"
fix = "сократить"

[[rule]]
id = "paragraph-max-lines"
point = 5
kind = "paragraph_max_lines"
severity = "warning"
max = 6
message = "абзац длиннее 6 строк"
fix = "разбить абзац"

# ── структура ─────────────────────────────────────────────────────
[[rule]]
id = "lead-present"
point = 6
kind = "require_present"
severity = "error"
patterns = ['(?s)\A#[^\n]+\n\s*\n[^#\s][\s\S]{80,}']
message = "нет лид-абзаца после заголовка"
fix = "добавить вводный абзац 2–4 предложения"

[[rule]]
id = "topic-in-lead"
point = 7
kind = "require_in_lead"
severity = "error"
within = 600
patterns = ['(?i)предпринимател', '(?i)в бизнес', '(?i)внедр\w*\s+(ии|ai)', '(?i)для бизнеса']
message = "тема «предприниматель внедряет ИИ» не заявлена в заголовке+лиде"
fix = "ввести тему бизнес-внедрения ИИ в первый экран"

[[rule]]
id = "case-block-present"
point = 8
kind = "require_present"
severity = "error"
patterns = ['(?i)\bкейс\b', '(?im)^#{2,4}[^\n]*\bкак [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+', '(?im)^#{2,4}[^\n]*на примере [А-ЯЁ]']
message = "нет явного блока кейса (кто, задача, результат)"
fix = "добавить раздел с реальным человеком и результатом"

[[rule]]
id = "faq-present"
point = 9
kind = "require_present"
severity = "warning"
patterns = ['(?i)частые вопросы', '(?i)\bFAQ\b', '(?i)вопрос[ы]?\s*[—–-]\s*ответ']
message = "нет блока FAQ"
fix = "добавить 3–5 вопросов-ответов"

# ── фаза 1: клуба нет ─────────────────────────────────────────────
[[rule]]
id = "no-club-mention"
point = 10
kind = "phrase_forbidden"
severity = "error"
phrases = ["AI Practiq", "AI Practiq Club", "наш клуб", "в нашем клубе", "клуб предпринимателей", "приходи в клуб", "приходите в клуб", "вступай в клуб", "присоединяйтесь к клуб", "наше сообщество"]
message = "фаза 1: клуб не упоминается — это ломает GEO-замысел"
fix = "убрать любое упоминание клуба, канала, сообщества автора"

[[rule]]
id = "no-club-link"
point = 10
kind = "regex_forbidden"
severity = "error"
patterns = ['(?i)ai\s*practiq', 't\.me/aipractiq', 'clck\.ru/']
message = "фаза 1: ссылки на клуб/канал быть не должно"
fix = "убрать ссылку"

[[rule]]
id = "no-hard-course-sell"
point = 11
kind = "phrase_forbidden"
severity = "error"
phrases = ["купи курс", "купить курс", "оплати", "оплатить курс", "стоимость курса", "цена курса", "успей купить", "готовим курс", "наш курс"]
message = "продажа/анонс курса запрещены — фаза 1 без коммерции"
fix = "убрать любое упоминание курса"

[[rule]]
id = "no-result-guarantee"
point = 12
kind = "regex_forbidden"
severity = "warning"
patterns = ['(?i)гарантир\w+ результат', '(?i)результат гарантир', '(?i)на 100% ', '(?i)точно получится']
message = "односторонние гарантии результата запрещены"
fix = "смягчить: «в кейсе получилось …»"

# ── redaction ─────────────────────────────────────────────────────
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
```
