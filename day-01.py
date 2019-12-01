import pytest


def get_fuel(mass):
    return mass // 3 - 2


@pytest.mark.parametrize('mass,fuel', (
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583),
))
def test_get_fuel(mass, fuel):
    assert get_fuel(mass) == fuel


def test_case1():
    with open('day-01.txt', 'r') as f:
        lines = f.readlines()

    masses = [int(line) for line in lines]
    fuel = sum(get_fuel(mass) for mass in masses)
    assert fuel == 3336985


def get_full_fuel(mass):
    s = 0
    while mass > 0:
        m = get_fuel(mass)
        if m > 0:
            s += m
        mass = m
    return s


@pytest.mark.parametrize('mass,fuel', (
    (14, 2),
    (1969, 966),
    (100756, 50346),
))
def test_get_full_fuel(mass, fuel):
    assert get_full_fuel(mass) == fuel


def test_case2():
    with open('day-01.txt', 'r') as f:
        lines = f.readlines()

    masses = [int(line) for line in lines]
    fuel = sum(get_full_fuel(mass) for mass in masses)
    assert fuel == 5002611
