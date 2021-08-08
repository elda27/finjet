from typing import Any, List


def get_attr_recurse(obj: Any, attrs: List[str]) -> Any:
    for attr in attrs:
        obj = getattr(obj, attr)
