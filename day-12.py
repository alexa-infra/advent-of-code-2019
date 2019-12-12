import math

import itertools
import functools


def read_input(lines):
    def conv(line):
        line = line.strip()[1:-1]
        xp, yp, zp = line.split(', ')
        x, y, z = xp[2:], yp[2:], zp[2:]
        return [int(x), int(y), int(z)], [0, 0, 0]
    return [conv(line) for line in lines]


def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1


def step(moons):
    positions = [p for p, v in moons]
    for i in range(3):
        for p in positions:
            for pp, vv in moons:
                vv[i] += sign(p[i] - pp[i])
    for i in range(3):
        for pp, vv in moons:
            pp[i] += vv[i]


def moon_energy(p, v):
    pot = sum(abs(x) for x in p)
    kin = sum(abs(x) for x in v)
    return pot * kin


def energy(moons):
    return sum(moon_energy(p, v) for p, v in moons)


def test_example1():
    lines = [
        "<x=-1, y=0, z=2>",
        "<x=2, y=-10, z=-7>",
        "<x=4, y=-8, z=8>",
        "<x=3, y=5, z=-1>",
    ]
    data = read_input(lines)
    for i in range(10):
        step(data)
    assert energy(data) == 179


def test_case1():
    with open('day-12.txt', 'r') as f:
        lines = f.readlines()
    data = read_input(lines)
    for i in range(1000):
        step(data)
    assert energy(data) == 7138


def flat_state(moons, axis):
    m1, m2, m3, m4 = moons
    p1, v1 = m1
    p2, v2 = m2
    p3, v3 = m3
    p4, v4 = m4
    return (
        p1[axis], p2[axis], p3[axis], p4[axis],
        v1[axis], v2[axis], v3[axis], v4[axis],
    )


def find_cycle_axis(data, axis):
    initial = flat_state(data, axis)

    for i in itertools.count(1):
        step(data)
        if flat_state(data, axis) == initial:
            return i


def find_cycle(data):
    cycles = [find_cycle_axis(data, i) for i in range(3)]
    return lcm(cycles)


def lcm(denominators):
    return functools.reduce(lambda a, b: a * b // math.gcd(a, b), denominators)


def test_example2():
    lines = [
        "<x=-1, y=0, z=2>",
        "<x=2, y=-10, z=-7>",
        "<x=4, y=-8, z=8>",
        "<x=3, y=5, z=-1>",
    ]
    data = read_input(lines)
    assert find_cycle(data) == 2772


def test_example3():
    lines = [
        "<x=-8, y=-10, z=0>",
        "<x=5, y=5, z=10>",
        "<x=2, y=-7, z=3>",
        "<x=9, y=-8, z=-3>",
    ]
    data = read_input(lines)
    assert find_cycle(data) == 4686774924


def test_case2():
    with open('day-12.txt', 'r') as f:
        lines = f.readlines()
    data = read_input(lines)
    assert find_cycle(data) == 572087463375796
