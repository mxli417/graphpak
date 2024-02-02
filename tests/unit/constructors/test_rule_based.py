from graphpak.kraken import KNGConstructor


class TestRuleGer:

    def test_ger_setup(self):
        ger_kng = KNGConstructor(language="ger", ctype="rule-based")
        assert ger_kng is not None

    def test_ger_complete(self, sample_text_ger):
        ger_kng = KNGConstructor(language="ger", ctype="rule-based")
        assert ger_kng is not None
        # assert ger_kng is not None
        kng_triples = ger_kng(sample_text_ger)
        assert kng_triples is not None
        assert all(
            [el.get("subject") is not None for el in kng_triples]
        ), f"Error: subject must be part of every kng triple"
        assert all(
            [el.get("object") is not None for el in kng_triples]
        ), f"Error: object must be part of every kng triple"
        assert all(
            [el.get("relation") is not None for el in kng_triples]
        ), f"Error: relation must be part of every kng triple"
