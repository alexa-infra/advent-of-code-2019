import pytest
import string
from heapq import heappush, heappop


diff = ((1, 0), (-1, 0), (0, 1), (0, -1))

def build_map(lines):
    portals = []
    data = dict()
    for j, line in enumerate(lines):
        for i, ch in enumerate(line):
            if ch == ' ' or ch == '\n':
                continue
            p = (i, j)
            data[p] = ch
            if ch in string.ascii_uppercase:
                portals.append(p)

    def find_around(p, symbols):
        for d in diff:
            pp = p[0] + d[0], p[1] + d[1]
            v = data.get(pp)
            if v and v in symbols:
                return pp
        return None

    xmin = min(k[0] for k in data.keys())
    xmax = max(k[0] for k in data.keys())
    ymin = min(k[1] for k in data.keys()) 
    ymax = max(k[1] for k in data.keys())
    limits = (xmin, xmax, ymin, ymax)

    start, end = None, None
    outer = set()
    inner = set()
    for i, j in portals:
        p1 = (i, j)
        v1 = data.get(p1)
        if not v1 or len(v1) > 1:
            continue

        p2 = find_around(p1, string.ascii_uppercase)
        v2 = data.get(p2)
        if not v2 or len(v2) > 1:
            continue

        coords = (p1[0], p1[1], p2[0], p2[1])
        is_outer = any(c in limits for c in coords)

        if p1[0] == p2[0]:
            if p1[1] > p2[1]:
                name = v2 + v1
            else:
                name = v1 + v2
        elif p1[1] == p2[1]:
            if p1[0] > p2[0]:
                name = v2 + v1
            else:
                name = v1 + v2
        else:
            assert False

        f1 = find_around(p1, '.')
        f2 = find_around(p2, '.')
        if f1 is None:
            assert f2 is not None
            data[p2] = name
            del data[p1]
            if name == 'AA':
                start = p2
            elif name == 'ZZ':
                end = p2
            elif is_outer:
                outer.add((name, p2))
            else:
                inner.add((name, p2))
        else:
            assert f2 is None
            data[p1] = name
            del data[p2]
            if name == 'AA':
                start = p1
            elif name == 'ZZ':
                end = p1
            elif is_outer:
                outer.add((name, p1))
            else:
                inner.add((name, p1))
    return {
        'map': data,
        'start': start,
        'end': end,
        'inner': inner,
        'outer': outer,
    }


def print_map(data, path):
    xmin = min(k[0] for k in data.keys())
    xmax = max(k[0] for k in data.keys())
    ymin = min(k[1] for k in data.keys()) 
    ymax = max(k[1] for k in data.keys())
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            p = (x, y)
            if p in path:
                ch = 'x'
            else:
                ch = data.get(p, ' ')
                if len(ch) > 1:
                    ch = 'O'
            print(ch, end='')
        print()


def solve(data):
    mmap = data['map']

    def find_portal(name, pos):
        return next((k for k, v in mmap.items() if v == name and k != pos), None)

    visited = set()

    h = []
    start = data['start']
    end = data['end']
    heappush(h, (0, start))
    while h:
        steps, pos = heappop(h)
        if pos in visited:
            continue
        visited.add(pos)

        name = mmap[pos]
        if len(name) > 1:
            portal = find_portal(name, pos)
            if portal:
                pos = portal
                if pos in visited:
                    continue
                visited.add(pos)

        if pos == end:
            return steps - 1

        for d in diff:
            pp = pos[0] + d[0], pos[1] + d[1]
            vv = mmap.get(pp)
            if vv is None or vv == '#':
                continue

            heappush(h, (steps + 1 if vv == '.' else steps, pp))


@pytest.mark.parametrize('filename,steps', (
    ('day-20-1.txt', 23),
    ('day-20-2.txt', 58),
    ('day-20.txt', 626),
))
def test_case1(filename, steps):
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = build_map(lines)
    assert solve(data) == steps


def solve_r(data):
    mmap = data['map']
    start = data['start']
    end = data['end']
    inner = data['inner']
    outer = data['outer']

    visited = set()
    h = []
    heappush(h, (0, 0, start))
    while h:
        steps, level, pos = heappop(h)

        kk = level, pos[0], pos[1]
        if kk in visited:
            continue
        visited.add(kk)

        name = mmap[pos]
        if len(name) > 1 and name not in ('AA', 'ZZ'):
            if (name, pos) in outer:
                _, pos = next(p for p in inner if p[0] == name)
                level -= 1
                assert level >= 0

                kk = level, pos[0], pos[1]
                if kk in visited:
                    continue
                visited.add(kk)
            elif (name, pos) in inner:
                _, pos = next(p for p in outer if p[0] == name)
                level += 1

                kk = level, pos[0], pos[1]
                if kk in visited:
                    continue
                visited.add(kk)
            else:
                assert False, name

        if pos == end and level == 0:
            print('steps', steps - 1)
            return steps - 1

        for d in diff:
            pp = pos[0] + d[0], pos[1] + d[1]
            vv = mmap.get(pp)
            if vv is None or vv == '#':
                continue

            if vv == '.':
                heappush(h, (steps + 1, level, pp))
                continue

            if (vv, pp) in outer and level > 0:
                heappush(h, (steps, level, pp))
                continue

            if (vv, pp) in inner:
                heappush(h, (steps, level, pp))
                continue

            if vv in ('AA', 'ZZ') and level == 0:
                heappush(h, (steps, level, pp))


@pytest.mark.parametrize('filename,steps', (
    ('day-20-1.txt', 26),
    #('day-20-2.txt', None),
    ('day-20-3.txt', 396),
    ('day-20.txt', 6912),
))
def test_case2(filename, steps):
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = build_map(lines)
    assert solve_r(data) == steps


if __name__ == '__main__':
    test_case2()
