day09 = __import__("day-09")
process = day09.process_gen


def builder(lines):
    with open('day-21.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]

    text = '\n'.join(lines + [''])
    inp = [ord(x) for x in reversed(text)]
    out = list(process(idata, inp))
    print(''.join(chr(x) for x in out[:-1]))
    return out[-1]


def test_case1():
    """
    Jump = D and (!A or !B or !C)
    """
    lines = [
        'NOT A T',
        'OR T J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK',
    ]
    assert builder(lines) == 19361332


def test_case2():
    """
    Jump = D and (!A or !B or !C) and (E or H)
    """
    lines = [
        # 1. exactly first case
        'NOT A T',
        'OR T J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        # 2. now we clear registor T
        'AND T T',
        'NOT T T',
        # 3. second part 
        'OR E T',
        'OR H T',
        'AND T J',
        'RUN',
    ]
    assert builder(lines) == 1143351187


if __name__ == '__main__':
    run2()
