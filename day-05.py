import pytest


def conv_op(data):
    string = f'{data:05}'
    a, b, c = string[:3]
    de = string[3:]
    return int(a), int(b), int(c), int(de)


@pytest.mark.parametrize('ival,a,b,c,de', (
    (1002, 0, 1, 0, 2),
))
def test_conv_op(ival, a, b, c, de):
    assert conv_op(ival) == (a, b, c, de)


def get_data_mode(data, pos, mode):
    pos = data[pos]

    if mode == 0:
        return data[pos]
    elif mode == 1:
        return pos
    else:
        assert False


def process(data, inp, out):
    current = 0
    n = len(data)
    while 0 <= current < n:
        op = data[current]
        mc, mb, ma, op = conv_op(op)

        if op == 99:
            break
        if op == 1:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            #c = get_data_mode(data, current + 3, mc)
            if mc == 0:
                c = data[current + 3]
                data[c] = a + b
            current += 4
        elif op == 2:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            #c = get_data_mode(data, current + 3, mc)
            if mc == 0:
                c = data[current + 3]
                data[c] = a * b
            current += 4
        elif op == 3:
            i = inp.pop()
            #a = get_data_mode(data, current + 1, ma)
            if ma == 0:
                a = data[current + 1]
                data[a] = i
            current += 2
        elif op == 4:
            #a = get_data_mode(data, current + 1, ma)
            if ma == 0:
                a = data[current + 1]
                out.append(data[a])
            elif ma == 1:
                a = data[current + 1]
                out.append(a)
            current += 2
        elif op == 5:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            if a != 0:
                current = b
            else:
                current += 3
        elif op == 6:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            if a == 0:
                current = b
            else:
                current += 3
        elif op == 7:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            if mc == 0:
                c = data[current + 3]
                data[c] = 1 if a < b else 0
            else:
                assert False
            current += 4
        elif op == 8:
            a = get_data_mode(data, current + 1, ma)
            b = get_data_mode(data, current + 2, mb)
            if mc == 0:
                c = data[current + 3]
                data[c] = 1 if a == b else 0
            else:
                assert False
            current += 4
    return data[0]


def test_example():
    text = '1,9,10,3,2,3,11,0,99,30,40,50'
    data = [int(x) for x in text.split(',')]
    assert process(data, [], []) == 3500


def test_case1():
    with open('day-02.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    data[1] = 12
    data[2] = 2
    assert process(data, [], []) == 6327510


def test_case2():
    with open('day-02.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]

    found = False
    for i in range(0, 99):
        for j in range(0, 99):
            dc = data[:]
            dc[1] = i
            dc[2] = j
            if process(dc, [], []) == 19690720:
                found = True
                break
        if found:
            break
    assert found
    sol = 100 * i + j
    assert sol == 4112


def test_negative():
    text = '1101,100,-1,4,0'
    data = [int(x) for x in text.split(',')]
    process(data, [], [])
    assert data[4] == 99


def test_case_day5_1():
    with open('day-05.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    out = []
    process(data, [1], out)
    for d in out[:-1]:
        assert d == 0
    assert out[-1] == 7566643


@pytest.mark.parametrize('a,b', (
    (4, 999),
    (7, 999),
    (8, 1000),
    (9, 1001),
    (19, 1001),
))
def test_large(a, b):
    text = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    data = [int(x) for x in text.split(',')]
    out = []
    process(data, [a], out)
    assert out == [b]


def test_case_day5_2():
    with open('day-05.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    out = []
    process(data, [5], out)
    assert out[-1] == 9265694
