import math
from collections import defaultdict
import pytest


def parse_comp(txt):
    num, name = txt.split(' ')
    return name, int(num)


def parse(line):
    line = line.strip()
    src, target = line.split(' => ')
    src = src.split(', ')
    src = tuple(parse_comp(x) for x in src)
    target = parse_comp(target)
    return target, {k: v for k, v in src}


@pytest.mark.parametrize('line,src,target', (
    ('1 A, 2 B, 3 C => 2 D', {'A': 1, 'B': 2, 'C': 3}, ('D', 2)),
    ('7 A, 1 E => 1 FUEL', {'A': 7, 'E': 1}, ('FUEL', 1)),
))
def test_parse(line, src, target):
    assert parse(line) == (target, src)


def ore_per_fuel(data, fuel):
    need = defaultdict(int)
    need['FUEL'] = fuel

    stack = list(need.keys())
    while stack:
        name = stack.pop()
        if name not in data:
            continue

        amount = need[name]
        if amount <= 0:
            continue

        units, sources = data[name]
        n = math.ceil(amount / units)
        for k, v in sources.items():
            need[k] += v * n
            stack.append(k)

        need[name] -= n * units

    return need['ORE']


def parse_input(lines):
    data = [parse(line) for line in lines]
    return {k: (n, v) for (k, n), v in data}


example1 = [
    "10 ORE => 10 A",
    "1 ORE => 1 B",
    "7 A, 1 B => 1 C",
    "7 A, 1 C => 1 D",
    "7 A, 1 D => 1 E",
    "7 A, 1 E => 1 FUEL",
]


example2 = [
    "9 ORE => 2 A",
    "8 ORE => 3 B",
    "7 ORE => 5 C",
    "3 A, 4 B => 1 AB",
    "5 B, 7 C => 1 BC",
    "4 C, 1 A => 1 CA",
    "2 AB, 3 BC, 4 CA => 1 FUEL",
]


example3 = [
    "157 ORE => 5 NZVS",
    "165 ORE => 6 DCFZ",
    "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
    "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
    "179 ORE => 7 PSHF",
    "177 ORE => 5 HKGWZ",
    "7 DCFZ, 7 PSHF => 2 XJWVT",
    "165 ORE => 2 GPVTF",
    "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
]


example4 = [
    "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
    "17 NVRVD, 3 JNWZP => 8 VPVL",
    "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
    "22 VJHF, 37 MNCFX => 5 FWMGM",
    "139 ORE => 4 NVRVD",
    "144 ORE => 7 JNWZP",
    "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
    "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
    "145 ORE => 6 MNCFX",
    "1 NVRVD => 8 CXFTF",
    "1 VJHF, 6 MNCFX => 4 RFSQX",
    "176 ORE => 6 VJHF",
]


example5 = [
    "171 ORE => 8 CNZTR",
    "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
    "114 ORE => 4 BHXH",
    "14 VRPVC => 6 BMBT",
    "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
    "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
    "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
    "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
    "5 BMBT => 4 WPTQ",
    "189 ORE => 9 KTJDG",
    "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
    "12 VRPVC, 27 CNZTR => 2 XDBXC",
    "15 KTJDG, 12 BHXH => 5 XCVML",
    "3 BHXH, 2 VRPVC => 7 MZWV",
    "121 ORE => 7 VRPVC",
    "7 XCVML => 6 RJRHP",
    "5 BHXH, 4 VRPVC => 5 LTCX",
]


@pytest.mark.parametrize('lines,ore', (
    (example1, 31),
    (example2, 165),
    (example3, 13312),
    (example4, 180697),
    (example5, 2210736),
))
def test_example(lines, ore):
    data = parse_input(lines)
    assert ore_per_fuel(data, 1) == ore


def test_case1():
    with open('day-14.txt', 'r') as f:
        lines = f.readlines()
    data = parse_input(lines)
    assert ore_per_fuel(data, 1) == 387001


def fuel_per_ore(data, ore):
    fuel = 1
    while True:
        n = ore_per_fuel(data, fuel)
        if n > ore:
            break
        fuel = fuel << 1
    L, R = fuel >> 1, fuel
    while L != R - 1:
        mid = (L + R) // 2
        n = ore_per_fuel(data, mid)
        if n > ore:
            R = mid
        else:
            L = mid
    return L


@pytest.mark.parametrize('lines,fuel', (
    (example3, 82892753),
    (example4, 5586022),
    (example5, 460664),
))
def test_example2(lines, fuel):
    data = parse_input(lines)
    assert fuel_per_ore(data, 1000000000000) == fuel


def test_case2():
    with open('day-14.txt', 'r') as f:
        lines = f.readlines()
    data = parse_input(lines)
    assert fuel_per_ore(data, 1000000000000) == 3412429
