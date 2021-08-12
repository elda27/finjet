from finjet.functional import get_global_container, set_global_container, inject
from finjet.dependency import Dependency, Depends, Singleton
from finjet.container import Container

__version__ = '0.1.2'
__all__ = [
    get_global_container,
    set_global_container,
    inject,
    Dependency,
    Depends,
    Singleton,
    Container
]
