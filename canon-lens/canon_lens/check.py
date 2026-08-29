"""Детерминированная проверка текста против канона.

Каждое нарушение — запись с точным местом (строка, колонка, абсолютный
сдвиг), цитатой, номером пункта канона и подсказкой правки. Правила с
`judgment_extends` ловятся здесь только в буквальной форме — вариации
добирает модуль `judge/` в той же форме записи.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict

from .rules import Canon, Rule

# эмодзи: пиктограммы, символы, флаги, дингбаты, вариационные селекторы
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"      # symbols & pictographs, supplemental, extended-A
    "\U0001F000-\U0001F0FF"      # mahjong / dominoes / cards
    "\U0001F1E6-\U0001F1FF"      # regional indicators (флаги)
    "\U00002600-\U000027BF"      # misc symbols + dingbats
    "\U00002B00-\U00002BFF"      # misc symbols and arrows
    "\U0000FE00-\U0000FE0F"      # variation selectors
    "\U00002190-\U000021FF"      # arrows
    "\U00002300-\U000023FF"      # technical (⌚ ⏰ …)
    "]"
)


@dataclass
class Violation:
    rule: str            # id правила канона
    point: int           # пункт канона (0 = redaction)
    category: str         # canon | redaction
    severity: str         # error | warning
    kind: str             # mechanical | redaction | judgment-literal
    line: int             # 1-based
    col: int              # 1-based
    end_col: int
    offset: list[int]     # [start, end) абсолютный сдвиг в тексте
    quote: str
    message: str
    fix: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


def check_text(text: str, canon: Canon) -> list[Violation]:
    out: list[Violation] = []
    for rule in canon.rules:
        out.extend(_check_rule(text, rule))
    out.sort(key=lambda v: (v.offset[0], v.offset[1], v.point, v.rule))
    seen: set[tuple] = set()                       # один stem-набор правила может дать
    uniq: list[Violation] = []                     # одно и то же место дважды — дедуп
    for v in out:
        key = (v.rule, v.offset[0], v.offset[1])
        if key not in seen:
            seen.add(key)
            uniq.append(v)
    return uniq


def summary(violations: list[Violation]) -> dict:
    errs = sum(1 for v in violations if v.severity == "error")
    return {
        "total": len(violations),
        "errors": errs,
        "warnings": len(violations) - errs,
        "points": sorted({v.point for v in violations}),
        "clean": errs == 0,
    }


# ── внутреннее ───────────────────────────────────────────────────────

def _line_col(text: str, pos: int) -> tuple[int, int]:
    head = text[:pos]
    return head.count("\n") + 1, pos - (head.rfind("\n") + 1) + 1


def _mk(text: str, rule: Rule, start: int, end: int, quote: str,
        kind: str = "mechanical") -> Violation:
    line, col = _line_col(text, start)
    if rule.category == "redaction":
        kind = "redaction"
    elif rule.judgment_extends:
        kind = "judgment-literal"
    q = quote.strip() or quote
    return Violation(
        rule=rule.id, point=rule.point, category=rule.category, severity=rule.severity,
        kind=kind, line=line, col=col, end_col=col + (end - start),
        offset=[start, end], quote=q, message=rule.message, fix=rule.fix,
    )


def _check_rule(text: str, rule: Rule) -> list[Violation]:
    fn = _DISPATCH.get(rule.kind)
    return fn(text, rule) if fn else []


def _k_emoji(text, rule):
    return [_mk(text, rule, m.start(), m.end(), m.group(0)) for m in EMOJI_RE.finditer(text)]


def _k_regex(text, rule):
    res = []
    for pat in rule.patterns:
        for m in re.compile(pat).finditer(text):
            res.append(_mk(text, rule, m.start(), m.end(), m.group(0)))
    return res


def _k_stem(text, rule):
    res = []
    for stem in rule.stems:
        rx = re.compile(r"\b" + re.escape(stem) + r"[а-яёА-ЯЁa-zA-Z]*", re.IGNORECASE)
        for m in rx.finditer(text):
            res.append(_mk(text, rule, m.start(), m.end(), m.group(0)))
    return res


def _k_phrase(text, rule):
    res = []
    for ph in rule.phrases:
        for m in re.finditer(re.escape(ph), text, re.IGNORECASE):
            res.append(_mk(text, rule, m.start(), m.end(), m.group(0)))
    return res


def _k_form(text, rule):
    res = []
    for form in rule.forms:
        for m in re.finditer(r"\b" + re.escape(form) + r"\b", text, re.IGNORECASE):
            res.append(_mk(text, rule, m.start(), m.end(), m.group(0)))
    return res


def _k_headline(text, rule):
    # только первый markdown-заголовок; правило «со строчной буквы»
    m = re.search(r"(?m)^#{1,6}[ \t]+(\S.*?)[ \t]*$", text)
    if not m:
        return []
    title = m.group(1)
    first_alpha = next((c for c in title if c.isalpha()), "")
    if first_alpha and first_alpha == first_alpha.upper():
        s = m.start(1)
        return [_mk(text, rule, s, s + len(title), title)]
    return []


def _k_par_lines(text, rule):
    res, pos = [], 0
    for chunk in re.split(r"(\n[ \t]*\n)", text):     # разделители сохранены → сдвиги точные
        body = chunk.strip("\n")
        if body.strip():                             # не разделитель и не пусто
            n = body.count("\n") + 1
            if rule.max and n > rule.max:
                q = (body[:57] + "…") if len(body) > 60 else body
                res.append(_mk(text, rule, pos, pos + len(chunk), q))
        pos += len(chunk)
    return res


def _k_doc_chars(text, rule):
    n = len(text)
    if rule.max and n > rule.max:
        v = _mk(text, rule, 0, n, f"{n} знаков")
        v.message = f"{rule.message}: {n} > {rule.max}"
        return [v]
    return []


_NUM_RE = re.compile(r"(?<![\w.])\d[\d.,]*%?")
_PAREN_RE = re.compile(r"\([^)]{2,}\)")


def _k_number(text, rule):
    res = []
    for m in _NUM_RE.finditer(text):
        num = m.group(0).rstrip(".,")
        if not num or re.fullmatch(r"\d{4}", num):      # год — пропускаем
            continue
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        line_end = len(text) if line_end < 0 else line_end
        if _PAREN_RE.search(text[line_start:line_end]):  # источник в той же строке
            continue
        res.append(_mk(text, rule, m.start(), m.start() + len(num), num))
    return res


_DISPATCH = {
    "emoji": _k_emoji,
    "regex_forbidden": _k_regex,
    "stem_forbidden": _k_stem,
    "phrase_forbidden": _k_phrase,
    "form_forbidden": _k_form,
    "headline_case": _k_headline,
    "paragraph_max_lines": _k_par_lines,
    "doc_max_chars": _k_doc_chars,
    "number_without_source": _k_number,
}
