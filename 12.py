from typing import DefaultDict, List, TypeVar, Generic, Set

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, name: str):

        self.name = name
        self.big = self.name.isupper()
        self.neighbours: List[T] = []

    def add_neighbour(self, neighbour: T):
        self.neighbours.append(neighbour)

    def __repr__(self) -> str:
        return f"(name={self.name}, neighbours={','.join([n.name for n in self.neighbours])})"


def real_input():
    return """start-kc
pd-NV
start-zw
UI-pd
HK-end
UI-kc
pd-ih
ih-end
start-UI
kc-zw
end-ks
MF-mq
HK-zw
LF-ks
HK-kc
ih-HK
kc-pd
ks-pd
MF-pd
UI-zw
ih-NV
ks-HK
MF-kc
zw-NV
NV-ks"""


def parse_input(input):
    nodes = {}
    for line in input.split("\n"):
        from_node, to_node = line.split("-")

        assert not (from_node.isupper() and to_node.isupper()), "Two big caves will result in an infinite loop"

        if from_node not in nodes:
            nodes[from_node] = Node(from_node)

        if to_node not in nodes:
            nodes[to_node] = Node(to_node)

    for line in input.split("\n"):
        from_node, to_node = line.split("-")
        # We don't ever want to go back to start
        if to_node != "start":
            nodes[from_node].add_neighbour(nodes[to_node])

        if from_node != "start":
            nodes[to_node].add_neighbour(nodes[from_node])

    # We get an implicit stopping condition if we say that the end node
    # has no neighbours
    nodes["end"].neighbours = []
    return nodes


def traverse(node: Node, visited: List[Node]):
    paths = []
    if node.name == "end":
        visited.append(node.name)
        return [visited]

    for neighbour in node.neighbours:

        if neighbour.big or neighbour.name not in visited:
            v = visited.copy()
            v.append(node.name)

            p = traverse(neighbour, v)
            if p:
                paths.extend(p)

    return paths


def traverse_pt2(node: Node, visited: List[Node], visited_small: bool):

    if not node.big and node.name in visited:
        visited_small = True

    paths = []
    if node.name == "end":
        visited.append(node.name)
        return [visited]

    for neighbour in node.neighbours:

        if neighbour.big or (neighbour.name not in visited) or (not visited_small):
            v = visited.copy()
            v.append(node.name)

            # if not visited_small and not neighbour.big and :
            # visited_small = True

            p = traverse_pt2(neighbour, v, visited_small)
            if p:
                paths.extend(p)

    return paths


if __name__ == "__main__":
    ex1 = "start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end"
    ex2 = "dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc"
    ex3 = "fs-end\nhe-DX\nfs-he\nstart-DX\npj-DX\nend-zg\nzg-sl\nzg-pj\npj-he\nRW-he\nfs-DX\npj-RW\nzg-RW\nstart-pj\nhe-WI\nzg-he\npj-fs\nstart-RW"

    graph = parse_input(ex1)
    paths = traverse(graph["start"], [])
    assert len(paths) == 10

    graph = parse_input(ex2)
    paths = traverse(graph["start"], [])
    assert len(paths) == 19

    graph = parse_input(ex3)
    paths = traverse(graph["start"], [])
    assert len(paths) == 226

    print(len(paths))

    # Part 2
    graph = parse_input(ex1)
    paths = traverse_pt2(graph["start"], [], False)
    assert len(paths) == 36

    graph = parse_input(ex2)
    paths = traverse_pt2(graph["start"], [], False)
    assert len(paths) == 103

    graph = parse_input(ex3)
    paths = traverse_pt2(graph["start"], [], False)
    assert len(paths) == 3509

    graph = parse_input(real_input())
    paths = traverse_pt2(graph["start"], [], False)
    print(len(paths))
