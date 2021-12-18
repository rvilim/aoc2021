from math import floor, ceil
import json
from typing import List, Optional
from copy import deepcopy


class Node:
    def __init__(self, left, right, value, parent):
        self.left = left
        self.right = right
        self.parent = parent
        self.value = value

    def __repr__(self) -> str:
        return f"({self.value})"


def parse(input: str) -> Node:
    root = Node(None, None, None, None)

    construct_tree(root, json.loads(input))

    return root


def construct_tree(root: Node, input):

    if isinstance(input[0], int):
        root.left = Node(None, None, input[0], root)

    if isinstance(input[1], int):
        root.right = Node(None, None, input[1], root)

    if isinstance(input[0], list):
        root.left = Node(None, None, None, root)
        construct_tree(root.left, input[0])

    if isinstance(input[1], list):
        root.right = Node(None, None, None, root)
        construct_tree(root.right, input[1])


def find_left_neighbour(root: Node, interest: Node) -> Optional[Node]:
    path = traverse(root)

    for i, n in enumerate(path):
        if n == interest.left:
            if i != 0:
                return path[i - 1]
            else:
                return None
    raise ValueError("Not found")


def find_right_neighbour(root: Node, interest: Node) -> Optional[Node]:
    path = traverse(root)

    for i, n in enumerate(path):
        if n == interest.right:
            if i != len(path) - 1:
                return path[i + 1]
            else:
                return None
    raise ValueError("Not found")


def find_explode_candidate(node: Node, depth: int = 0) -> Optional[Node]:
    if node.left.value is not None and node.right.value is not None and depth == 4:
        return node

    if node.left.value is None:
        r = find_explode_candidate(node.left, depth + 1)
        if r:
            return r

    if node.right.value is None:
        r = find_explode_candidate(node.right, depth + 1)
        if r:
            return r
    return None


def explode(root: Node) -> bool:
    node = find_explode_candidate(root)

    if node is None:
        return False

    assert node.left.value is not None and node.right.value is not None

    left_neighbour = find_left_neighbour(root, node)
    right_neighbour = find_right_neighbour(root, node)

    if right_neighbour:
        right_neighbour.value += node.right.value

    if left_neighbour:
        left_neighbour.value += node.left.value

    node.left = None
    node.right = None
    node.value = 0

    return True


def split(root: Node) -> bool:
    nodes = traverse(root)

    for n in nodes:
        if n.value >= 10:
            n.left = Node(None, None, int(floor(n.value / 2)), n)
            n.right = Node(None, None, int(ceil(n.value / 2)), n)
            n.value = None
            return True
    return False


def traverse(node: Node) -> List[Node]:
    nodes = []
    if node.left is not None:
        nodes.extend(traverse(node.left))

    if node.value is not None:
        nodes.append(node)

    if node.right is not None:
        nodes.extend(traverse(node.right))

    return nodes


def add(left: Node, right: Node) -> Node:
    node = Node(left, right, None, None)
    node.left.parent = node
    node.right.parent = node
    return node


def add_many(nodes: List[Node]) -> Node:
    running_sum = nodes[0]
    for addend in nodes[1:]:
        running_sum = add(running_sum, addend)
        reduce(running_sum)

    return running_sum


def reduce(root: Node):
    while True:
        if explode(root):
            continue
        if split(root):
            continue
        break


def magnitude(node: Node) -> int:

    s = 0

    if node.left.value is None:
        s += 3 * magnitude(node.left)
    else:
        s += 3 * node.left.value

    if node.right.value is None:
        s += 2 * magnitude(node.right)
    else:
        s += 2 * node.right.value

    return s


def largest_sum(input: List[Node]) -> int:
    largest = 0

    for i in input:
        for j in input:
            if i == j:
                continue

            i_copy = deepcopy(i)
            j_copy = deepcopy(j)
            res = add(i_copy, j_copy)

            reduce(res)

            if magnitude(res) > largest:
                largest = magnitude(res)

            i_copy = deepcopy(i)
            j_copy = deepcopy(j)

            res = add(j_copy, i_copy)
            reduce(res)
            if magnitude(res) > largest:
                largest = magnitude(res)

    return largest


