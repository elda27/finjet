from finjet.dependency import Depends, Singleton
from typing import NamedTuple
import pytest
import finjet


def test_fully_injection_from_config():
    class Configuration(NamedTuple):
        positional_arg: int
        source: int = 10
        dest: int = 20

    @finjet.inject
    def func(
        positional_arg: int = finjet.Depends(),
        source: int = finjet.Depends()
    ):
        return positional_arg + source

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = func()
        assert x == (config.positional_arg + config.source)


def test_injection_from_function():
    class Configuration(NamedTuple):
        positional_arg: int
        source: int = 10
        dest: int = 20

    def test():
        return 10

    def test_b():
        return 20

    def test_c(test=Depends(test_b)):
        return test + 30

    @ finjet.inject
    def func(
        test_val: int = finjet.Depends(test),
        c: int = finjet.Depends(test_c)
    ):
        return test_val + c

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = func()
        assert x == 60


def test_injection_from_class():
    class Configuration(NamedTuple):
        positional_arg: int
        source: int = 10
        dest: int = 20

    def test():
        return 10

    class B:
        def __init__(self, a=Depends(test)) -> None:
            self.a = a

    def test_c(test: B = Depends(B)):
        return test.a + 30

    @ finjet.inject
    def func(
        positional_arg: int = Depends(),
        source: int = Depends(),
        test_val: int = finjet.Depends(test),
        c: int = finjet.Depends(test_c)
    ):
        return positional_arg + source + test_val + c
    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = func()
        assert x == 260


def test_singleton_injection():
    class Configuration(NamedTuple):
        positional_arg: int
        source: int = 10
        dest: int = 20

    def test():
        return 10

    class B:
        value = 0

        def __init__(self, a=Depends(test)) -> None:
            B.value += 10
            self.a = a + B.value

    @finjet.inject
    def test_c(test: B = Singleton(B)):
        return test.a

    @finjet.inject
    def test_d(test: B = Singleton(B)):
        return test.a

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        assert test_c() == test_d()


if __name__ == '__main__':
    pytest.main(__file__)
