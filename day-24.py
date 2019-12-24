import io
import collections

case = [
    "#.#.#",
    "..#..",
    ".#.##",
    ".####",
    "###..",
]

example = [
    "....#",
    "#..#.",
    "#..##",
    "..#..",
    "#....",
]

dirs_ = {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0),}

def get_adjacent_r(p, lvl):
    """
    01234
  0 xxxxx
  1 x.x.x
  2 xx?xx
  3 x.x.x
  4 xxxxx
    """
    rv = []
    center = (2, 2)
    for name, d in dirs_.items():
        k = p[0] + d[0], p[1] + d[1]
        if k == center:
            if name == 'u':
                for x in range(0, 5):
                    rv.append((x, 4, lvl-1))
            elif name == 'd':
                for x in range(0, 5):
                    rv.append((x, 0, lvl-1))
            elif name == 'l':
                for y in range(0, 5):
                    rv.append((4, y, lvl-1))
            elif name == 'r':
                for y in range(0, 5):
                    rv.append((0, y, lvl-1))
        elif k[0] < 0 or k[0] > 4 or k[1] < 0 or k[1] > 4:
            rv.append((center[0] + d[0], center[1] + d[1], lvl+1))
        else:
            rv.append((k[0], k[1], lvl))
    return rv


def make_map(lines):
    data = dict()
    for j, line in enumerate(lines):
        for i, ch in enumerate(line):
            data[(i, j)] = ch
    return data

neignbors = ((1, 0), (-1, 0), (0, 1), (0, -1))

def mutate(data):
    ndata = dict()
    for k, v in data.items():
        bugs_around = 0
        empty_around = 0
        for n in neignbors:
            p = k[0] + n[0], k[1] + n[1]
            v1 = data.get(p, '.')
            if v1 == '.':
                empty_around += 1
            elif v1 == '#':
                bugs_around += 1
        if v == '#' and bugs_around in (0, 2, 3, 4):
            ndata[k] = '.'
        elif v == '.' and bugs_around in (1, 2):
            ndata[k] = '#'
        else:
            ndata[k] = v
    return ndata

def mutate2(rdata, lvl):
    data = rdata[lvl]
    ndata = dict()
    for k, v in data.items():
        if k == (2, 2):
            ndata[k] = '?'
            continue
        bugs_around = 0
        empty_around = 0
        for p1, p2, n_lvl in get_adjacent_r(k, lvl):
            p = (p1, p2)
            v1 = rdata[n_lvl].get(p, '.')
            if v1 == '.':
                empty_around += 1
            elif v1 == '#':
                bugs_around += 1
        assert empty_around + bugs_around in (4, 8)
        if v == '#' and bugs_around in (0, 2, 3, 4, 5, 6, 7, 8):
            ndata[k] = '.'
        elif v == '.' and bugs_around in (1, 2):
            ndata[k] = '#'
        else:
            ndata[k] = v
    return ndata

def map_to_text(data):
    out = io.StringIO()
    for j in range(5):
        for i in range(5):
            ch = data[(i, j)]
            out.write(ch)
        out.write('\n')
    return out.getvalue()

def map_rating(data):
    c = 1
    rv = 0
    for j in range(5):
        for i in range(5):
            if data[(i, j)] == '#':
                rv += c
            c *= 2
    return rv

def solve(lines):
    data = make_map(lines)
    cache = set()
    while True:
        m = map_to_text(data)
        if m in cache:
            break
        cache.add(m)
        data = mutate(data)
    return map_rating(data)


def test_example():
    assert solve(example) == 2129920

def test_case1():
    assert solve(case) == 14539258


def solve2(lines, n):
    make_default = lambda: {(i, j): '.' for i in range(5) for j in range(5)}
    rdata = collections.defaultdict(make_default)
    rdata[0] = make_map(lines)
    for i in range(n):
        m = i // 2 + 1
        rdata2 = collections.defaultdict(make_default)
        for lvl in range(-m, m+1):
            rdata2[lvl] = mutate2(rdata, lvl)
        rdata = rdata2
    return count_bugs(rdata)

def count_bugs(rdata):
    n = 0
    for k, v in sorted(rdata.items()):
        #print('depth', k)
        n += len(list(x for x in v.values() if x == '#'))
        #txt = map_to_text(v)
        #print(txt)
        #print('-' * 20)
    return n

def test_example2():
    assert solve2(example, 10) == 99


def test_case2():
    assert solve2(case, 200) == 1977


if __name__ == '__main__':
    example_run()
