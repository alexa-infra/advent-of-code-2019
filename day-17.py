
day09 = __import__("day-09")
process = day09.process_gen

car_symbols = ('<', '>', '^', 'v', 'X')

def build_map():
    with open('day-17.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]
    out = ''.join(chr(x) for x in process(idata, []))
    #print(out)
    data = dict()
    lines = out.split('\n')
    for j, line in enumerate(lines):
        for i, ch in enumerate(line):
            if ch == '.':
                continue
            if ch == '#':
                data[(i, j)] = '#'
            if ch in car_symbols:
                data[(i, j)] = ch
    return data

directions = {
    '^': (0, -1),
    'v': (0, 1),
    '>': (1, 0),
    '<': (-1, 0),
}

def find_intersections(data):
    car_pos, car_sym = next((k, v) for k, v in data.items() if v in car_symbols)
    path = set([car_pos])

    while True:
        next_dir = directions[car_sym]
        next_pos = car_pos[0] + next_dir[0], car_pos[1] + next_dir[1]

        if next_pos in data:
            if next_pos in path:
                data[next_pos] = 'O'
            else:
                path.add(next_pos)
            car_pos = next_pos
            if data[car_pos] != 'O':
                data[car_pos] = car_sym
            continue

        for k, v in directions.items():
            next_pos = car_pos[0] + v[0], car_pos[1] + v[1]
            if next_pos in data:
                if next_pos in path:
                    continue
                else:
                    path.add(next_pos)
                car_pos = next_pos
                car_sym = k
                data[car_pos] = car_sym
                break
        else:
            break

rotate = {
    '^': { '<': 'L', '>': 'R' },
    '>': { '^': 'L', 'v': 'R' },
    'v': { '>': 'L', '<': 'R' },
    '<': { 'v': 'L', '^': 'R' },
}

def find_path(data):
    car_pos, car_sym = next((k, v) for k, v in data.items() if v in car_symbols)
    path = list()
    visited = set()

    n = 0
    while True:
        next_dir = directions[car_sym]
        next_pos = car_pos[0] + next_dir[0], car_pos[1] + next_dir[1]

        if next_pos in data:
            visited.add(next_pos)
            n += 1
            car_pos = next_pos
            continue

        for k, v in directions.items():
            next_pos = car_pos[0] + v[0], car_pos[1] + v[1]
            if next_pos in data:
                if next_pos in visited:
                    continue
                else:
                    visited.add(next_pos)
                if n > 0:
                    path.append(n + 1)
                    n = 0
                rl = rotate[car_sym][k]
                path.append(rl)
                car_pos = next_pos
                car_sym = k
                break
        else:
            path.append(n + 1)
            break
    return path

def print_map(data):
    xmin = min(k[0] for k in data.keys())
    xmax = max(k[0] for k in data.keys())
    ymin = min(k[1] for k in data.keys()) 
    ymax = max(k[1] for k in data.keys())
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            ch = data.get((x, y), '.')
            print(ch, end='')
        print()


def test_case1():
    data = build_map()
    find_intersections(data)
    it = (k for k, v in data.items() if v == 'O')
    assert sum(k[0] * k[1] for k in it) == 3608

def test_case2():
    with open('day-17.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]
    idata[0] = 2
    inp = [
        "A,B,A,C,A,B,C,A,B,C",
        "R,8,R,10,R,10",
        "R,4,R,8,R,10,R,12",
        "R,12,R,4,L,12,L,12",
        "n",
        "",
    ]
    inp = '\n'.join(inp)
    inp = [ord(ch) for ch in inp]
    inp.reverse()
    out = [x for x in process(idata, inp)]
    assert out[-1] == 897426


if __name__ == '__main__':
    data = build_map()
    #print_map(data)
    path = find_path(data)
    #print_map(data)
    print(path)
