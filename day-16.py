import itertools
import pytest

mod10 = lambda x: x if x < 10 else x % 10


def parse(text):
    return [int(ch) for ch in text.strip()]


base = [0, 1, 0, -1]

phase_cache = {}

def phase(n):
    if n in phase_cache:
        return phase_cache[n]
    el = (itertools.repeat(x, n) for x in base)
    p = list(itertools.chain(*el))
    rv = p[1:] + [p[0]]
    phase_cache[n] = rv
    return rv


@pytest.mark.parametrize('iphase,seq', (
    (1, [1, 0, -1, 0]),
    (2, [0, 1, 1, 0, 0, -1, -1, 0]),
    (3, [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0]),
    (4, [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, -1, -1, -1, -1, 0]),
))
def test_phase(iphase, seq):
    assert phase(iphase) == seq


def phase_iter(data, n):
    len_seq = n * 4
    n_repeats = len(data) // len_seq
    for i in range(n_repeats):
        start = i * len_seq + (n - 1)
        for j in range(n):
            yield data[start + j], 1
        start = start + 2 * n
        for j in range(n):
            yield data[start + j], -1
    rest = data[n_repeats * len_seq:]
    for a, b in zip(rest, phase(n)):
        if b == 0:
            continue
        yield a, b


import collections

def calc(idata, i):
    #p = phase(i)

    d = collections.defaultdict(int)
    #for a, b in zip(idata, itertools.cycle(p)):
    for a, b in phase_iter(idata, i):
        if a == 0:
            continue
        if b == -1:
            d[a] -= 1
        elif b == 1:
            d[a] += 1

    s = sum(k * v for k, v in d.items())
    return abs(s) % 10


def solve(idata, n):
    for i in range(n):
        idata = list(calc(idata, x + 1) for x in range(len(idata)))
    return idata

@pytest.mark.parametrize('inp,n,out', (
    ('12345678', 1, '48226158'),
    ('12345678', 2, '34040438'),
    ('12345678', 3, '03415518'),
    ('12345678', 4, '01029498'),
))
def test_solve(inp, n, out):
    idata = parse(inp)
    idata = solve(idata, n)
    assert ''.join(str(ch) for ch in idata) == out


@pytest.mark.parametrize('inp,out', (
    ('80871224585914546619083218645595', '24176176'),
    ('19617804207202209144916044189917', '73745418'),
    ('69317163492948606335995924319873', '52432133'),
))
def test_solve_100_first8(inp, out):
    idata = parse(inp)
    idata = solve(idata, 100)
    assert ''.join(str(ch) for ch in idata[:8]) == out


def _test_case1():
    with open('day-16.txt', 'r') as f:
        text = f.read()
    idata = parse(text)
    idata = solve(idata, 100)
    assert ''.join(str(ch) for ch in idata[:8]) == '29956495'

def part2(input):
    skip = int(input[0:7])
    digits = [int(i) for i in input] * 10000

    # confirm that only the first 2 elements of the pattern will be used:
    assert(len(digits) < 2*skip - 1)

    for phase in range(100):
        checksum = sum(digits[skip:])
        new_digits = [0]*skip + [int(str(checksum)[-1])]
        for n in range(skip+2, len(digits)+1):
            checksum -= digits[n-2]
            new_digits += [int(str(checksum)[-1])]
        digits = new_digits

    return ''.join(str(i) for i in digits[skip:(skip+8)])

@pytest.mark.parametrize('inp,out', (
    ('03036732577212944063491565474664', '84462026'),
))
def test_example12(inp, out):
    assert part2(inp) == out

def test_case2():
    with open('day-16.txt', 'r') as f:
        text = f.read().strip()
    assert part2(text) == '73556504'
