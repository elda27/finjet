from typing import NamedTuple, Callable, Any


class Dependency(NamedTuple):
    klass_or_func: Callable[[Any], Any]
    is_singleton: bool = False


def Depends(klass_or_func=None) -> Dependency:
    return Dependency(klass_or_func)


def Singleton(klass_or_func) -> Dependency:
    return Dependency(klass_or_func, True)


def get_indentification(dep: Dependency) -> str:
    return '.'.join([
        dep.klass_or_func.__module__,
        dep.klass_or_func.__name__
    ])
