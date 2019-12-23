import itertools
from collections import defaultdict
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

        get_a = lambda: getter(current + 1, ma)
        get_b = lambda: getter(current + 2, mb)
        set_a = lambda x: setter(current + 1, ma, x)
        set_c = lambda x: setter(current + 3, mc, x)

        if op == 99:
            return
        if op == 1:
            a, b = get_a(), get_b()
            set_c(a + b)
            current += 4
        elif op == 2:
            a, b = get_a(), get_b()
            set_c(a * b)
            current += 4
        elif op == 3:
            if not inp:
                yield "input", None
            i = inp.pop()
            set_a(i)
            current += 2
        elif op == 4:
            a = get_a()
            yield "output", a
            current += 2
        elif op == 5:
            a, b = get_a(), get_b()
            current = b if a != 0 else current + 3
        elif op == 6:
            a, b = get_a(), get_b()
            current = b if a == 0 else current + 3
        elif op == 7:
            a, b = get_a(), get_b()
            set_c(1 if a < b else 0)
            current += 4
        elif op == 8:
            a, b = get_a(), get_b()
            set_c(1 if a == b else 0)
            current += 4
        elif op == 9:
            a = get_a()
            rel_base += a
            current += 2
    assert False

def get_intcode():
    with open('day-23.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]
    return idata


def builder(idata):
    inp = []
    g = process_gen(idata, inp) 
    def push(v):
        inp.append(v)
    return g, push

def run():
    idata = get_intcode()
    data = [None] * 50
    for i in range(50):
        g, push = data[i] = builder(idata)
        push(i)

    for g, push in itertools.cycle(data):
        name, v = next(g)
        if name == 'input':
            push(-1)
        elif name == 'output':
            packet_for = v
            _, a = next(g)
            _, b = next(g)

            if packet_for == 255:
                return b

            g1, push1 = data[packet_for]
            push1(b)
            push1(a)


def test_case1():
    assert run() == 16250


def run2():
    idata = get_intcode()
    data = [None] * 50
    for i in range(50):
        g, push = data[i] = builder(idata)
        push(i)

    nat = None
    nat_y_prev = None
    idle = 0

    for g, push in itertools.cycle(data):
        if idle >= 100:
            a, b = nat
            if nat_y_prev and nat_y_prev == b:
                return nat_y_prev
            nat_y_prev = b

            g1, push1 = data[0]
            push1(b)
            push1(a)

            nat = None
            idle = 0
            continue

        name, v = next(g)
        if name == 'input':
            push(-1)
            idle += 1
        elif name == 'output':
            idle = 0
            packet_for = v
            _, a = next(g)
            _, b = next(g)

            if packet_for == 255:
                nat = (a, b)
                continue

            g1, push1 = data[packet_for]
            push1(b)
            push1(a)

def test_case2():
    assert run2() == 11046


if __name__ == '__main__':
    r = run2()
    print(r)
