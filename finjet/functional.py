
from functools import wraps
from typing import Optional, TypeVar
from finjet.container import Container


def get_global_container() -> Optional[Container]:
    """get global container object

    Returns
    -------
    Optional[Container]
        Container object
    """
    if Container.current is None:
        Container.current = Container()
    return Container.current


T = TypeVar('T')


def inject(func: T) -> T:
    """Decorator function of dependency injection.

    Parameters
    ----------
    func : T
        Any function or class.

    Returns
    -------
    T
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
