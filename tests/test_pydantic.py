from typing import NamedTuple
from finjet.dependency import Depends
from pydantic import BaseModel
import pytest
import finjet


def test_pydantic_fully_injection_from_config():
    class Configuration(NamedTuple):
        positional_arg: int
        source: int = 10
        dest: int = 20

    @finjet.inject
    class A(BaseModel):
        positional_arg: int = finjet.Depends()
        source: int = finjet.Depends()

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = A()
        assert x.positional_arg == config.positional_arg
        assert x.source == config.source


def test_pydantic_injection_from_function():
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

    @finjet.inject
    class A(BaseModel):
        test_val: int = finjet.Depends(test)
        c: int = finjet.Depends(test_c)

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = A()
        assert x.test_val == test()
        assert x.c == test_c(test_b())


def test_pydantic_injection_from_class():
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

    @finjet.inject
    class A(BaseModel):
        test_val: int = finjet.Depends(test)
        c: int = finjet.Depends(test_c)

    container = finjet.Container()
    config = Configuration(200)
    container.configure(config)
    with container:
        x = A()
        assert x.test_val == test()
        assert x.c == test_c(B(10))


if __name__ == '__main__':
    pytest.main(__file__)
