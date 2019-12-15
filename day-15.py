from heapq import heappush, heappop

day09 = __import__("day-09")
process = day09.process_gen


diffs = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0),
}


diffs_rev = {v: k for k, v in diffs.items()}


def scanner(ttest):
    data = dict()
    data[(0, 0)] = 'X'
    path = [(0, 0)]
    while True:
        current = path[-1]

        for code, dd in diffs.items():
            next_coord = current[0] + dd[0], current[1] + dd[1]
            if next_coord in data:
                continue
            resp = ttest(code)
            if resp == 0:
                data[next_coord] = '#'
                continue
            elif resp == 1:
                data[next_coord] = '.'
            elif resp == 2:
                data[next_coord] = 'O'
            path.append(next_coord)
            break
        else:
            path.pop()
            if not path:
                break
            prev = path[-1]
            dd = prev[0] - current[0], prev[1] - current[1]
            a = ttest(diffs_rev[dd])
            assert a in (1, 2)
    return data


def find_min(mmap, cc):
    h = []
    heappush(h, (0, cc[0], cc[1]))
    v = set()
    while True:
        idx, x, y = heappop(h)
        coord = (x, y)
        if coord in v:
            continue
        v.add(coord)

        ch = mmap.get(coord, ' ')
        if ch in ('#', ' '):
            continue

        if ch in ('.', 'X'):
            for _, dd in diffs.items():
                next_coord = coord[0] + dd[0], coord[1] + dd[1]
                if next_coord in mmap and next_coord not in v:
                    heappush(h, (idx + 1, next_coord[0], next_coord[1]))
            continue

        if ch == 'O':
            return idx
        assert False


def find_max(mmap, cc):
    h = []
    heappush(h, (0, cc[0], cc[1]))
    v = set()
    m = None
    while h:
        idx, x, y = heappop(h)
        if m is None or idx > m:
            m = idx
        coord = (x, y)
        if coord in v:
            continue
        v.add(coord)

        ch = mmap.get(coord, ' ')
        if ch in ('#', ' '):
            continue

        if ch in ('.', 'X', 'O'):
            for _, dd in diffs.items():
                next_coord = coord[0] + dd[0], coord[1] + dd[1]
                if next_coord in mmap and next_coord not in v:
                    heappush(h, (idx + 1, next_coord[0], next_coord[1]))
            continue
        assert False
    return m


def build_map(text):
    idata = [int(x) for x in text.split(',')]

    inp = []
    g = process(idata, inp)
    def ttest(x):
        inp.append(x)
        return next(g)

    return scanner(ttest)


def print_map(mmap):
    xmin = min(k[0] for k in mmap.keys())
    xmax = max(k[0] for k in mmap.keys())
    ymin = min(k[1] for k in mmap.keys()) 
    ymax = max(k[1] for k in mmap.keys())
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            ch = mmap.get((x, y), ' ')
            print(ch, end='')
        print()


def test_case1():
    with open('day-15.txt', 'r') as f:
        text = f.read().strip()

    mmap = build_map(text)
    assert find_min(mmap, (0, 0)) == 218


def test_case2():
    with open('day-15.txt', 'r') as f:
        text = f.read().strip()

    mmap = build_map(text)
    oxy = next(k for k, v in mmap.items() if v == 'O')
    assert find_max(mmap, oxy) == 544
