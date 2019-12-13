day09 = __import__("day-09")
process = day09.process_gen


def gen_map(data):
    mmap = dict()
    g = process(data, [])
    try:
        while True:
            x = next(g)
            y = next(g)
            t = next(g)
            mmap[(x, y)] = t
    except StopIteration:
        pass
    return mmap


def test_case1():
    with open('day-13.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    mmap = gen_map(data)
    blocktiles = {k: v for k, v in mmap.items() if v == 2}
    assert len(blocktiles) == 304


def print_map(mmap):
    xmin = min(k[0] for k in mmap.keys())
    xmax = max(k[0] for k in mmap.keys())
    ymin = min(k[1] for k in mmap.keys()) 
    ymax = max(k[1] for k in mmap.keys())
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            t = mmap.get((x, y), 0)
            if t == 0:
                print(' ', end='')
            elif t == 1:
                print('#', end='')
            elif t == 2:
                print('.', end='')
            elif t == 3:
                print('-', end='')
            elif t == 4:
                print('X', end='')
        print()


def find_tile(mmap, i):
    return next(k for k, v in mmap.items() if v == i)


def game():
    with open('day-13.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    data[0] = 2
    score = 0

    try:
        mmap = dict()

        class Inp:
            pball = None

            def pop(self):
                #print_map(mmap)
                ball = find_tile(mmap, 4)
                pad = find_tile(mmap, 3)

                if self.pball is None:
                    self.pball = ball
                    return 0
                elif ball[0] < pad[0]:
                    return -1
                elif ball[0] > pad[0]:
                    return 1
                elif ball[0] < self.pball[0]:
                    return -1
                else:
                    return 1

        inp = Inp()

        g = process(data, inp)
        while True:
            x = next(g)
            y = next(g)
            t = next(g)
            if (x, y) == (-1, 0):
                score = t
            else:
                mmap[(x, y)] = t
    except StopIteration:
        pass
    print('Score', score)
    return score


def test_game():
    assert game() == 14747


if __name__ == '__main__':
    game()
