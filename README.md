# finjet

Simple dependency injection library like fastapi.
It can be used to turn your modules to loosely coupled parts. and configurations to allow you to easily re-use and test your code.

Dependency injection is performed on the arguments given with the `Depends` function as the default argument.
The inserted values will be values of the variable given by `Container.configure` and the return value of the function.

# Installation

Latest PyPI stable release

```
pip install finjet
```

# Example

```python
from typing import NamedTuple
from finjet import Container, Depends, inject


class Config(NamedTuple):
    gear_ratio: int


class Engine:
    def __init__(self, gear_ratio: int = Depends()) -> None:
        self.rpm = 40000
        self.gear_ratio = gear_ratio


class Tire:
    def __init__(self) -> None:
        self.tire_r = 100


def get_rotation_speed(engine: Engine = Depends(Engine)) -> int:
    return engine.gear_ratio


@inject
def get_tire_speed(
    tire: Tire = Depends(Tire),
    rpm: int = Depends(get_rotation_speed)
) -> float:
    return tire.tire_r * rpm


def main():
    container = Container()
    container.configure(Config(100))
    with container:
        print(get_tire_speed())


if __name__ == '__main__':
    main()

```
