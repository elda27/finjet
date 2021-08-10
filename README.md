# finjet

[![codecov](https://codecov.io/gh/elda27/finjet/branch/master/graph/badge.svg?token=Lnx3ZA0VKg)](https://codecov.io/gh/elda27/finjet)
[![PyPI version](https://badge.fury.io/py/finjet.svg)](https://badge.fury.io/py/finjet)

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
from finjet import Container, Depends, Singleton, inject


class Config(NamedTuple):
    gear_ratio: int
    tire_r: int = 100


class Engine:
    # gear_ratio will be obtained from `Config`
    def __init__(self, gear_ratio: int = Depends()) -> None:
        self.gear_ratio = gear_ratio


class Tire:
    count = 0

    def __init__(self, tire_r: int = Depends()) -> None:
        Tire.count += 1
        # Actually tire_r is multiplied by instanced number of times.
        self.tire_r = tire_r * Tire.count


def get_rotation_speed(engine: Engine = Depends(Engine)) -> int:
    # Arguments of `Engine` class will inject from dependencies.
    # In this example, the gear_ratio is configured 100 or 50
    return engine.gear_ratio


@inject
def get_tire_speed(
    tire: Tire = Singleton(Tire),
    rpm: int = Depends(get_rotation_speed)
) -> float:
    # Depends is always created such as factory pattern
    # Singleton is only generate at once such as singleton pattern.
    # The singleton object is shared in the Container class.
    return tire.tire_r * rpm


def main():
    container = Container()

    # Configuration of container
    container.configure(Config(100, 100))
    with container:
        print('Speed:', get_tire_speed())  # 10000
        print('#Tire:', Tire.count)  # 1

    # If the configuration value is changed, the displaying value is difference.
    # But `Tire.count` is same so that a second argument, the Tire object is re-used.
    container.configure(Config(20, 100))
    with container:
        print('Speed:', get_tire_speed())  # 2000
        print('#Tire:', Tire.count)  # 1

    # If the configuration value is changed, the displaying value is difference.
    # The `Tire` object is updated.
    container.configure(Config(20, 10))
    with container:
        print('Speed:', get_tire_speed())  # 400
        print('#Tire:', Tire.count)  # 2


if __name__ == '__main__':
    main()

```
