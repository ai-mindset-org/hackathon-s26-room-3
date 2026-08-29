"""Модель канона и загрузчик.

Канон — данные, не код. Формат: markdown-документ с одним fenced-блоком
```toml``` (машиночитаемая часть). Если toml-блока нет — включается
best-effort парсер прозаического нумерованного списка (`examples/canon.md`),
чтобы линтер работал прямо на файле приёмки.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# перечень видов правил — контракт с check.py
KINDS = {
    "emoji",                 # эмодзи (регэксп зашит в коде)
    "regex_forbidden",       # совпадение любого из patterns — нарушение
    "stem_forbidden",        # слово, начинающееся с любого stem — нарушение
    "phrase_forbidden",      # буквальная фраза (регистронезависимо)
    "form_forbidden",        # точная словоформа
    "headline_case",         # первый заголовок должен начинаться со строчной (allow: префиксы-исключения)
    "paragraph_max_lines",   # абзац длиннее max строк (param: max)
    "doc_max_chars",         # документ длиннее max знаков (param: max)
    "number_without_source", # число в утверждении без «(источник)» рядом
    "require_present",        # нарушение, если НИ ОДИН pattern не встретился в тексте
    "require_in_lead",        # нарушение, если НИ ОДИН pattern не встретился в первых `within` знаках
    "keyword_min_count",      # keyword встречается меньше `min` раз
    "count_range",            # число совпадений patterns вне диапазона [min, max]
}


@dataclass
class Rule:
    id: str
    point: int                       # номер пункта канона; 0 = вне нумерации (redaction)
    kind: str
    severity: str = "error"          # error | warning
    category: str = "canon"          # canon | redaction
    message: str = ""
    fix: str = ""
    patterns: list[str] = field(default_factory=list)
    stems: list[str] = field(default_factory=list)
    phrases: list[str] = field(default_factory=list)
    forms: list[str] = field(default_factory=list)
    allow: list[str] = field(default_factory=list)   # префиксы-исключения (headline_case)
    max: int | None = None
    min: int | None = None
    within: int | None = None                        # окно «лида» в знаках (require_in_lead)
    keyword: str = ""
    judgment_extends: bool = False   # буквальное ловим здесь, вариации — модуль judge/
    note: str = ""


@dataclass
class Canon:
    meta: dict
    rules: list[Rule]

    def by_point(self) -> dict[int, list[Rule]]:
        out: dict[int, list[Rule]] = {}
        for r in self.rules:
            out.setdefault(r.point, []).append(r)
        return out


_TOML_FENCE = re.compile(r"```toml\s*\n(.*?)\n```", re.DOTALL)


def load_canon(path: str | Path) -> Canon:
    text = Path(path).read_text(encoding="utf-8")
    m = _TOML_FENCE.search(text)
    if m:
        return _from_toml(tomllib.loads(m.group(1)))
    return _from_prose(text)


def _from_toml(data: dict) -> Canon:
    rules = []
    for d in data.get("rule", []):
        if d["kind"] not in KINDS:
            raise ValueError(f"canon: неизвестный kind {d['kind']!r} в правиле {d.get('id')!r}")
        rules.append(Rule(
            id=d["id"], point=int(d.get("point", 0)), kind=d["kind"],
            severity=d.get("severity", "error"), category=d.get("category", "canon"),
            message=d.get("message", ""), fix=d.get("fix", ""),
            patterns=d.get("patterns", []), stems=d.get("stems", []),
            phrases=d.get("phrases", []), forms=d.get("forms", []),
            allow=d.get("allow", []),
            max=d.get("max"), min=d.get("min"), within=d.get("within"),
            keyword=d.get("keyword", ""),
            judgment_extends=d.get("judgment_extends", False),
            note=d.get("note", ""),
        ))
    return Canon(meta=data.get("meta", {}), rules=rules)


# ── прозаический фолбэк: examples/canon.md ────────────────────────────
# best-effort. Пункт распознаётся по номеру строки-абзаца и ключевым
# словам; списки слов берутся из «кавычек-ёлочек».

def _quoted(s: str) -> list[str]:
    return re.findall(r"«([^»]+)»", s)


def _stem(word: str) -> str:
    w = word.strip().lower()
    return w[:-2] if len(w) > 4 else w      # грубое усечение окончания


def _num_before(s: str, word: str) -> int | None:
    m = re.search(r"(\d+)\D*" + word, s)
    return int(m.group(1)) if m else None


def _from_prose(text: str) -> Canon:
    rules: list[Rule] = []
    for line in text.splitlines():
        m = re.match(r"\s*(\d+)\.\s+(.*)", line)
        if not m:
            continue
        n, body = int(m.group(1)), m.group(2)
        low = body.lower()
        if "эмодзи" in low:
            rules.append(Rule(f"p{n}-emoji", n, "emoji",
                              message=f"эмодзи запрещены (п.{n})", fix="убрать эмодзи"))
        elif "строчной" in low or "строчную" in low:
            rules.append(Rule(f"p{n}-headline", n, "headline_case",
                              message=f"заголовок со строчной буквы (п.{n})"))
        elif "антитеза" in low:
            rules.append(Rule(
                f"p{n}-antithesis", n, "regex_forbidden", judgment_extends=True,
                patterns=[r'(?i)\bне\s+(?:просто\s+|только\s+)?[^,.\n]{1,40},\s+а\s+\S',
                          r'(?i)\bэто\s+не\s+[^—\n]{1,50}\s*—\s*это\b'],
                message=f"антитеза «не X, а Y» (п.{n})"))
        elif "запрещённые слова" in low or "запрещенные слова" in low:
            rules.append(Rule(f"p{n}-words", n, "stem_forbidden",
                              stems=[_stem(w) for w in _quoted(body)],
                              message=f"запрещённое слово (п.{n})"))
        elif "≤" in body and ("строк" in low or "знаков" in low):
            pl = _num_before(body, "строк")
            dc = _num_before(body, "знаков")
            if pl:
                rules.append(Rule(f"p{n}-par", n, "paragraph_max_lines", severity="warning",
                                  max=pl, message=f"абзац длиннее {pl} строк (п.{n})"))
            if dc:
                rules.append(Rule(f"p{n}-len", n, "doc_max_chars", severity="warning",
                                  max=dc, message=f"пост длиннее {dc} знаков (п.{n})"))
        elif "источник" in low and "скобк" in low:
            rules.append(Rule(f"p{n}-source", n, "number_without_source",
                              message=f"число без источника в скобках (п.{n})"))
        elif "подписывайтесь" in low:
            rules.append(Rule(f"p{n}-cta", n, "stem_forbidden",
                              stems=["подписывайт", "подпишит", "подписыва"],
                              message=f"CTA «подписывайтесь» запрещён (п.{n})"))
        elif "канцелярит" in low:
            items = [w.strip().lower() for w in _quoted(body) if len(w.strip()) >= 4]
            phrases = [w for w in items if " " in w]
            long_w = [_stem(w) for w in items if " " not in w and len(w) >= 8]
            short_w = [w for w in items if " " not in w and len(w) < 8]  # «данный» и т.п. — точной формой
            if phrases:
                rules.append(Rule(f"p{n}-cler-p", n, "phrase_forbidden",
                                  phrases=phrases, message=f"канцелярит (п.{n})"))
            if long_w:
                rules.append(Rule(f"p{n}-cler-s", n, "stem_forbidden",
                                  stems=long_w, message=f"канцелярит (п.{n})"))
            if short_w:
                rules.append(Rule(f"p{n}-cler-f", n, "form_forbidden",
                                  forms=short_w, message=f"канцелярит (п.{n})"))
    return Canon(meta={"source": "prose"}, rules=rules)
