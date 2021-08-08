
from functools import wraps
from typing import Any, Callable, Optional, TypeVar
from finjet.container import Container


def get_global_container() -> Optional[Container]:
    """get global container object

    Returns
    -------
    Optional[Container]
        Container object
    """
    return Container.current


T = TypeVar('T')


def inject(func: T) -> T:
    """Decorator function of dependency injection.

    Parameters
    ----------
    func : Callable[[Any], Any]
        Any function or class.

    Returns
    -------
    Callable[[Any], Any]
        func
    """
    @wraps(func)
    def _(*args, **kwargs):
        container = get_global_container()
        if container is not None:
            return container.inject(func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return _
