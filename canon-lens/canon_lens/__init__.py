"""canon-lens — детерминированная проверка текста против канона.

API:
    from canon_lens import load_canon, check_text
    vs = check_text(text, load_canon("canon.md"))
"""
from .rules import Canon, Rule, load_canon
from .check import Violation, check_text

__all__ = ["Canon", "Rule", "load_canon", "Violation", "check_text"]
