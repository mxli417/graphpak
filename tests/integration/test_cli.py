from typer.testing import CliRunner
from graphpak.cli.main_cli import app

runner = CliRunner()


class TestCLIfunctions:

    def test_main_cli(self, sample_text_ger):
        result = runner.invoke(app, ["--text", f"{sample_text_ger}"])
        assert result.exit_code == 1
