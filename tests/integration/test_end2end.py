from pathlib import Path
from tempfile import TemporaryDirectory


from graphpak.io.serialization.triplets import kng2csv
from graphpak.kraken import KNGConstructor
from graphpak.visualizers.plotting import kng2plot


class TestRuleGer:

    def test_ger_complete_plot(self, sample_text_ger):
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
        # build plot and check for it
        with TemporaryDirectory() as tempdir:
            fpath = Path(tempdir) / "testplot.png"
            kng2plot(
                kng_triples=kng_triples,
                fpath=fpath,
                silent=True,
            )
            assert fpath.exists() == True

    def test_ger_complete_save(self, sample_text_ger):
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
        # build plot and check for it
        with TemporaryDirectory() as tempdir:
            fpath = Path(tempdir) / "testdump.csv"
            kng2csv(
                kng_triples=kng_triples,
                fpath=fpath,
                encoding="utf-8",
            )
            assert fpath.exists() == True
