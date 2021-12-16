from typing import List
import numpy as np
from itertools import zip_longest


def test_input():
    raw = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    return raw.split("\n")


def real_input() -> List[int]:
    with open("data/5.txt") as f:
        return [x.rstrip() for x in f.readlines()]


def parse(input: List[str]):
    return np.array([line.replace(" -> ", ",").split(",") for line in input]).astype(int)


def draw_lines(input: np.ndarray, no_diagonals: bool):

    if no_diagonals:
        diagonal_filter = np.logical_or(input[:, 0] == input[:, 2], input[:, 1] == input[:, 3])
        input = input[diagonal_filter, :]

    max_y = max(np.amax(input[:, 0]), np.amax(input[:, 2])) + 1
    max_x = max(np.amax(input[:, 1]), np.amax(input[:, 3])) + 1
    board = np.zeros((max_y, max_x), dtype=int)

    for row in input:
        if row[0] == row[2]:
            start = min(row[1], row[3])
            end = max(row[1], row[3]) + 1

            board[start:end, row[0]] += 1
        elif row[1] == row[3]:
            start = min(row[0], row[2])
            end = max(row[0], row[2]) + 1

            board[row[1], start:end] += 1
        else:

            step_x = -1 if row[0] > row[2] else 1
            step_y = -1 if row[1] > row[3] else 1

            for x, y in zip(range(row[0], row[2] + step_x, step_x), range(row[1], row[3] + step_y, step_y)):
                board[y, x] += 1

    return board


def score(board: np.ndarray) -> int:
    return np.sum(board > 1)


if __name__ == "__main__":
    input = parse(test_input())
    board = draw_lines(input, True)
    assert score(board) == 5

    input = parse(real_input())
    board = draw_lines(input, True)
    print(score(board))

    # part 2
    input = parse(test_input())
    board = draw_lines(input, False)
    assert score(board) == 12

    input = parse(real_input())
    board = draw_lines(input, False)
    print(score(board))
