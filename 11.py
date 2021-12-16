import numpy as np
from scipy.signal import convolve2d
from typing import Tuple


def real_input() -> np.ndarray:
    with open("data/11.txt") as f:
        return np.array([[int(l) for l in r.rstrip()] for r in f])


def parse_input(raw=None) -> np.ndarray:
    if raw is None:
        raw = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

    return np.array([[int(l) for l in r] for r in raw.split("\n")])


def step(energy: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    e = energy.copy()
    e += 1

    newly_flashed = e == 10
    flashed = e == 10

    while True:
        kernel = np.asarray([[True, True, True], [True, False, True], [True, True, True]])
        e += convolve2d(newly_flashed.astype(int), kernel.astype(int), mode="same").astype(int)

        newly_flashed = (e >= 10) & (~flashed)
        flashed |= newly_flashed

        if not newly_flashed.any():
            break

    e[flashed] = 0
    return e, flashed


def get_synchronized_step(energy: np.ndarray) -> np.ndarray:
    step_number = 0
    while not (energy == 0).all():
        e, f = step(energy)
        energy = e
        step_number += 1

    return step_number


def steps(initial_energy: np.ndarray, n_steps: int):
    e = initial_energy.copy()
    n_flashed = np.zeros_like(initial_energy)

    for _ in range(n_steps):
        e, f = step(e)
        n_flashed += f
    return e, np.sum(n_flashed)


if __name__ == "__main__":
    t = parse_input("""11111\n19991\n19191\n19991\n11111""")

    e, _ = step(t)
    assert (e == parse_input("""34543\n40004\n50005\n40004\n34543""")).all()

    e, _ = step(e)
    assert (e == parse_input("""45654\n51115\n61116\n51115\n45654""")).all()

    e, _ = steps(t, 2)
    assert (e == parse_input("""45654\n51115\n61116\n51115\n45654""")).all()

    t = parse_input()

    e, _ = step(t)
    assert (
        e
        == parse_input(
            """6594254334\n3856965822\n6375667284\n7252447257\n7468496589\n5278635756\n3287952832\n7993992245\n5957959665\n6394862637"""
        )
    ).all()

    input = parse_input(
        "6594254334\n3856965822\n6375667284\n7252447257\n7468496589\n5278635756\n3287952832\n7993992245\n5957959665\n6394862637"
    )

    output = parse_input(
        "8807476555\n5089087054\n8597889608\n8485769600\n8700908800\n6600088989\n6800005943\n0000007456\n9000000876\n8700006848"
    )

    e, _ = step(input)
    assert (e == output).all()

    input = parse_input()
    e, _ = steps(input, 1)
    output = parse_input(
        "6594254334\n3856965822\n6375667284\n7252447257\n7468496589\n5278635756\n3287952832\n7993992245\n5957959665\n6394862637"
    )
    assert (e == output).all()

    input = parse_input()
    e, _ = steps(input, 2)
    output = parse_input(
        "8807476555\n5089087054\n8597889608\n8485769600\n8700908800\n6600088989\n6800005943\n0000007456\n9000000876\n8700006848"
    )
    assert (e == output).all()

    input = parse_input()
    e, n_flashed = steps(input, 10)
    output = parse_input(
        "0481112976\n0031112009\n0041112504\n0081111406\n0099111306\n0093511233\n0442361130\n5532252350\n0532250600\n0032240000"
    )
    assert (e == output).all()
    assert n_flashed == 204

    input = parse_input()
    output = parse_input(
        "0397666866\n0749766918\n0053976933\n0004297822\n0004229892\n0053222877\n0532222966\n9322228966\n7922286866\n6789998766"
    )
    e, n_flashed = steps(input, 100)
    assert (e == output).all()
    assert n_flashed == 1656

    input = real_input()
    e, n_flashed = steps(input, 100)
    print(n_flashed)

    # part 2

    input = parse_input()
    assert 195 == get_synchronized_step(input)

    input = real_input()
    print(get_synchronized_step(input))
