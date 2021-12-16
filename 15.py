import numpy as np
from typing import Generator, Tuple


def test_input():
    return """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def real_input():
    with open("data/15.txt") as f:
        return f.read()


def get_neighbours(row: int, col: int, n_rows: int, n_cols: int) -> Generator[Tuple[int, int], None, None]:
    for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= row + i < n_rows and 0 <= col + j < n_cols:
            yield (row + i, col + j)


def parse(input: str) -> np.ndarray:
    grid = [[int(i) for i in line] for line in input.split("\n") if line]
    return np.array(grid)


def path(grid: np.ndarray):
    max_distance = np.sum(grid)
    visited = np.zeros_like(grid, dtype=bool)
    distance = np.full_like(grid, np.sum(grid) + 1, dtype=int)
    distance[0, 0] = 0

    current_node = (0, 0)

    while True:
        for neighbour in get_neighbours(*current_node, *grid.shape):
            if not visited[neighbour]:
                new_distance = distance[current_node] + grid[neighbour]

                if new_distance < distance[neighbour]:
                    distance[neighbour] = new_distance

        visited[current_node[0], current_node[1]] = True

        if visited[-1, -1]:
            break

        # This is a hack to make the np.argmin faster, doing it on a masked array is kinda slow
        distance[current_node[0], current_node[1]] = max_distance
        current_node = np.unravel_index(np.argmin(distance), distance.shape)

    return distance[-1, -1]


def tile_map(input: np.ndarray) -> np.ndarray:
    new_grid = np.zeros(np.array(input.shape) * 5, dtype=int)

    in_rows, in_cols = input.shape

    for i in range(5):
        for j in range(5):
            new_grid[i * in_rows : (i + 1) * in_rows, j * in_cols : (j + 1) * in_cols] = input + i + j

    new_grid[new_grid >= 10] = new_grid[new_grid >= 10] - 9

    return new_grid


if __name__ == "__main__":
    input = test_input()

    assert path(parse(input)) == 40

    print(path(parse(real_input())))

    # Part 2

    input = test_input()
    new_grid = tile_map(parse(input))
    assert path(new_grid) == 315

    print(path(tile_map(parse(real_input()))))
