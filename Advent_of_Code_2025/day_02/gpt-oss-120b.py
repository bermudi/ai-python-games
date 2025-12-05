#!/usr/bin/env python3
"""
Solution for the “invalid product IDs” puzzle.

The program reads a file named 'input.txt' that contains a single line
with comma‑separated ranges of the form “a-b”.  It prints the sum of all
numbers that consist of a digit block repeated twice and that lie inside
any of the given ranges.

Author: ChatGPT
"""

import sys
import bisect

def read_ranges(filename: str):
    """Parse the single line of comma‑separated a-b ranges."""
    with open(filename, "r") as f:
        line = f.read().strip()
    ranges = []
    for token in line.split(","):
        lo_str, hi_str = token.split("-")
        lo, hi = int(lo_str), int(hi_str)
        if lo > hi:
            lo, hi = hi, lo
        ranges.append((lo, hi))
    return ranges

def generate_double_numbers(limit: int):
    """Return a sorted list of all numbers ≤ limit of the form t||t."""
    doubles = []
    max_len = len(str(limit)) // 2          # maximal length of block t
    for block_len in range(1, max_len + 1):
        start = 10 ** (block_len - 1)       # first block without leading zero
        end   = 10 ** block_len             # one past the last block
        for block in range(start, end):
            s = str(block)
            double_val = int(s + s)
            if double_val > limit:
                # Since blocks increase, further blocks will only be larger.
                break
            doubles.append(double_val)
    doubles.sort()
    return doubles

def main():
    ranges = read_ranges("input.txt")
    if not ranges:
        print(0)
        return

    max_hi = max(hi for _, hi in ranges)

    # Step 4‑5: generate every invalid ID up to the global maximum
    doubles = generate_double_numbers(max_hi)

    total = 0
    for lo, hi in ranges:
        left = bisect.bisect_left(doubles, lo)
        right = bisect.bisect_right(doubles, hi)
        # sum of the slice; using built‑in sum is efficient enough
        total += sum(doubles[left:right])

    print(total)


if __name__ == "__main__":
    main()