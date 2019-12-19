import pytest

day09 = __import__("day-09")
process = day09.process_gen


def builder():
    with open('day-19.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]

    def get_value(x, y):
        assert x >= 0, y >= 0
        inp = [y, x]
        v = next(process(idata, inp))
        return v == 1

    return get_value


def build_map(x, y):
    get_value = builder()

    data = dict()
    for j in range(y):
        for i in range(x):
            value = get_value(i, j)
            ch = '#' if value else '.'
            data[(i, j)] = ch
    return data

def run1():
    data = build_map(50, 50)
    print_map(data)
    ones = [k for k, v in data.items() if v == '#']
    rv = len(ones)
    print(rv)
    return rv


def test_case1():
    assert run1() == 220


def run2():
    check = builder()

    size = 100 - 1
    x, y = 0, size

    # (x, y-s)  (x+s, y-s)
    # (x, y)    (x+s, y)

    while True:
        while not check(x, y):
            x += 1

        if check(x + size, y - size) and check(x, y-size) and check(x+size, y):
            rv = x*10000 + (y - size)
            print(rv)
            return rv
        y += 1


def test_case2():
    assert run2() == 10010825


def print_map(data):
    xmin = min(k[0] for k in data.keys())
    xmax = max(k[0] for k in data.keys())
    ymin = min(k[1] for k in data.keys()) 
    ymax = max(k[1] for k in data.keys())
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            ch = data.get((x, y), 'x')
            print(ch, end='')
        print()


if __name__ == '__main__':
    run2()
