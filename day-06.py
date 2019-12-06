from itertools import chain


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.weight = None


def build_graph(lines):
    nodes = {}

    def get_node(name):
        if node := nodes.get(name):
            return node
        node = nodes[name] = Node(name)
        return node

    for line in lines:
        a, b = line.strip().split(')')
        a = get_node(a)
        b = get_node(b)
        a.children.append(b)
        assert b.parent is None
        b.parent = a

    return list(nodes.values())


def solve1(nodes):
    def count_parents(node):
        i = 0
        while node := node.parent:
            i += 1
        return i

    n = 0
    for node in nodes:
        n += count_parents(node)
    return n


def solve2(nodes):
    a = next(x for x in nodes if x.name == 'YOU')
    b = next(x for x in nodes if x.name == 'SAN')
    a = a.parent
    b = b.parent

    a.weight = 0
    next_nodes = [a]
    while next_nodes:
        c = next_nodes.pop()
        p = c.weight
        for n in chain(c.children, [c.parent]):
            if n is None:
                continue
            if n.weight is None or n.weight > p + 1:
                n.weight = p + 1
                next_nodes.append(n)
    return b.weight


def test_example():
    lines = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    nodes = build_graph(lines)
    assert solve1(nodes) == 42


def test_case1():
    with open('day-06.txt', 'r') as f:
        lines = f.readlines()
    nodes = build_graph(lines)
    assert solve1(nodes) == 314247


def test_example2():
    lines = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
    ]
    nodes = build_graph(lines)
    assert solve2(nodes) == 4


def test_case2():
    with open('day-06.txt', 'r') as f:
        lines = f.readlines()
    nodes = build_graph(lines)
    assert solve2(nodes) == 514
