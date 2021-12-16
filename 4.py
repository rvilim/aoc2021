from typing import List, Tuple

import numpy as np


def test_input():

    raw = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
    return [x for x in raw.split("\n")]


def real_input() -> List[int]:
    with open("data/4.txt") as f:
        return [x.rstrip() for x in f.readlines()]


def parse(input: List[str]) -> List[List[int]]:

    order = [int(i) for i in input[0].split(",")]

    boards = []

    for line in range(2, len(input), 6):
        boards.append(
            np.array([int(row[i : i + 3]) for row in input[line : line + 6] for i in range(0, len(row), 3)]).reshape(5, 5)
        )

    return order, boards


def mark(number: int, boards: List[np.ndarray], marks: List[bool], boards_won):
    for index, (mark, board) in enumerate(zip(marks, boards)):
        if index in [a[0] for a in boards_won]:
            continue

        marks[index] = mark | (board == number)


def check(marks: List[np.ndarray], boards_won) -> Tuple[int, np.ndarray, np.ndarray]:
    winning_indices = []
    for index, mark in enumerate(marks):
        if index in [a[0] for a in boards_won]:
            continue

        for i in range(5):
            if np.all(mark[i, :]) or np.all(mark[:, i]):
                winning_indices.append(index)

    return winning_indices


def score_board(winning_board, winning_marks, number):
    return np.sum(winning_board[winning_marks == False]) * number


def play(order, boards):
    boards_won = []

    marks = [np.zeros((5, 5), dtype=bool) for i in enumerate(boards)]

    for number in order:
        mark(number, boards, marks, boards_won)
        winning_board_indices = check(marks, boards_won)

        for winning_board_index in winning_board_indices:
            winning_board = boards[winning_board_index]
            winning_marks = marks[winning_board_index]
            winning_score = score_board(winning_board, winning_marks, number)

            boards_won.append((winning_board_index, winning_score, winning_marks))

    return boards_won


if __name__ == "__main__":
    test_order, test_boards = parse(test_input())

    wins = play(test_order, test_boards)
    assert wins[0][0] == 2
    assert wins[0][1] == 4512

    order, boards = parse(real_input())
    wins = play(order, boards)
    print(play(order, boards)[0][1])

    # part 2
    wins = play(test_order, test_boards)
    assert wins[-1][0] == 1
    assert wins[-1][1] == 1924

    print(play(order, boards)[-1][1])
