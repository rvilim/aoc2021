import numpy as np
from typing import NamedTuple, Set, Dict


class Point(NamedTuple):
    row: int
    col: int


def real_input() -> np.ndarray:
    with open("data/9.txt") as f:
        return np.array([[int(l) for l in r.rstrip()] for r in f])


def test_input() -> np.ndarray:
    raw = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    return np.array([[int(l) for l in r] for r in raw.split("\n")])


def test_input_custom() -> np.ndarray:
    raw = """2122243210
3987894921
9856789892
8767896789
9899965678"""
    return np.array([[int(l) for l in r] for r in raw.split("\n")])


def low_points_risk(grid: np.ndarray) -> int:
    padded = np.pad(grid, 1, "constant", constant_values=np.amax(grid) + 1)

    low_point = (
        (padded < np.roll(padded, 1, axis=1))
        & (padded < np.roll(padded, -1, axis=1))
        & (padded < np.roll(padded, 1, axis=0))
        & (padded < np.roll(padded, -1, axis=0))
    )
    return np.sum(1 + grid[low_point[1:-1, 1:-1]])


def neighbours(grid: np.ndarray, point: Point) -> list:
    return [
        Point(point.row + x, point.col + y)
        for x, y in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if (0 <= point.row + x < grid.shape[0]) and (0 <= point.col + y < grid.shape[1])
    ]


def get_basin_size(grid: np.ndarray, basin_point: Point, all_basin_points: Set[Point], max: int) -> int:

    visited = set([basin_point])
    other_basin_points = all_basin_points - {basin_point}

    q = [basin_point]

    while q:
        current = q.pop()
        if current in other_basin_points:
            raise ValueError("Basin has two low points")

        for neighbour in neighbours(grid, current):
            if grid[neighbour.row, neighbour.col] <= max and neighbour not in visited:
                q.append(neighbour)
                visited.add(neighbour)

    return len(visited)


def get_basins(grid: np.ndarray):
    padded = np.pad(grid, 1, "constant", constant_values=np.amax(grid) + 1)

    low_point = (
        (padded < np.roll(padded, 1, axis=1))
        & (padded < np.roll(padded, -1, axis=1))
        & (padded < np.roll(padded, 1, axis=0))
        & (padded < np.roll(padded, -1, axis=0))
    )[1:-1, 1:-1]

    low_point_coords = np.where(low_point)
    low_point_coords = {Point(x, y) for x, y in zip(low_point_coords[0], low_point_coords[1])}

    basin_sizes = {}
    for basin in low_point_coords:
        for height in range(9):
            try:
                basin_sizes[basin] = get_basin_size(grid, basin, low_point_coords, height)
            except ValueError:
                break
    return basin_sizes


def test_get_basins():

    t = test_input()
    low_point_coords = {
        Point(row=0, col=1),
        Point(row=4, col=6),
        Point(row=0, col=9),
        Point(row=2, col=2),
    }
    assert 1 == get_basin_size(t, Point(row=0, col=1), low_point_coords, 1)
    assert 2 == get_basin_size(t, Point(row=0, col=1), low_point_coords, 2)
    assert 3 == get_basin_size(t, Point(row=0, col=1), low_point_coords, 3)
    assert 3 == get_basin_size(t, Point(row=0, col=1), low_point_coords, 4)

    assert 14 == get_basin_size(t, Point(row=2, col=2), low_point_coords, 8)
    assert 7 == get_basin_size(t, Point(row=2, col=2), low_point_coords, 7)

    # t_custom is the same basin, except the 0,1 and 0,9 points are not separated
    # by 9's

    """
2122243210
3987894921
9856789892
8767896789
9899965678
    """
    t_custom = test_input_custom()
    assert 1 == get_basin_size(t_custom, Point(row=0, col=9), low_point_coords, 0)
    assert 3 == get_basin_size(t_custom, Point(row=0, col=9), low_point_coords, 1)
    assert 7 == get_basin_size(t_custom, Point(row=0, col=9), low_point_coords, 3)

    # In this example going to 4 will overflow a saddle point and the basin
    # will merge with the basin at 0,1. This should raise a value error
    try:
        get_basin_size(t_custom, Point(row=0, col=9), low_point_coords, 4)
        assert False
    except ValueError:
        pass


def score(basin_sizes: Dict[Point, int]) -> int:
    top_3 = sorted(basin_sizes.values(), reverse=True)[:3]

    return top_3[0] * top_3[1] * top_3[2]


if __name__ == "__main__":
    t = test_input()
    assert 15 == low_points_risk(t)

    r = real_input()
    print(low_points_risk(r))

    # part 2

    basin_sizes = get_basins(t)
    assert score(basin_sizes) == 1134
    test_get_basins()

    basin_sizes = get_basins(r)
    print(score(basin_sizes))
