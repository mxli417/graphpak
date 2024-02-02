from pathlib import Path

from graphpak.io.input.pdf import load_pdf


class TestRuleGer:

    def test_ger_setup(self, test_assets_path):
        pdf_test_asset = Path(test_assets_path) / "hello_world.pdf"
        loaded_text = load_pdf(pdf_test_asset)
        assert loaded_text is not None
