import math
from itertools import cycle
import pytest


def read_map(lines):
    data = set()
    for j, line in enumerate(lines):
        for i, ch in enumerate(line.strip()):
            p = (i, j)
            if ch == '#':
                data.add(p)
    return data


def vectoring(a, b):
    x1, y1 = a
    x2, y2 = b
    return x2 - x1, y2 - y1


def sign(a):
    return 1 if a >= 0 else -1


def cmp_v(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    # v2 = a * v1
    # (x1, y1) = (a * x2, a * y2)
    # a = x1 / x2 = y1 / y2
    if x2 != 0 and y2 != 0:
        a = x1 / x2
        a1 = y1 / y2
        return a == a1, sign(a)

    if x2 == 0:
        # (x1, y1) = (a * 0, a * y2)
        # a = y1 / y2
        return x1 == 0, sign(y1 / y2)

    if y2 == 0:
        return y1 == 0, sign(x1 / x2)

    assert False


def count_visible(data, center):
    vectors = []
    for p in data:
        if p == center:
            continue
        v = vectoring(center, p)

        found = False
        for w, dd in vectors:
            equal, d = cmp_v(v, w)
            if equal and dd == d:
                found = True
                break

        if not found:
            if (v, 1) in vectors:
                vectors.append((v, -1))
            else:
                vectors.append((v, 1))
    return len(vectors)


def distance(a, b):
    return abs(a[0] - b[0]), abs(a[1] - b[1])


def get_visible_vectors(data, center):
    vectors = []
    for p in data:
        if p == center:
            continue
        v = vectoring(center, p)

        found = False
        for w, dd in vectors:
            equal, d = cmp_v(v, w)
            if equal and dd == d:
                found = True
                break

        if not found:
            if (v, 1) in vectors:
                vectors.append((v, -1))
            else:
                vectors.append((v, 1))
    return vectors


def resort_vectors(vectors):
    vectors = [(x * d, y * d) for (x, y), d in vectors]
    return sorted(vectors, key=lambda v: -math.atan2(v[0], v[1]))


def get_next_by_vector(v, data, center):
    pp = None
    for p in data:
        if p == center:
            continue
        w = vectoring(center, p)

        equal, d = cmp_v(w, v)
        if equal and d > 0:
            if pp is None or distance(center, p) < distance(center, pp):
                pp = p
    return pp


def laser(data, center):
    vectors = get_visible_vectors(data, center)
    vectors = resort_vectors(vectors)

    n = 0
    for v in cycle(vectors):
        p = get_next_by_vector(v, data, center)
        if not p:
            continue
        data.remove(p)
        n += 1
        if n == 200:
            return p


def find_max(data):
    m = None
    for p in data:
        n = len(get_visible_vectors(data, p))
        if m is None or n > m:
            m = n
    return m


def test_example1():
    lines = [
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ]
    data = read_map(lines)
    assert find_max(data) == 8


def test_example2():
    lines = [
        "......#.#.",
        "#..#.#....",
        "..#######.",
        ".#.#.###..",
        ".#..#.....",
        "..#....#.#",
        "#..#....#.",
        ".##.#..###",
        "##...#..#.",
        ".#....####",
    ]
    data = read_map(lines)
    assert find_max(data) == 33


def test_case1():
    with open('day-10.txt', 'r') as f:
        lines = f.readlines()
    data = read_map(lines)
    assert find_max(data) == 230


@pytest.mark.parametrize('c,p,r', (
    ((3, 3), (3, 0), math.pi),
    ((3, 3), (6, 3), math.pi / 2),
    ((3, 3), (3, 6), 0),
    ((3, 3), (0, 3), -math.pi / 2),
    ((3, 3), (0, 0), -math.pi * 3/4),
))
def test_tan(c, p, r):
    """
    0123456
   0#######
   1#.....#
   2#.....#
   3#..x..#
   4#.....#
   5#.....#
   6#######
    """
    x1, y1 = c
    x2, y2 = p
    v = x2 - x1, y2 - y1
    assert math.atan2(v[0], v[1]) == pytest.approx(r)


def test_case2():
    cc = (19, 11)

    with open('day-10.txt', 'r') as f:
        lines = f.readlines()
    data = read_map(lines)
    p = laser(data, cc)
    assert p[0] * 100 + p[1] == 1205
