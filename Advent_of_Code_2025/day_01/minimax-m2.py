#!/usr/bin/env python3
"""
Advent of Code – Day 1: Secret Entrance

The password is the number of times the dial lands on 0 after each rotation.
"""

def main() -> None:
    # Read the input file "input.txt" in the same directory as this script.
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    pos = 50          # dial starts at 50
    count = 0         # how many times we land on 0

    for raw in lines:
        line = raw.strip()
        if not line:
            continue          # skip empty lines

        direction = line[0]          # 'L' or 'R'
        distance = int(line[1:])     # the numeric part

        if direction == 'L':
            pos = (pos - distance) % 100
        else:  # direction == 'R'
            pos = (pos + distance) % 100

        if pos == 0:
            count += 1

    print(count)


if __name__ == "__main__":
    main()