from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass(frozen=True)
class Dot:
    row: int
    col: int


@dataclass(frozen=True)
class Fold:
    axis: str
    coord: int


def test_input() -> Tuple[Tuple[Dot, ...], Tuple[Fold, ...]]:

    raw = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    return parse(raw)


def real_input():
    raw = open("data/13.txt").read()
    return parse(raw)


def parse(raw: str):
    dots = []
    folds = []

    raw_dots, raw_folds = raw.split("\n\n")

    for line in raw_dots.split("\n"):
        col, row = line.split(",")
        dots.append(Dot(int(row), int(col)))

    for line in raw_folds.split("\n"):
        axis, coord = line.replace("fold along ", "").split("=")
        folds.append(Fold(axis, int(coord)))

    return tuple(dots), tuple(folds)


def draw_sheet(dots: Tuple[Dot, ...]) -> np.ndarray:
    n_rows = np.amax([d.row for d in dots]) + 1
    n_cols = np.amax([d.col for d in dots]) + 1

    print(n_rows, n_cols)
    sheet = np.zeros((n_rows, n_cols), dtype=bool)

    for dot in dots:
        sheet[dot.row, dot.col] = True

    for row in sheet:
        print("".join(["#" if col else "." for col in row]))


def fold_dot(dot: Dot, fold: Fold) -> Dot:

    if fold.axis == "x":
        if dot.col > fold.coord:

            d = Dot(dot.row, dot.col - 2 * (dot.col - fold.coord))
            assert d.col >= 0
            return d
        else:
            return dot

    elif fold.axis == "y":
        if dot.row > fold.coord:
            d = Dot(dot.row - 2 * (dot.row - fold.coord), dot.col)
            assert d.row >= 0
            return d
        else:
            return dot


def fold(dots: Tuple[Dot, ...], fold: Fold) -> Tuple[Dot, ...]:
    return tuple({fold_dot(dot, fold) for dot in dots})


if __name__ == "__main__":
    dots, folds = test_input()

    assert 17 == len(fold(dots, folds[0]))
    assert 16 == len(fold(fold(dots, folds[0]), folds[1]))

    dots, folds = real_input()

    print(len(fold(dots, folds[0])))

    # part 2

    dots, folds = real_input()

    for f in folds:
        dots = fold(dots, f)

    draw_sheet(dots)
