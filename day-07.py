from itertools import permutations, cycle
import pytest
day05 = __import__("day-05")


conv_op = day05.conv_op
get_data_mode = day05.get_data_mode


def terminator(data):
    def term(inp, phase):
        idata = data[:]
        outp = []
        g = process_gen(idata, [inp, phase], outp)
        s = next(g)
        assert s == "output"
        return outp[-1]
    m = None
    for state in permutations(range(5), 5):
        signal = 0
        for phase in state:
            signal = term(signal, phase)
        if m is None or signal > m:
            m = signal
    return m


@pytest.mark.parametrize('text,value', (
    ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", 43210),
    ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", 54321),
    ("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", 65210),
))
def test_example(text, value):
    data = [int(x) for x in text.split(',')]
    assert terminator(data) == value


def test_case1():
    with open('day-07.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    assert terminator(data) == 38834


def process_gen(data, inp, out):
    current = 0
    n = len(data)
    while 0 <= current < n:
        op = data[current]
        mc, mb, ma, op = conv_op(op)

        if op == 99:
            return
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
            if not inp:
                yield "input"
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
            yield "output"
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
    assert False


def terminator1000(data):
    def term(phase):
        idata = data[:]
        inp = [phase]
        out = []
        g = process_gen(idata, inp, out)
        def push(i):
            inp.append(i)
        s = next(g)
        assert s == "input"
        return g, push, out

    def run(state):
        devices = [term(phase) for phase in state]

        signal = 0
        for g, push, out in cycle(devices):
            push(signal)
            it = next(g, None)
            if it is None:
                break
            assert it == "output"
            signal = out[-1]

        _, _, output = devices[-1]
        return output[-1]

    m = None
    for state in permutations(range(5, 10), 5):
        v = run(state)
        if m is None or v > m:
            m = v
    return m


@pytest.mark.parametrize('text,value', (
    ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", 139629729),
    ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", 18216),
))
def test_example2(text, value):
    data = [int(x) for x in text.split(',')]
    assert terminator1000(data) == value


def test_case2():
    with open('day-07.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    assert terminator1000(data) == 69113332
