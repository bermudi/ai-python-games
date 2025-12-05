# ------------------------------------------------------------
# Advent of Code – Day 1 – Part 2 (method 0x434C49434B)
# Counts every click that lands on 0.
# ------------------------------------------------------------

def count_zero_hits(pos: int, distance: int, direction: str) -> int:
    """
    Returns how many times the dial points at 0 while moving
    `distance` clicks from `pos` in the given `direction` ('L' or 'R').
    """
    if direction == 'R':
        # distance to the next 0 when moving right
        first = (100 - pos) % 100
        if first == 0:
            first = 100
    else:   # direction == 'L'
        # distance to the next 0 when moving left
        first = pos % 100
        if first == 0:
            first = 100

    if first > distance:
        return 0
    # first hit + possible additional hits each 100 clicks later
    return 1 + (distance - first) // 100


def main() -> None:
    # read input
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    pos = 50          # initial dial position
    total = 0         # total number of times we hit 0

    for line in lines:
        direction = line[0]               # 'L' or 'R'
        distance = int(line[1:])           # may be > 100

        # count intermediate zero hits
        total += count_zero_hits(pos, distance, direction)

        # update final position after the whole rotation
        delta = distance if direction == 'R' else -distance
        pos = (pos + delta) % 100

    print(total)


if __name__ == "__main__":
    main()