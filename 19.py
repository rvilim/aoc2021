import numpy as np
from collections import Counter, defaultdict
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Transform:
    from_index: int
    to_index: int
    offset: np.ndarray
    rotation: np.ndarray


def test_rotate():
    input = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7"""

    expected_raw = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8"""

    scanners = parse(input)
    expecteds = parse(expected_raw)
    rotations = get_rotations()

    for expected in expecteds:
        assert any(np.all(expected == rotation) for rotation in rotate(scanners[0], rotations))


def parse(input: str):
    scanners = []

    for scanner in input.split("\n\n--- "):
        scanner_list = []
        for line_no, line in enumerate(scanner.split("\n")):
            if line_no == 0:
                continue
            scanner_list.append([int(i) for i in line.split(",")])
        scanners.append(np.array(scanner_list))
    return scanners


def read(filename: str):
    with open(filename) as f:
        return parse(f.read())


def get_rotations():
    x = np.zeros((3, 3))
    x[:, :] = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    y = np.zeros((3, 3))
    y[:, :] = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])

    z = np.zeros((3, 3))
    z[:, :] = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    return [
        i.astype(int)
        for i in [
            np.eye(3),
            x,
            y,
            z,
            x @ x,
            x @ y,
            x @ z,
            y @ x,
            y @ y,
            z @ y,
            z @ z,
            x @ x @ x,
            x @ x @ y,
            x @ x @ z,
            x @ y @ x,
            x @ y @ y,
            x @ z @ z,
            y @ x @ x,
            y @ y @ y,
            z @ z @ z,
            x @ x @ x @ y,
            x @ x @ y @ x,
            x @ y @ x @ x,
            x @ y @ y @ y,
        ]
    ]


def rotate(coords: np.ndarray, rotations: List[np.ndarray]):
    for rotation in rotations:
        yield rotation, coords @ rotation


def find_offsets_single_dim(points_1: np.ndarray, points_2: np.ndarray):

    c = Counter(point_1 - point_2 for point_1 in points_1 for point_2 in points_2)

    offset, number = c.most_common()[0]

    if number < 12:
        raise ValueError("No match found")

    return offset


def find_translation(points_1: np.ndarray, points_2: np.ndarray):
    rotations = get_rotations()

    for rotation, rotated in rotate(points_2, rotations):
        try:
            x_offset = find_offsets_single_dim(points_1[:, 0], rotated[:, 0])
            y_offset = find_offsets_single_dim(points_1[:, 1], rotated[:, 1])
            z_offset = find_offsets_single_dim(points_1[:, 2], rotated[:, 2])
            return rotation, np.array([x_offset, y_offset, z_offset])
        except ValueError:
            continue
    # return rotation, np.array([x_offset, y_offset, z_offset])
    raise ValueError("No match found")


def single_transform(coords, offset, rotation):
    return (coords @ rotation) + offset


def solve_transforms(scanners):
    transforms = defaultdict(dict)
    for index_1, scanner_1 in enumerate(scanners):
        for index_2, scanner_2 in enumerate(scanners):
            if index_1 == index_2:
                continue
            try:
                rotation, translation = find_translation(scanner_1, scanner_2)

                transforms[index_2][index_1] = Transform(index_1, index_2, translation, rotation)

            except ValueError:
                continue

    return transforms


def transform_paths(transforms, path):
    current = path[-1][1]
    visited = [i[0] for i in path] + [i[1] for i in path]

    for dest in transforms[current].keys():
        if dest in visited:
            continue

        if dest == 0:
            return path + [(current, 0)]

        if transform_paths(transforms, path + [(current, dest)]):
            return transform_paths(transforms, path + [(current, dest)])


def normalize_points(transforms, scanners):
    all_points = {tuple(i) for i in scanners[0]}

    for scanner_num, scanner in enumerate(scanners):
        if scanner_num == 0:
            continue

        transform_path = transform_paths(transforms, [[None, scanner_num]])[1:]

        points = scanner.copy()
        for t in transform_path:
            points = single_transform(points, transforms[t[0]][t[1]].offset, transforms[t[0]][t[1]].rotation)

        all_points = all_points.union({tuple(i) for i in points})

    return all_points


def manhattan(point1: Tuple[int], point2: Tuple[int]):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])


def max_scanner_distance(transforms):
    # n_scanners = max(i for i in transforms.keys()) + 1
    n_scanners = max(max(from_t, to_t) for from_t in transforms.keys() for to_t in transforms[from_t].keys()) + 1

    origins = [np.array([[0, 0, 0]]) for _ in range(n_scanners)]

    normalized_points = normalize_points(transforms, origins)

    return max(manhattan(i, j) for i in normalized_points for j in normalized_points)


if __name__ == "__main__":
    scanners_test = read("data/19_test.txt")
    scanners_real = read("data/19.txt")

    transforms = solve_transforms(scanners_test)
    normalized_points = normalize_points(transforms, scanners_test)
    assert 79 == len(normalized_points)

    transforms = solve_transforms(scanners_real)
    normalized_points = normalize_points(transforms, scanners_real)
    print(len(normalized_points))

    # pt 2
    transforms = solve_transforms(scanners_test)
    assert 3621 == max_scanner_distance(transforms)

    transforms = solve_transforms(scanners_real)
    print(max_scanner_distance(transforms))