if __name__ == "__main__":
    root = parse("[7,6]")

    root = parse("[7,[6,[5,[4,[3,2]]]]]")
    assert find_left_neighbour(root, root.right.right.right.right).value == 4

    n = find_explode_candidate(root)
    assert n.left.value == 3 and n.right.value == 2

    explode(root)
    assert str(traverse(root)) == "[(7), (6), (5), (7), (0)]"

    root = parse("[[[[[9,8],1],2],3],4]")

    assert find_left_neighbour(root, root.left.left.left.left) is None
    assert find_right_neighbour(root, root.left.left.left.left).value == 1

    n = find_explode_candidate(root)
    assert n.left.value == 9 and n.right.value == 8

    explode(root)
    assert str(traverse(root)) == "[(0), (9), (2), (3), (4)]"

    root = parse("[[6,[5,[4,[3,2]]]],1]")
    explode(root)
    assert str(traverse(root)) == "[(6), (5), (7), (0), (3)]"

    root = parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    explode(root)
    assert str(traverse(root)) == "[(3), (2), (8), (0), (9), (5), (4), (3), (2)]"

    root = parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    explode(root)
    assert str(traverse(root)) == "[(3), (2), (8), (0), (9), (5), (7), (0)]"

    root = parse("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    split(root)
    assert str(traverse(root)) == "[(0), (7), (4), (7), (8), (0), (13), (1), (1)]"

    root = parse("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    split(root)
    split(root)
    assert str(traverse(root)) == "[(0), (7), (4), (7), (8), (0), (6), (7), (1), (1)]"

    addend_1 = parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    addend_2 = parse("[1,1]")

    root = add(addend_1, addend_2)
    reduce(root)

    input = [parse(i) for i in ["[1,1]", "[2,2]", "[3,3]", "[4,4]"]]
    assert str(traverse(add_many(input))) == "[(1), (1), (2), (2), (3), (3), (4), (4)]"

    input = [parse(i) for i in ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]]
    assert str(traverse(add_many(input))) == "[(3), (0), (5), (3), (4), (4), (5), (5)]"

    input = [parse(i) for i in ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"]]
    assert str(traverse(add_many(input))) == "[(5), (0), (7), (4), (5), (5), (6), (6)]"

    input = [
        parse(i)
        for i in [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ]
    ]
    result = add(input[0], input[1])
    reduce(result)
    assert str(traverse(result)) == "[(4), (0), (5), (4), (7), (7), (6), (0), (8), (7), (7), (7), (9), (5), (0)]"
    assert str(traverse(add_many(input))) == "[(8), (7), (7), (7), (8), (6), (7), (7), (0), (7), (6), (6), (8), (7)]"

    assert magnitude(parse("[[1,2],[[3,4],5]]")) == 143
    assert magnitude(parse("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")) == 1384.0
    assert magnitude(parse("[[[[1,1],[2,2]],[3,3]],[4,4]]")) == 445
    assert magnitude(parse("[[[[3,0],[5,3]],[4,4]],[5,5]]")) == 791
    assert magnitude(parse("[[[[5,0],[7,4]],[5,5]],[6,6]]")) == 1137
    assert magnitude(parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")) == 3488

    input_raw = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    input = [parse(i) for i in input_raw.split("\n")]

    assert magnitude(add_many(input)) == 4140

    with open("data/18.txt") as f:
        input = [parse(i) for i in f.readlines()]

    print(magnitude(add_many(input)))

    # Part 2

    input_raw = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    input = [parse(i) for i in input_raw.split("\n")]

    assert largest_sum(input) == 3993

    with open("data/18.txt") as f:
        input = [parse(i) for i in f.readlines()]

    print(largest_sum(input))
