import logging
from typing import Dict, List

import networkx as nx
import spacy

from graphpak.constructors import BaseKNGConstructor


class RBGermanKNGConstructor(BaseKNGConstructor):
    """Rule Based KNG-triple constructor relying mainly on spacy and heuristics
    to build KNG-style triples from German text input. Will be reworked soon.
    """

    def __init__(self, spacy_model: str = "de_core_news_sm") -> None:
        super().__init__()
        self.nlp_model = spacy_model

    @staticmethod
    def ger_filter_or_select(shortest_path_elements: List[str], sentence_elements: List[str]) -> List[str]:
        """Filtering algorithm for shortest path elements lying between
        the sentence subject and sentence object. Tries to filter out
        irrelevant, non-verb words and returns a list of strs defining
        the relation. Unsupervised, only partially linguistically founded,
        motivated by heuristics and hence messy.

        Args:
            shortest_path_elements (List[str]): list of sentence elements on
                the shortest path between a subject and object
            sentence_elements (List[str]): complete list of sentence elements
                with all token information

        Returns:
            List[str]: list of strs defining the relation
        """
        middle_elements = shortest_path_elements[1:-1]
        clean_middle_els = []
        # recover the elements from the sentparse
        element_ids = [int(el.split("-")[-1]) for el in middle_elements]
        for idx, el_id in enumerate(element_ids):
            token_info = sentence_elements[int(el_id)]
            # filter all elements not ROOT or VERB or ADVERB
            if token_info["tokdep"] in ["ROOT", "mo", "oc"] and token_info["tokpos"] in [
                "VERB",
                "AUX",
            ]:
                clean_middle_els.append(middle_elements[idx].split("-")[0])
            else:
                logging.debug(f"filtered out: {token_info}")
        # TODO: check if clean middle eles is empty and decide what else to do
        if len(clean_middle_els) == 0:
            logging.debug(f"dropped out: {clean_middle_els} relation elements")
        return clean_middle_els

    def ger_get_entrel(self, sentence: str) -> List[Dict]:
        """
        We need the possible sentence subjects, the possible objects and the
        dependency - parse - graph shortest path between them. Then we decide
        which elements to keep on every shortest path between subject and
        object. Then, we return subject - verb - object triples.

        Args:
            sentence (str): input sentence string from a document
            model (str, optional): spacy language-specific model providing all
            functionality for parsing and tagging. Defaults to 'de_core_news_sm'.

        Returns:
            List[dict]: List of kng-like triples containing
            subject-relation-object triples
        """
        nlp = spacy.load(self.nlp_model)
        sentparse = []

        # parse sentence
        sentdoc = nlp(sentence)

        sent_subjects = []
        sent_objects = []

        for token in sentdoc:
            # check for objects in sent
            if str(token.dep_) in ["oa", "oc", "op", "nk", "cj"] and str(token.pos_) in [
                "NOUN",
                "PROPN",
            ]:
                sent_objects.append(
                    {
                        "tokenid": token.i,
                        "tokentxt": token.text,
                    }
                )

            # check for subjects in sentW
            if str(token.dep_) in ["sb", "pnc"] and str(token.pos_) in [
                "NOUN",
                "PROPN",
            ]:
                sent_subjects.append(
                    {
                        "tokenid": token.i,
                        "tokentxt": token.text,
                    }
                )

            sentparse.append(
                {
                    "tokenid": token.i,
                    "tokdep": token.dep_,
                    "tokpos": token.pos_,
                    "toktag": token.tag_,
                    "toktxt": token.text,
                    "tokhed": token.head.text,
                    "tokchd": [el for el in token.children],
                    "tokhdc": [el for el in token.head.children],
                    "tokent": token.ent_type_,
                }
            )

        # load the dependencies as a graph into networkx
        edges = []
        for token in sentdoc:
            # token api lookup - https://spacy.io/docs/api/token
            for child in token.children:
                edges.append(
                    (
                        "{0}-{1}".format(token.lower_, token.i),
                        "{0}-{1}".format(child.lower_, child.i),
                    )
                )
        graph = nx.Graph(edges)

        # for every subject, get the shortest dep path to the objects
        sentence_sps = []
        for subj in sent_subjects:
            for obj in sent_objects:
                sp = nx.shortest_path(
                    graph,
                    source=f"{str(subj['tokentxt']).lower()}-{subj['tokenid']}",
                    target=f"{str(obj['tokentxt']).lower()}-{obj['tokenid']}",
                )
                logging.debug(f"SP: {subj['tokentxt']}{sp}{obj['tokentxt']}")
                sentence_sps.append(sp)

        sentence_triples = []
        for sentsps in sentence_sps:
            if len(sentsps) == 3:
                sent_triple = {
                    "subject": sentsps[0].split("-")[0],
                    "relation": "-".join(sentsps[1].split("-")[:-1]),
                    "object": "".join(sentsps[2].split("-")[:-1]),
                }
            else:
                clean_middle_eles = self.ger_filter_or_select(sentsps, sentparse)
                # collect the triples one by one
                sent_triple = {
                    "subject": sentsps[0].split("-")[0],
                    "relation": "-".join(clean_middle_eles),
                    "object": "".join([el for el in sentsps[-1].split("-")[:-1]]),
                }
            # check if sentence triple contains empty relation
            if (
                len(sent_triple["subject"].replace(" ", "")) > 0
                and len(sent_triple["relation"].replace(" ", "")) > 0
                and len(sent_triple["object"].replace(" ", ""))
            ):
                sentence_triples.append(sent_triple)
            elif (
                len(sent_triple["subject"].replace(" ", "")) > 0
                and len(sent_triple["relation"].replace(" ", "")) == 0
                and len(sent_triple["object"].replace(" ", ""))
            ):
                sent_triple["relation"] = "--binds--"
                sentence_triples.append(sent_triple)
            else:
                logging.debug(f"Filtered out triple: {sent_triple}")
        return sentence_triples

    def build_kng(self, doc: str) -> List[Dict]:
        """Main method to build the kng-triples from the input text document

        Args:
            doc (str): input text document

        Returns:
            List[Dict]: KNG-style triples holding the triples from the input
                text document. Each triple contains a `subject`, `relation` and
                an `object`
        """
        kng_triples = self.ger_get_entrel(sentence=doc)
        return kng_triples
