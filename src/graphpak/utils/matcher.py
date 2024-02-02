from typing import Dict

from graphpak.constructors import BaseKNGConstructor
from graphpak.constructors.rule_based import RBGermanKNGConstructor

LANG_TYPE_MATCH = {
    ("ger", "rule-based"): RBGermanKNGConstructor(),
    # TODO: add the rest here
}


def lang_constructor_matcher(language: str = "ger", ctype: str = "rulebased") -> BaseKNGConstructor:
    return LANG_TYPE_MATCH[language, ctype]
