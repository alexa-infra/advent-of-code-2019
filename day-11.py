
day09 = __import__("day-09")
process = day09.process_gen

rotor = {
    0: {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'},
    1: {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'},
}
diff = {
    'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0),
}

def draw(data, panels):
    direction = 'N'
    coord = (0, 0)
    try:
        inp = []
        g = process(data, inp)
        while True:
            current_color = panels.get(coord, 0)
            inp.append(current_color)
            color = next(g)
            panels[coord] = color
            rotate = next(g)
            direction = rotor[rotate][direction]
            dd = diff[direction]
            coord = coord[0] + dd[0], coord[1] + dd[1]
    except StopIteration:
        pass
    return panels


def test_case1():
    with open('day-11.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    panels = dict()
    draw(data, panels)
    xmin = min(x[0] for x in panels.keys())
    xmax = max(x[0] for x in panels.keys())
    ymin = min(x[1] for x in panels.keys())
    ymax = max(x[1] for x in panels.keys())
    w = xmax - xmin
    h = ymax - ymin
    for j in range(ymin, ymax):
        for i in range(xmin, xmax):
            c = (i, j)
            color = panels.get(c, 0)
            print('#' if color == 1 else '.', end='')
        print()
    assert len(panels) == 2339


def test_case2():
    with open('day-11.txt', 'r') as f:
        text = f.read().strip()
    data = [int(x) for x in text.split(',')]
    panels = dict()
    panels[(0, 0)] = 1
    draw(data, panels)
    xmin = min(x[0] for x in panels.keys()) - 2
    xmax = max(x[0] for x in panels.keys()) + 2
    ymin = min(x[1] for x in panels.keys()) - 2
    ymax = max(x[1] for x in panels.keys()) + 2
    w = xmax - xmin
    h = ymax - ymin
    for j in range(ymax, ymin, -1):
        for i in range(xmin, xmax):
            c = (i, j)
            color = panels.get(c, 0)
            print('#' if color == 1 else '.', end='')
        print()
    assert False
