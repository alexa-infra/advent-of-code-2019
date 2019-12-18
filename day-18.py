import itertools
import string
import pytest
from heapq import heappush, heappop


def get_map_items(mmap, items):
    return {v: k for k, v in mmap.items() if v in items}


def build_map(lines):
    data = dict()
    for j, line in enumerate(lines):
        for i, ch in enumerate(line):
            data[(i, j)] = ch
    keys = get_map_items(data, string.ascii_lowercase)
    doors = get_map_items(data, string.ascii_uppercase)
    entrances = [k for k, v in data.items() if v == '@']
    for pos in entrances:
        data[pos] = '.'
    return {
        'map': data,
        'keys': keys,
        'doors': doors,
        'entrances': entrances,
    }


directions = ((1, 0), (-1, 0), (0, 1), (0, -1))


def find_available_keys(data, own_keys, pos):
    keys = dict()

    h = []
    heappush(h, (0, pos[0], pos[1]))
    v = set()
    while h:
        idx, x, y = heappop(h)
        p = (x, y)
        if p in v:
            continue
        v.add(p)

        for d in directions:
            np = p[0] + d[0], p[1] + d[1]
            ch = data['map'].get(np)

            if ch is None or ch == '#':
                continue

            if ch == '.':
                heappush(h, (idx + 1, np[0], np[1]))
                continue

            if ch in own_keys or ch.lower() in own_keys:
                heappush(h, (idx + 1, np[0], np[1]))
                continue

            if ch in string.ascii_lowercase:
                keys[ch] = idx + 1
    return keys


def flatten(points):
    return tuple(itertools.chain(*points))


def solve(lines):
    data = build_map(lines)
    starts = data['entrances']
    h = []
    heappush(h, (0, '', starts))
    cache = set()
    while h:
        steps, own_keys, starts = heappop(h)

        kk = flatten(starts), ''.join(sorted(own_keys))
        if kk in cache:
            continue
        cache.add(kk)

        found = False
        for i, start in enumerate(starts):
            keys = find_available_keys(data, own_keys, start)

            for k, d in keys.items():
                key_pos = data['keys'][k]
                new_starts = [key_pos if j == i else pos for j, pos in enumerate(starts)]
                heappush(h, (steps + d, own_keys + k, new_starts))
                found = True
        if not found:
            return steps


def test_run1():
    lines = [
        '#########',
        '#b.A.@.a#',
        '#########',
    ]
    assert solve(lines) == 8


def test_run2():
    lines = [
        '########################',
        '#f.D.E.e.C.b.A.@.a.B.c.#',
        '######################.#',
        '#d.....................#',
        '########################',
    ]
    assert solve(lines) == 86


def test_run3():
    lines = [
        '########################',
        '#...............b.C.D.f#',
        '#.######################',
        '#.....@.a.B.c.d.A.e.F.g#',
        '########################',
    ]
    assert solve(lines) == 132


def test_run4():
    lines = [
        '#################',
        '#i.G..c...e..H.p#',
        '########.########',
        '#j.A..b...f..D.o#',
        '########@########',
        '#k.E..a...g..B.n#',
        '########.########',
        '#l.F..d...h..C.m#',
        '#################',
    ]
    assert solve(lines) == 136


def test_run5():
    lines = [
        '#############',
        '#g#f.D#..h#l#',
        '#F###e#E###.#',
        '#dCba@#@BcIJ#',
        '#############',
        '#nK.L@#@G...#',
        '#M###N#H###.#',
        '#o#m..#i#jk.#',
        '#############',
    ]
    assert solve(lines) == 72


def test_case1():
    with open('day-18.txt', 'r') as f:
        lines = f.readlines()
    assert solve(lines) == 3918


def test_case2():
    with open('day-18-2.txt', 'r') as f:
        lines = f.readlines()
    assert solve(lines) == 2004


if __name__ == '__main__':
    test_case1()
    #test_case2()
