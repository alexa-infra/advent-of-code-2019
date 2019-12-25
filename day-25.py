import re
import io
day23 = __import__("day-23")
process = day23.process_gen


def get_intcode():
    with open('day-25.txt', 'r') as f:
        text = f.read().strip()
    idata = [int(x) for x in text.split(',')]
    return idata

def parse_output(text):
    lines = text.split('\n')
    name, doors, items = None, [], []
    parse_doors, parse_items = False, False
    for line in lines:
        line = line.strip()
        if match := re.match("== (.*) ==", line):
            name = match[1]
        elif line == "Doors here lead:":
            parse_doors = True
        elif line == "Items here:":
            parse_items = True
        elif parse_doors:
            if match := re.match("- (east|west|south|north)", line):
                doors.append(match[1])
            else:
                parse_doors = False
        elif parse_items:
            if match := re.match("- (.*)", line):
                items.append(match[1])
            else:
                parse_items = False
    return name, doors, items


def build_map():

    def walk(path):
        path = list(path)
        idata = get_intcode()
        inp = []
        g = process(idata, inp)

        def push_cmd(cmd):
            for ch in reversed(cmd + '\n'):
                inp.append(ord(ch))

        rv = None
        buf = io.StringIO()
        while True:
            name, v = next(g)
            if name == 'output':
                buf.write(chr(v))
            elif name == 'input':
                rv = parse_output(buf.getvalue())
                buf = io.StringIO()
                if path:
                    push_cmd(path.pop(0))
                else:
                    return rv

    name, doors, items = walk([])
    visited = set()
    stack = [(name, doors, [])]
    while stack:
        name, doors, path = stack.pop()
        if name in visited:
            continue
        visited.add(name)
        for door in doors:
            new_path = path + [door]
            new_name, new_doors, _ = walk(new_path)
            stack.append((new_name, new_doors, new_path))
    print(visited)

def run(items):
    # Hull Breach:
    #   east - Holodeck
    #   south - Stables (cake)
    #     east - Observatory (electoromagnet)
    #       east - Passages (infinite loop)
    #         north - Science Lab (photons)
    #     south - Kitchen
    #       west - Arcade (mutex)
    #   west - Sick Bay (klein bottle)
    #     south - Hot Chocolate Fountain
    #       east - Gift Wrapping Center (monolith)
    #         south - Crew Quarters (fuel cell)
    #           west - Corridor (escape pod)
    #             west - Warp Drive Maintenance (astrolabe)
    #       west - Hallway (molten lava)
    #     west - Storage
    #       north - Engineering (tambourine)
    #       west - Navigation (dark matter)
    #         west - Security Checkpoint
    #           north
    # {'astrolabe', 'monolith', 'tambourine', 'dark matter'}
    commands = [
        'south',
        'take cake',
        'south',
        'west',
        'take mutex',
        'east',
        'north',
        'north',
        'west',
        'take klein bottle',
        'south',
        'east',
        'take monolith',
        'south',
        'take fuel cell',
        'west',
        'west',
        'take astrolabe',
        'east',
        'east',
        'north',
        'west',
        'north',
        'west',
        'north',
        'take tambourine',
        'south',
        'west',
        'take dark matter',
        'west',
        'north', # security check!
    ]
    idata = get_intcode()
    inp = []
    g = process(idata, inp)

    def push_cmd(cmd):
        for ch in reversed(cmd + '\n'):
            inp.append(ord(ch))

    buf = io.StringIO()
    try:
        while True:
            name, v = next(g)
            if name == 'output':
                buf.write(chr(v))
            elif name == 'input':
                text = buf.getvalue()
                if 'Pressure-Sensitive Floor' in text:
                    if 'heavier' not in text and 'lighter' not in text:
                        print(text)
                buf = io.StringIO()

                if commands:
                    value = commands.pop(0)
                    if value.startswith('take'):
                        if any(value.endswith(x) for x in items):
                            pass
                        else:
                            value = commands.pop(0)
                else:
                    break
                push_cmd(value)
    except StopIteration:
        print(items)
        print(buf.getvalue())

def run_vm():
    idata = get_intcode()
    inp = []
    g = process(idata, inp)

    def push_cmd(cmd):
        for ch in reversed(cmd + '\n'):
            inp.append(ord(ch))

    while True:
        name, v = next(g)
        if name == 'output':
            print(chr(v), end='')
        elif name == 'input':
            value = input('IN: ')
            push_cmd(value)

import itertools

def run_scissors():
    items = set([
        "mutex",
        "dark matter",
        "klein bottle",
        "tambourine",
        "fuel cell",
        "astrolabe",
        "monolith",
        "cake",
    ])
    for i in range(len(items)):
        for it in itertools.combinations(items, i):
            new_items = items - set(it)
            run(new_items)

if __name__ == '__main__':
    build_map()
