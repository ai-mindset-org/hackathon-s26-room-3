"""Сборка сценария рилза из facts.json и canon.md.

Модель не вызывается: сборка детерминированная, из фактов и шаблона. Смысл в
том, что сборщик физически не может добавить число или утверждение, которого
нет в facts.json, — а это ключевая проверка приёмочного примера 02-рилз.
"""

import json
import re

from . import lens

PAIN = ("теря", "пропада", "не найти", "вручную", "рутин", "тратил", "тратит",
        "уходит", "забыт", "не понима", "барьер", "ошиб", "долго", "недел")
USABLE = ("number", "claim", "action", "quote")
MIN_FACTS = 2
FALLBACK_CTA = "возьмите один процесс из своей недели и опишите его словами"


class Refusal(Exception):
    """Штатный отказ: сценарий не собирается, причина уходит в отчёт."""


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _pain_score(fact):
    text = fact.get("text", "").lower()
    return sum(1 for marker in PAIN if marker in text)


def pick(facts):
    """Хук, 2-3 факта в суть, действие для CTA."""
    usable = [f for f in facts if f.get("kind") in USABLE]
    if len(usable) < MIN_FACTS:
        raise Refusal(
            f"в сырье {len(usable)} пригодных фактов, нужно минимум {MIN_FACTS}")

    actions = [f for f in usable if f.get("kind") == "action"]
    rest = [f for f in usable if f not in actions]

    hook = max(rest, key=_pain_score) if rest else usable[0]
    if _pain_score(hook) == 0:
        numbers = [f for f in rest if f.get("kind") == "number"]
        hook = numbers[0] if numbers else rest[0]

    body = [f for f in rest if f["id"] != hook["id"]]
    body.sort(key=lambda f: (f.get("kind") != "number", f["id"]))
    body = body[:3]
    if not body:
        raise Refusal("после выбора хука не осталось фактов для сути")

    return hook, body, (actions[0] if actions else None)


def _with_source(line, source_id, need_source):
    if need_source and re.search(r"\d", line) and not re.search(r"\([^)]*\)", line):
        return f"{line} ({source_id})"
    return line


def render(data, canon):
    facts = data.get("facts", [])
    source = data.get("source", {})
    source_id = source.get("id", "источник")
    hook, body, action = pick(facts)

    # заголовок начинается со слова «сценарий», поэтому строчная буква по п.2
    # обеспечена и без порчи имён собственных внутри названия статьи
    title = (source.get("title") or "рилз").strip()

    lines = [f"# сценарий: {title}", ""]
    lines += ["## хук (0–3 с)", "",
              _with_source(hook["text"].rstrip("."), source_id, lens.needs_number_source(canon)) + ".",
              ""]
    lines += ["## суть (3–22 с)", ""]
    for fact in body:
        lines.append("- " + _with_source(fact["text"].rstrip("."), source_id,
                                         lens.needs_number_source(canon)) + ".")
    lines += ["", "## cta (22–30 с)", ""]
    cta = action["text"].rstrip(".") if action else FALLBACK_CTA
    lines += [cta + ".", ""]
    used = [hook["id"]] + [f["id"] for f in body] + ([action["id"]] if action else [])
    lines += ["## использованные факты", "", ", ".join(used), ""]

    script = "\n".join(lines)
    return script, used, (action is None)


USED_SECTION = re.compile(r"\n## использованные факты.*", re.S)


def spoken(script, source_id=""):
    """Только произносимый текст: без заголовков с тайм-кодами, без списка
    id фактов и без служебной пометки источника. На нём и меряется, не
    добавил ли сборщик числа от себя."""
    text = USED_SECTION.sub("", script)
    text = "\n".join(l for l in text.split("\n") if not l.startswith("#"))
    if source_id:
        text = text.replace(f"({source_id})", "")
    return text


def outside_source(script, facts, source_id=""):
    """Числа в сценарии, которых нет ни в одном факте."""
    haystack = " ".join(
        (f.get("text", "") + " " + str(f.get("value") or "") + " " + f.get("quote", ""))
        for f in facts)
    known = set(re.findall(r"\d+", haystack))
    return [n for n in re.findall(r"\d+", spoken(script, source_id)) if n not in known]


def source_violations(facts, canon):
    """Нарушения канона в исходнике — по дословным цитатам фактов."""
    quotes = "\n\n".join(f.get("quote", "") for f in facts if f.get("quote"))
    return lens.check(quotes, canon, document_level=False)


def report(data, canon, script=None, used=None, refusal=None, template_cta=False):
    facts = data.get("facts", [])
    source_id = data.get("source", {}).get("id", "")
    out = ["# отчёт", ""]

    out += ["## нарушения канона в исходнике", ""]
    src = source_violations(facts, canon)
    if src:
        for i, v in enumerate(src, 1):
            out.append(f"{i}. п.{v.point} {v.message} — «{v.quote}»")
    else:
        out.append("нет")
    out.append("")

    out += ["## факты вне источника", ""]
    stray = outside_source(script, facts, source_id) if script else []
    out.append("нет" if not stray else "числа, которых нет в фактах: " + ", ".join(stray))
    out.append("")

    if script is not None:
        out += ["## самопроверка сценария", ""]
        own = lens.check(USED_SECTION.sub("", script), canon)
        if own:
            for v in own:
                out.append(f"- п.{v.point} {v.message} — «{v.quote}»")
        else:
            out.append(f"канон пройден, {len(used)} фактов использовано")
        out.append(f"- движок канона: {lens.ENGINE}")
        if template_cta:
            out.append("- CTA шаблонный: в сырье нет факта с kind=action")
        out.append("")

    if lens.unparsed(canon):
        out += ["## пункты канона, которые парсер не понял", ""]
        for num, item in lens.unparsed(canon):
            out.append(f"- п.{num}: {item[:90]}")
        out.append("")

    out += ["## решение", ""]
    out.append("годится" if script is not None else f"контента нет — {refusal}")
    out.append("")
    return "\n".join(out)
