
def read_image(data, w, h):
    n_layers = len(data) // (w * h)
    layers = []
    i = 0
    for n in range(n_layers):
        layer = []
        for y in range(h):
            for x in range(w):
                layer.append(data[i])
                i += 1
        layers.append(layer)
    return layers


def test_example():
    data = "123456789012"
    data = [int(x) for x in data]
    layers = read_image(data, 3, 2)
    assert layers == [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 0, 1, 2],
    ]


def test_case1():
    with open('day-08.txt', 'r') as f:
        data = f.read().strip()
    data = [int(x) for x in data]
    w, h = 25, 6
    layers = read_image(data, w, h)

    def count(layer, n):
        return layer.count(n)

    zeros = min(layers, key=lambda x: count(x, 0))
    ones = count(zeros, 1)
    twos = count(zeros, 2)
    assert ones * twos == 2500


def decode_image(layers, w, h):
    """ 0 - black, 1 - white, 2 - transparent """
    result = [0 for x in range(w * h)]
    for y in range(h):
        for x in range(w):
            for layer in layers:
                p = layer[y * w + x]
                if p == 2:
                    continue
                else:
                    result[y * w + x] = p
                    break
    return result


def test_case2():
    with open('day-08.txt', 'r') as f:
        data = f.read().strip()
    data = [int(x) for x in data]
    w, h = 25, 6
    layers = read_image(data, w, h)
    image = decode_image(layers, w, h)
    img = []
    for y in range(h):
        row = [image[y * w + x] for x in range(w)]
        row = ['.' if p == 0 else '#' for p in row]
        img.append(''.join(row))
    expected = [
        ".##..#...##..#..##..#..#.",
        "#..#.#...##..#.#..#.#..#.",
        "#.....#.#.#..#.#..#.####.",
        "#......#..#..#.####.#..#.",
        "#..#...#..#..#.#..#.#..#.",
        ".##....#...##..#..#.#..#.",
    ]
    assert img == expected
