from pathlib import Path
from typing import Dict, List, Union

import pandas as pd


def kng2csv(kng_triples: List[Dict], fpath: Union[str, Path], encoding: str = "utf-8") -> None:
    """Stores a list of kng triples in a csv file with columns
    suitable for direct re-use the networkx library

    Args:
        kng_triples (List[Dict]): kng-stryle triples defined as dict per item
            in list holding the keys subject, object and relation
        fpath (str): target path for the file to be stored on HDD
        encoding (str, optional): encoding format str. Defaults to "utf-8".
    """
    target_path = Path(fpath)
    assert all(
        [el.get("subject") is not None for el in kng_triples]
    ), f"Error: subject must be part of every kng triple"
    assert all([el.get("object") is not None for el in kng_triples]), f"Error: object must be part of every kng triple"
    assert all(
        [el.get("relation") is not None for el in kng_triples]
    ), f"Error: relation must be part of every kng triple"

    # build nx - suitable dataframe
    source, target, edge = (
        [el["subject"] for el in kng_triples],
        [el["object"] for el in kng_triples],
        [el["relation"] for el in kng_triples],
    )
    kng_df = pd.DataFrame({"source": source, "target": target, "edge": edge})
    kng_df.to_csv(target_path, encoding=encoding)
