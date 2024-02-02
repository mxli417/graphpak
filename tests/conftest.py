from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_assets_path() -> Path:
    fpath = Path(__file__).parent.resolve()
    return fpath / "assets"


@pytest.fixture(scope="session")
def sample_text_ger() -> str:
    # provides a german test text snippet from a public newspaper article
    text = """
    Wenn in Bayern und dann sogar noch in München etwas nicht klappt, 
    sprechen Politiker, bevorzugt solche aus der CSU, gerne von "Berliner 
    Verhältnissen". So zum Beispiel Hans Theiss, der stellvertretende 
    CSU-Fraktionsvorsitzende im Stadtrat. Fünf Tage nach dem heftigsten 
    Schneefall seit vielen Jahren ist der Straßenbahnverkehr noch immer 
    nicht wieder komplett angelaufen. Nur nach und nach gehen die Linien 
    an den Start. Das geht so langsam, weil die Mitarbeiter der Münchner
    Verkehrsgesellschaft (MVG) per Hand die vereisten Rillengleise freikratzen 
    müssen und sich dabei Meter für Meter vorarbeiten. Einen Räum-Unimog hat die 
    MVG im Einsatz, für Verstärkung sorgt aktuell auch ein ähnliches Fahrzeug 
    aus Stuttgart.
    """
    return text
