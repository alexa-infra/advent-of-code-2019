from collections import defaultdict
from itertools import tee
import pytest


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_pass(lnum):
    has_double = False
    for a, b in pairwise(lnum):
        if a > b:
            return False
        elif a == b:
            has_double = True
    return has_double


@pytest.mark.parametrize('num,valid', (
    (111111, True),
    (111123, True),
    (223450, False),
    (123789, False),
))
def test_pass(num, valid):
    lnum = list(str(num))
    assert is_pass(lnum) == valid


def next_char(a):
    return chr(ord(a) + 1)


def get_last_correct(lnum):
    last_correct = None
    for i, (a, b) in enumerate(pairwise(lnum)):
        if a <= b:
            if b < '9':
                last_correct = i + 1
            else:
                last_correct = i
                break
        elif a > b:
            last_correct = i + 1
            break
    return last_correct


@pytest.mark.parametrize('num,last_correct', (
    (111111, 5),
    (111117, 5),
    (111119, 4),
    (399999, 0),
    (111890, 3),
    (999999, 0),
    (347312, 3),
))
def test_last_correct(num, last_correct):
    lnum = list(str(num))
    assert get_last_correct(lnum) == last_correct


def get_next_pass(lnum):
    last_correct = get_last_correct(lnum)
    if last_correct is None:
        return False
    ch = lnum[last_correct]
    ch = next_char(ch)
    for i in range(last_correct, len(lnum)):
        lnum[i] = ch
    return True


@pytest.mark.parametrize('num,next_num', (
    (111111, 111112),
    (111119, 111122),
    (899999, 999999),
    (111229, 111233),
    (347312, 347444),
    (347444, 347555),
    (347666, 347777),
    (347777, 347778),
))
def test_next_pass(num, next_num):
    lnum = list(str(num))
    assert get_next_pass(lnum) is True
    assert int(''.join(lnum)) == next_num


def test_case1():
    a, b = 347312, 805915
    lnum1, lnum2 = list(str(a)), list(str(b))
    n = 0
    while get_next_pass(lnum1):
        if lnum1 > lnum2:
            break
        if is_pass(lnum1):
            n += 1
    assert n == 594


def extra_check(lnum):
    r = defaultdict(int)
    for a, b in pairwise(lnum):
        if a == b:
            r[a] += 1
    return any(x == 1 for x in r.values())


@pytest.mark.parametrize('num,valid', (
    (112233, True),
    (123444, False),
    (111122, True),
))
def test_extra_check(num, valid):
    lnum = list(str(num))
    assert extra_check(lnum) == valid


def test_case2():
    a, b = 347312, 805915
    lnum1, lnum2 = list(str(a)), list(str(b))
    n = 0
    while get_next_pass(lnum1):
        if lnum1 > lnum2:
            break
        if extra_check(lnum1):
            n += 1
    assert n == 364
