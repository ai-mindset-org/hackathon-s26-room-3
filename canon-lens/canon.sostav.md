# Канон: клубный блог AI Practiq на Sostav.ru

Собран из 3 опубликованных статей Тимура Яковлева (sostav.ru/blogs/289407/):
`86369`, `89284`, `97142`. Цель статьи — вход в воронку `SEO → Telegram-канал → курс`.
Claude Code — тема-приманка, суть — сообщество предпринимателей AI Practiq.

Отличия от synthetic `canon.md`: CTA «подписывайтесь на канал» здесь **разрешён**
(это и есть цель), плюс появились структурные требования (лид, блок кейса, FAQ,
SEO-ключ в лиде, 1–2 CTA на клуб). Кода менять не нужно — только этот файл.

```toml
[meta]
name = "AI Practiq — клубный блог на Sostav"
source = "sostav.ru/blogs/289407/{86369,89284,97142}"
seo_key = "Claude Code"   # на конкретную статью подставляется свой узкий ключ

# ── тон и форма (общее с synthetic) ─────────────────────────────────
[[rule]]
id = "no-emoji"
point = 1
kind = "emoji"
severity = "error"
message = "эмодзи запрещены (во всех 3 статьях их нет)"
fix = "убрать эмодзи"

[[rule]]
id = "headline-lowercase"
point = 2
kind = "headline_case"
severity = "error"
allow = ["Claude Code", "AI Practiq", "ERP", "GitHub"]
message = "заголовок со строчной буквы, кроме имён собственных"
fix = "строчная первая буква; «Claude Code» оставить как есть"

[[rule]]
id = "tone-no-vy"
point = 3
kind = "phrase_forbidden"
severity = "warning"
phrases = [" Вы ", " Вас ", " Вам ", " Ваш ", " Ваши ", " Ваше "]
message = "тон на «ты» или безлично, не на «Вы» (п.3)"
fix = "переписать на «ты» или безличную конструкцию"

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

# ── объём и ритм ────────────────────────────────────────────────────
[[rule]]
id = "doc-length"
point = 5
kind = "doc_max_chars"
severity = "warning"
max = 12000
message = "статья длиннее нормы (в статьях Тимура ~5500–8000 знаков)"
fix = "сократить"

[[rule]]
id = "paragraph-max-lines"
point = 5
kind = "paragraph_max_lines"
severity = "warning"
max = 6
message = "абзац длиннее 6 строк (у Тимура 2–4 предложения, редко 6)"
fix = "разбить абзац"

# ── структура (новое; require_*) ───────────────────────────────────
[[rule]]
id = "lead-present"
point = 6
kind = "require_present"
severity = "error"
patterns = ['(?s)\A#[^\n]+\n\s*\n[^#\s][\s\S]{80,}']
message = "нет лид-абзаца после заголовка (во всех 3 статьях есть)"
fix = "добавить вводный абзац 2–4 предложения перед первым подзаголовком"

[[rule]]
id = "seo-key-in-lead"
point = 7
kind = "require_in_lead"
severity = "error"
within = 600
patterns = ['(?i)Claude Code']
message = "SEO-ключ не встречается в заголовке + первом абзаце (п.7)"
fix = "ввести ключевую фразу в заголовок и лид"

[[rule]]
id = "seo-key-frequency"
point = 7
kind = "keyword_min_count"
severity = "warning"
keyword = "Claude Code"
min = 3
message = "SEO-ключ повторяется реже 3 раз (в статьях Тимура 3–12)"
fix = "повысить частоту ключа до 3+ естественным образом"

[[rule]]
id = "case-block-present"
point = 8
kind = "require_present"
severity = "error"
patterns = ['(?i)\bкейс\b', '(?im)^#{2,4}[^\n]*\bкак [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+', '(?im)^#{2,4}[^\n]*на примере [А-ЯЁ]']
message = "нет явного блока кейса участника (имя + задача + результат)"
fix = "добавить раздел с реальным участником клуба: кто, что делал, результат с цифрами"

[[rule]]
id = "faq-present"
point = 9
kind = "require_present"
severity = "warning"
patterns = ['(?i)частые вопросы', '(?i)\bFAQ\b', '(?i)вопрос[ы]?\s*[—–-]\s*ответ']
message = "нет блока FAQ / «Частые вопросы» (есть во всех 3 статьях)"
fix = "добавить раздел с 3–5 частыми вопросами и ответами"

# ── CTA и бренд ────────────────────────────────────────────────────
[[rule]]
id = "club-cta-present"
point = 10
kind = "require_present"
severity = "error"
patterns = ['(?i)ai\s*practiq', 't\.me/', 'clck\.ru/', '(?i)присоединяйтесь к клуб', '(?i)приходи в клуб']
message = "нет CTA/ссылки на клуб или канал AI Practiq — статья не закрывает воронку"
fix = "добавить один призыв в конце: ссылка на клуб или канал AI Practiq"

[[rule]]
id = "club-cta-count"
point = 10
kind = "count_range"
severity = "warning"
min = 1
max = 3
patterns = ['(?i)присоединяйтесь к ai\s*practiq', '(?i)приходи в клуб', '(?i)подписывайтесь на канал', '(?i)следите за анонсами', '(?i)приходи в клуб']
message = "число CTA на клуб/канал"
fix = "оставить 1–2 призыва, оба в конце статьи"

[[rule]]
id = "no-hard-course-sell"
point = 11
kind = "phrase_forbidden"
severity = "error"
phrases = ["купи курс", "купить курс", "оплати", "оплатить курс", "стоимость курса", "цена курса", "успей купить"]
message = "прямая продажа курса в лоб запрещена (курс — только «анонс», «готовим»)"
fix = "убрать; вести на клуб/канал, курс упоминать как анонс"

[[rule]]
id = "no-result-guarantee"
point = 12
kind = "regex_forbidden"
severity = "warning"
patterns = ['(?i)гарантир\w+ результат', '(?i)результат гарантир', '(?i)на 100% ', '(?i)точно получится']
message = "односторонние гарантии результата запрещены"
fix = "смягчить: «в кейсе получилось …», без обещаний читателю"

# ── redaction (безопасность публикации) ────────────────────────────
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
