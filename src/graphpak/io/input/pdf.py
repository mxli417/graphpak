import logging
from pathlib import Path
from typing import Union

import fitz
from unidecode import unidecode


def load_pdf(filename: Union[str, Path]) -> Union[str, None]:
    """Tries to load all available text from a given PDF file

    Args:
        filename (Union[str, Path]): path to a machine-readable PDF file

    Returns:
        Union[str, None]: returns a large string containing the available text
            contents from the given PDF file, `None` otherwise
    """
    docpath = Path(filename)
    page_texts = []
    try:
        doc = fitz.open(docpath)
    except IOError as excep:
        logging.error(f"Could not open PDF: {docpath}, error: {excep}")
    else:
        for page in doc:
            page_texts += unidecode(page.get_text())
    return " ".join(page_texts) if len(page_texts) > 0 else None
