from typing import Tuple, Dict
from collections import Counter, defaultdict


def test_input():
    return tuple((int(i) for i in "3,4,3,1,2".split(",")))


def real_input() -> Tuple[int, ...]:
    with open("data/6.txt") as f:
        return tuple((int(i) for i in f.readline().split(",")))


def refactor_state(state: Tuple[int, ...]) -> Dict[int, int]:
    return defaultdict(int, dict(Counter(state)))


def tick(state: Dict[int, int]) -> Dict[int, int]:
    new_state = defaultdict(int)

    new_state[8] = state[0]
    new_state[6] = state[7] + state[0]
    new_state[7] = state[8]

    for i in range(6):
        new_state[i] = state[i + 1]

    return new_state


def tick_many(state: Dict[int, int], n: int) -> Dict[int, int]:
    new_state = state.copy()

    for _ in range(n):
        new_state = tick(new_state)

    return new_state


def score_state(state: Dict[int, int]) -> int:
    return sum(state.values())


if __name__ == "__main__":
    s = refactor_state(test_input())
    assert sum(tick_many(s, 80).values()) == 5934

    t = refactor_state(real_input())
    print(sum(tick_many(t, 80).values()))

    # part 2
    s = refactor_state(test_input())
    assert sum(tick_many(s, 256).values()) == 26984457539

    t = refactor_state(real_input())
    print(sum(tick_many(t, 256).values()))
