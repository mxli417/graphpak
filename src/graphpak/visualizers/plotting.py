from pathlib import Path
from typing import Dict, List, Union

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def kng2plot(kng_triples: List[Dict], fpath: Union[str, Path, None], silent: bool = False) -> None:
    assert all(
        [el.get("subject") is not None for el in kng_triples]
    ), f"Error: subject must be part of every kng triple"
    assert all([el.get("object") is not None for el in kng_triples]), f"Error: object must be part of every kng triple"
    assert all(
        [el.get("relation") is not None for el in kng_triples]
    ), f"Error: relation must be part of every kng triple"

    # build nx-suitable dataframe
    source, target, edge = (
        [el["subject"] for el in kng_triples],
        [el["object"] for el in kng_triples],
        [el["relation"] for el in kng_triples],
    )

    kng_df = pd.DataFrame({"source": source, "target": target, "edge": edge})

    # build and display kg-graph
    kg_graph = nx.from_pandas_edgelist(
        kng_df,
        "source",
        "target",
        edge_attr="edge",
        create_using=nx.MultiDiGraph(),
        edge_key="edge",
    )
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(kg_graph, k=0.5)
    nx.draw(
        kg_graph,
        with_labels=True,
        node_color="pink",
        edge_cmap=plt.cm.Blues,
        pos=pos,
        edge_color="black",
        width=1,
        alpha=0.9,
    )
    nx.draw_networkx_edge_labels(
        kg_graph,
        pos=pos,
        edge_labels={(u, v): d["edge"] for u, v, d in kg_graph.edges(data=True)},
        font_color="red",
    )
    # check if we have to store the plot to hdd
    if fpath is not None:
        target_path = Path(fpath)
        plt.savefig(target_path, bbox_inches="tight")
    # check if we have to display the plot
    if silent == False:
        plt.show()
