import pytest


dirs_ = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

def build_path(data, path):
    c = (0, 0)
    j = 1
    for p in path:
        d, n = p[0], p[1:]
        d = dirs_[d]
        n = int(n)
        for i in range(n):
            c = c[0] + d[0], c[1] + d[1]
            if c not in data:
                data[c] = j
            j += 1


def dist(p):
    return abs(p[0]) + abs(p[1])


def find_inter(data1, data2):
    m = None
    for p in data1.keys():
        if p in data2:
            d = dist(p)
            if m is None or d < m:
                m = d
    return m


def find_inter2(data1, data2):
    m = None
    for p in data1.keys():
        if p in data2:
            v = data1[p] + data2[p]
            if m is None or v < m:
                m = v
    return m


def solve(lines):
    data1 = dict()
    build_path(data1, lines[0].strip().split(','))
    data2 = dict()
    build_path(data2, lines[1].strip().split(','))
    return find_inter(data1, data2)


def solve2(lines):
    data1 = dict()
    build_path(data1, lines[0].strip().split(','))
    data2 = dict()
    build_path(data2, lines[1].strip().split(','))
    return find_inter2(data1, data2)


@pytest.mark.parametrize('lines,n', (
    (
        [
            "R8,U5,L5,D3",
            "U7,R6,D4,L4",
        ],
        6
    ),
    (
        [
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
        ],
        159
    ),
))
def test_example(lines, n):
    assert solve(lines) == n


@pytest.mark.parametrize('lines,n', (
    (
        [
            "R8,U5,L5,D3",
            "U7,R6,D4,L4",
        ],
        30
    ),
    (
        [
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83",
        ],
        610
    ),
))
def test_example2(lines, n):
    assert solve2(lines) == n


def test_case1():
    with open('day-03.txt', 'r') as f:
        lines = f.readlines()
    assert solve(lines) == 308


def test_case2():
    with open('day-03.txt', 'r') as f:
        lines = f.readlines()
    assert solve2(lines) == 12934


if __name__ == '__main__':
    test_case1()
