import pytest
from typing import NamedTuple
from finjet import Container, Depends, Singleton, inject


def test_example():
    class Config(NamedTuple):
        gear_ratio: int
        tire_r: int

    class Engine:
        def __init__(self, gear_ratio: int = Depends()) -> None:
            self.rpm = 40000
            self.gear_ratio = gear_ratio

    class Tire:
        def __init__(self, tire_r: int = Depends()) -> None:
            self.tire_r = tire_r

    @inject
    class Car:
        def __init__(
            self,
            tire: Tire = Depends(Tire),
            engine: Engine = Singleton(Engine)
        ) -> None:
            self.speed = tire.tire_r * engine.gear_ratio * engine.rpm

        def drive(self) -> None:
            print(self.speed)

    container = Container()
    container.configure(Config(100, 5))
    with container:
        car = Car()
        car.drive()


if __name__ == '__main__':
    pytest.main(__file__)
