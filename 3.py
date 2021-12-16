from collections import Counter

from typing import List, Tuple


def test_input():

    raw = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    return [x for x in raw.split("\n")]


def real_input() -> List[int]:
    with open("data/3.txt") as f:
        return [x for x in f.readlines()]


def get_gamma_epsilon(input: List[str]) -> Tuple[int, int]:
    c = [Counter() for _ in range(len(input[0]))]

    for row in input:
        for i, x in enumerate(row):
            c[i].update(x)

    gamma = int("".join(i.most_common(1)[0][0] for i in c), 2)
    epsilon = int("".join(i.most_common()[-1][0] for i in c), 2)

    return gamma, epsilon


def get_bit_rating(input: List[str], pos: int) -> Tuple[int, int]:
    n_zeros = 0
    n_ones = 0

    for row in input:
        if row[pos] == "1":
            n_ones += 1
        else:
            n_zeros += 1

    most_common = 1 if n_ones >= n_zeros else 0
    least_common = 1 if n_ones < n_zeros else 0

    return most_common, least_common


def get_rating(input: List[str], oxygen: bool) -> int:
    length = len(input[0])

    for pos in range(length):
        input = [row for row in input if get_bit_rating(input, pos)[int(not oxygen)] == int(row[pos])]

        if len(input) == 1:
            return int(input[0], 2)


if __name__ == "__main__":

    test = test_input()
    assert get_gamma_epsilon(test_input()) == (22, 9)

    gamma, epsilon = get_gamma_epsilon(real_input())
    print(gamma * epsilon)

    bit_rating_input = ["111", "100", "101", "000"]
    assert get_bit_rating(bit_rating_input, 0) == (1, 0)
    assert get_bit_rating(bit_rating_input, 1) == (0, 1)
    assert get_bit_rating(bit_rating_input, 2) == (1, 0)

    assert get_rating(test_input(), True) == 23
    assert get_rating(test_input(), False) == 10
    assert get_rating(test_input(), False) * get_rating(test_input(), True) == 230

    print(get_rating(real_input(), False) * get_rating(real_input(), True))
