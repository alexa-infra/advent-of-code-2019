from collections import deque


class Deck:
    def __init__(self, size):
        self.deck = deque(range(size))
        self.dir = 1

    def new(self):
        self.dir = -self.dir

    def cut(self, n):
        self.deck.rotate(-n * self.dir)

    def deal(self, incr):
        deck = deque(range(len(self.deck)))

        while len(self.deck):
            deck[0] = self.deck.popleft() if self.dir == 1 else self.deck.pop()
            deck.rotate(-incr)

        self.deck = deck
        self.dir = 1

    def cards(self):
        return list(self.deck) if self.dir == 1 else list(self.deck)[::-1]


def part1(filename):
    card = 2019
    size = 10007

    with open(filename, 'r') as f:
        lines = f.readlines()

    deck = Deck(size)
    for cmd in lines:
        op, *_, n = cmd.strip().split(" ")
        if op == "cut":
            deck.cut(int(n))
        elif op == "deal" and n == "stack":
            deck.new()
        elif op == "deal":
            deck.deal(int(n))

    idx = deck.cards().index(card)
    print(f"Position of card {card}: {idx}")


def part2(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    cards = 119315717514047 # is prime!
    repeats = 101741582076661

    # the idea is that such deck might be described as a pair of integers (offset, increment)
    #   increment = the difference between two adjacent cards (initially 1)
    #   offset = the first number in the deck (initially 0)
    # all deck operations can be describeds as operations on that pair (using modular math)
    #   cut (shift n left) - new offset = (b * increment) by modulo (num cards)
    #   reverse - new increment = -1 * increment
    #   deal into new stack (reverse, then shift 1 left)
    #   deal with increment n - new increment is multiplied by inv(n)
    # the problem is to find n-th item in the deck after repeating all operations (repeats) times

    def inv(n):
        # gets the modular inverse of n (Euler's theorem)
        return pow(n, cards-2, cards)

    def get(offset, increment, n):
        # gets the n-th number in the deck
        return (offset + n * increment) % cards
    
    # at first we calculate what would be (increment, offset) after one repeat
    increment_mul = 1
    offset_diff = 0
    for line in lines:
        op, *_, n = line.strip().split(" ")
        if op == "cut":
            offset_diff += int(n) * increment_mul
            offset_diff %= cards
        elif op == "deal" and n == "stack":
            increment_mul *= -1
            increment_mul %= cards
            offset_diff += increment_mul
            offset_diff %= cards
        elif op == "deal":
            increment_mul *= inv(int(n))
            increment_mul %= cards

    # second and every next repeat would change (increment, offset)
    # new increment = increment * increment_mul
    # new offset = offset + offset_diff * increment

    # after (iterations) repeats it would be...
    # increment = increment_mul^iterations
    # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
    # (which could be solved by using geometric series)

    def get_sequence(iterations):
        increment = pow(increment_mul, iterations, cards)
        offset = offset_diff * (1 - increment) * inv((1 - increment_mul) % cards)
        offset %= cards
        return increment, offset

    increment, offset = get_sequence(repeats)
    print(get(offset, increment, 2020))

if __name__ == '__main__':
    part1('day-22.txt')
    part2('day-22.txt')
