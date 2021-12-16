from typing import List


def test_input() -> List[int]:
    raw = """199
    200
    208
    210
    200
    207
    240
    269
    260
    263"""

    return [int(x) for x in raw.split("\n")]


def real_input() -> List[int]:
    with open("data/1.txt") as f:
        return [int(x) for x in f.readlines()]


def count_increased(input: List[int]) -> int:
    return sum(cur > prev for prev, cur in zip(input, input[1:]))


def get_window(input: List[int]) -> List[int]:
    return [i + j + k for i, j, k in zip(input, input[1:], input[2:])]


if __name__ == "__main__":
    t = test_input()
    assert count_increased(t) == 7

    print(count_increased(real_input()))

    assert get_window(t) == [607, 618, 618, 617, 647, 716, 769, 792]
    assert count_increased(get_window(t)) == 5

    print(count_increased(get_window(real_input())))
