from typing import List, Tuple


def test_input() -> List[str]:
    raw = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
    return [x for x in raw.split("\n")]


def parse_1(input: List[str]) -> List[Tuple[int, int]]:
    res = []

    for l in input:
        direction, magnitude = l.split(" ")

        if direction == "forward":
            res.append((0, int(magnitude)))
        elif direction == "up":
            res.append((-int(magnitude), 0))
        elif direction == "down":
            res.append((int(magnitude), 0))
        else:
            print("Unknown direction: {}".format(direction))
    return res


def parse_2(input: List[str]) -> List[Tuple[int, int]]:
    res = []
    aim = 0

    for l in input:
        direction, magnitude = l.split(" ")

        if direction == "forward":
            res.append((aim * int(magnitude), int(magnitude)))
        elif direction == "up":
            aim -= int(magnitude)
        elif direction == "down":
            aim += int(magnitude)
        else:
            print("Unknown direction: {}".format(direction))

    return res


def real_input() -> List[int]:
    with open("data/2.txt") as f:
        return [x for x in f.readlines()]


def destination(input: List[Tuple[int, int]]):
    return [sum(x) for x in zip(*input)]


if __name__ == "__main__":
    input = test_input()

    assert parse_1(input) == [(0, 5), (5, 0), (0, 8), (-3, 0), (8, 0), (0, 2)]
    assert destination(parse_1(input)) == [10, 15]

    input = real_input()
    dest = destination(parse_1(input))
    print(dest[0] * dest[1])

    input = test_input()
    assert destination(parse_2(input)) == [60, 15]

    input = real_input()
    dest = destination(parse_2(input))
    print(dest[0] * dest[1])
