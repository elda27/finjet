
from functools import wraps
from typing import Any, Callable, Optional, TypeVar
from finjet.container import Container


def set_global_container(container: Container) -> None:
    """Set global container object

    Returns
    -------
    Optional[Container]
        Container object
    """
    Container.current = container


def get_global_container() -> Container:
    """get global container object

    Returns
    -------
    Container
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
