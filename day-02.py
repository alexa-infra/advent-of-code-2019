import pytest


def process(data):
    current = 0
    n = len(data)
    while 0 <= current < n:
        op = data[current]
        if op == 99:
            break
        if op == 1:
            a, b, c = data[current + 1:current + 4]
            data[c] = data[a] + data[b]
        elif op == 2:
            a, b, c = data[current + 1:current + 4]
            data[c] = data[a] * data[b]
        current += 4
    return data[0]


def test_example():
    text = '1,9,10,3,2,3,11,0,99,30,40,50'
    data = [int(x) for x in text.split(',')]
    assert process(data) == 3500


def test_case1():
    with open('day-02.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    data[1] = 12
    data[2] = 2
    assert process(data) == 6327510


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
            if process(dc) == 19690720:
                found = True
                break
        if found:
            break
    assert found
    sol = 100 * i + j
    assert sol == 4112
