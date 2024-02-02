from abc import ABC
from typing import Any, Dict, List


class BaseKNGConstructor(ABC):
    """Base class of rule-based or model-based kng constructors returning triples"""

    def __init__(self, *args: Any, **kwds: Any) -> None:
        pass

    def build_kng(self, doc: str) -> List[Dict]:
        raise NotImplementedError

    def __call__(self, doc: str, *args: Any, **kwds: Any) -> Any:
        kng_triples = self.build_kng(doc=doc)
        return kng_triples
