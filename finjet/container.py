from functools import wraps
from finjet.dependency import Dependency, get_indentification
from finjet.injecter import InjecterBase, Notset, create_injecter
from typing import Any, Callable, NamedTuple, Optional, Type


class Container:
    current: "Container" = None

    def __init__(self) -> None:
        """Container object contains attributes and injecting attributes.
        """
        self.last_current = None
        self.singletons = {}
        self.configuration = None

    def configure(self, configuration: NamedTuple):
        """Configure container object

        Parameters
        ----------
        configuration : NamedTuple
            Solving named dependency from this variable
        """
        self.configuration = configuration
        self.current = self

    def __enter__(self):
        """Set global containers to this container.
        """
        self.last_current = self.__class__.current
        self.__class__.current = self

    def __exit__(self, *args, **kwargs):
        self.__class__.current = self.last_current

    def inject(self, obj: type) -> Callable[[Any], Any]:
        """Injecting dependecies to arguments of input object. 

        Parameters
        ----------
        obj : type
            target object

        Returns
        -------
        Callable[[Any], Any]
            Injection result
        """
        injecter = create_injecter(obj)
        inject_fields = {}
        for name, value in injecter.iter_field():
            if isinstance(value, Dependency):
                if hasattr(self.configuration, name):
                    inject_fields[name] = getattr(self.configuration, name)
                else:
                    inject_fields[name] = self.solve_dependency(
                        value
                    )
            else:
                inject_fields[name] = value

        @wraps(obj)
        def _(*args, **kwargs):
            return obj(*args, **inject_fields, **kwargs)
        return _

    def solve_dependency(self, value: Dependency) -> Any:
        """Solve hierarchy of depedencies.

        Parameters
        ----------
        value : Dependency
            value
        _depth : str
            unique identification for singleton object.

        Returns
        -------
        Any
            Solved value
        """
        if value.is_singleton:  # If singleton object, check cache.
            cache = self.solve_singleton_cache(value)
            if cache is not None:
                return cache

        # Solve dependency
        injecter = create_injecter(value.klass_or_func)

        def _solve_dependency(key: str, value: Any) -> Any:
            if isinstance(value, Dependency):
                return self.solve_dependency(value)
            elif callable(value):
                return value()
            elif hasattr(self.configuration, key):
                return getattr(self.configuration, key)
            else:
                return value

        # Check positional args from config
        positional_args = []
        keyword_args = {}
        for field_name, field_value in injecter.iter_field():
            if field_value is None:
                positional_args.append(
                    _solve_dependency(field_name, field_value)
                )
            elif field_value is Notset:
                pass
            else:
                keyword_args[field_name] = _solve_dependency(
                    field_name, field_value
                )

        result = value.klass_or_func(*positional_args, **keyword_args)
        if value.is_singleton:
            self.add_singleton(
                value,
                result
            )
        return result

    def solve_singleton_cache(self, dependency: Dependency) -> Optional[Any]:
        """Get singleton cache if exists

        Parameters
        ----------
        dependency : Dependency
            depedency object

        Returns
        -------
        Optional[Any]
            singleton object
        """
        return self.singletons.get(
            get_indentification(dependency)
        )

    def add_singleton(self, dependency: Dependency, result: Any):
        """Add singleton object"""
        self.singletons[
            get_indentification(dependency)
        ] = result
