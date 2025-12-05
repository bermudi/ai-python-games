#!/usr/bin/env python3
"""
Advent of Code – Day 1: Secret Entrance (Part 2)

Password method 0x434C49434B ("CLICK") counts every click that lands on 0.
"""

def main() -> None:
    # Read the input file "input.txt" located in the same directory.
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    pos = 50                 # dial starts at 50
    total_hits = 0           # answer to be printed

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        direction = line[0]          # 'L' or 'R'
        distance  = int(line[1:])    # integer distance

        # Determine the first step that reaches 0
        if direction == 'L':
            target = pos % 100
        else:  # 'R'
            target = (100 - pos) % 100

        if target == 0:
            target = 100  # first positive step that lands on 0

        # Count hits during this rotation
        if distance >= target:
            total_hits += 1 + (distance - target) // 100

        # Update the dial position for the next rotation
        if direction == 'L':
            pos = (pos - distance) % 100
        else:
            pos = (pos + distance) % 100

    print(total_hits)


if __name__ == "__main__":
    main()