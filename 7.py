import numpy as np
from typing import Tuple


def test_input() -> np.ndarray:
    raw = "16,1,2,0,4,2,7,1,2,14"
    return np.array([int(i) for i in raw.split(",")])


def real_input() -> np.ndarray:
    with open("data/7.txt") as f:
        return np.array([int(i) for i in f.readline().split(",")])


def shift_fuel(init: np.ndarray, pos: int, increasing: bool = False) -> int:
    if not increasing:
        return np.sum(np.abs(init - pos))

    n = np.abs(init - pos)
    return int(np.sum(n * (n + 1) // 2))


def scan(init: np.ndarray, increasing: bool = False) -> Tuple[int, int]:
    min_fuel_pos = int(np.argmin([shift_fuel(init, pos, increasing) for pos in range(len(init))]))
    min_fuel = shift_fuel(init, min_fuel_pos, increasing)

    return min_fuel_pos, min_fuel


if __name__ == "__main__":
    t = test_input()

    min_fuel_pos, min_fuel = scan(t, increasing=False)
    assert min_fuel_pos == 2
    assert min_fuel == 37

    r = real_input()
    min_fuel_pos, min_fuel = scan(r, increasing=False)
    print(min_fuel_pos, min_fuel)

    # Part 2
    t = test_input()
    min_fuel_pos, min_fuel = scan(t, increasing=True)
    assert min_fuel_pos == 5
    assert min_fuel == 168

    t = real_input()
    min_fuel_pos, min_fuel = scan(t, increasing=True)
    print(min_fuel_pos, min_fuel)
