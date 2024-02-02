import logging
from typing import Dict, List

import spacy

from graphpak.utils.matcher import lang_constructor_matcher


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


class KNGConstructor:

    def __init__(self, language: str = "ger", ctype: str = "rule-based", model: str = ""):
        self.lang = language
        self.ctype = ctype
        self.constructor = lang_constructor_matcher(language, ctype)
        assert (
            self.constructor is not None
        ), f"Cannot retrieve constructor for language: {language} and constructor type: {ctype}"

    def __call__(self, target_text: str) -> List[Dict]:
        # build the KG - sentence by sentence
        kng_triples = []
        nlp = spacy.load(self.constructor.nlp_model)
        doc = nlp(target_text)
        for sent in doc.sents:
            sentdoc = nlp(sent.text)
            sent_triples = self.constructor(doc=sentdoc.text)
            kng_triples += sent_triples

        return kng_triples
