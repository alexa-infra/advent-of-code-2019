from collections import defaultdict
import pytest
day05 = __import__("day-05")
conv_op = day05.conv_op


def get_data_mode(data, pos, mode, rel_base):
    pos = data[pos]

    if mode == 0:
        return data[pos]
    elif mode == 1:
        return pos
    elif mode == 2:
        return data[pos + rel_base]
    else:
        assert False


def set_data_mode(data, pos, mode, rel_base, value):
    pos = data[pos]

    if mode == 0:
        data[pos] = value
    elif mode == 1:
        assert False
        pass
    elif mode == 2:
        data[pos + rel_base] = value
    else:
        assert False


def process_gen(data, inp):
    dd = defaultdict(int)
    for i, x in enumerate(data):
        dd[i] = x

    current = 0
    rel_base = 0
    getter = lambda pos, mode: get_data_mode(dd, pos, mode, rel_base)
    setter = lambda pos, mode, value: set_data_mode(dd, pos, mode, rel_base, value)

    while True:
        op = data[current]
        mc, mb, ma, op = conv_op(op)

        if op == 99:
            return
        if op == 1:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            setter(current + 3, mc, a + b)
            current += 4
        elif op == 2:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            setter(current + 3, mc, a * b)
            current += 4
        elif op == 3:
            i = inp.pop()
            setter(current + 1, ma, i)
            current += 2
        elif op == 4:
            a = getter(current + 1, ma)
            yield a
            current += 2
        elif op == 5:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            if a != 0:
                current = b
            else:
                current += 3
        elif op == 6:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            if a == 0:
                current = b
            else:
                current += 3
        elif op == 7:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            setter(current + 3, mc, 1 if a < b else 0)
            current += 4
        elif op == 8:
            a = getter(current + 1, ma)
            b = getter(current + 2, mb)
            setter(current + 3, mc, 1 if a == b else 0)
            current += 4
        elif op == 9:
            a = getter(current + 1, ma)
            rel_base += a
            current += 2
    assert False


def test_example1():
    text = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    data = [int(x) for x in text.split(',')]
    out = [x for x in process_gen(data, [])]
    assert out == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]


def test_example2():
    text = "1102,34915192,34915192,7,4,7,99,0"
    data = [int(x) for x in text.split(',')]
    out = [x for x in process_gen(data, [])]
    assert len(out) == 1
    xx = out[0]
    assert len(str(xx)) == 16


def test_example3():
    text = "104,1125899906842624,99"
    data = [int(x) for x in text.split(',')]
    out = [x for x in process_gen(data, [])]
    assert out == [1125899906842624]


def test_case1():
    with open('day-09.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    out = [x for x in process_gen(data, [1])]
    assert out == [3241900951]


def test_case1():
    with open('day-09.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    out = [x for x in process_gen(data, [2])]
    assert out == [83089]
