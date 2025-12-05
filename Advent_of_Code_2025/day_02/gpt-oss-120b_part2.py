#!/usr/bin/env python3
"""
Advent of Code – Part Two
Invalid IDs are numbers whose decimal representation consists of a
digit block repeated at least twice.
The program reads 'input.txt' (a single line of comma‑separated ranges)
and prints the sum of all invalid IDs that fall inside any range.
"""

import bisect
import sys
from typing import List, Tuple, Set


def read_ranges(fname: str) -> List[Tuple[int, int]]:
    """Parse the single line of the file into a list of (lo, hi) pairs."""
    with open(fname, "r") as f:
        line = f.read().strip()
    ranges = []
    for token in line.split(","):
        lo_str, hi_str = token.split("-")
        lo, hi = int(lo_str), int(hi_str)
        if lo > hi:          # safety, should not happen
            lo, hi = hi, lo
        ranges.append((lo, hi))
    return ranges


def generate_invalid_ids(limit: int) -> List[int]:
    """
    Return a sorted list of every integer <= limit that is a repetition
    of a digit block at least twice (no leading zero).
    """
    max_len = len(str(limit))
    candidates: Set[int] = set()

    # block length L
    for L in range(1, max_len // 2 + 1):
        start = 10 ** (L - 1)          # first digit cannot be 0
        end = 10 ** L                  # exclusive
        for block in range(start, end):
            block_str = str(block)
            # repeat count r >= 2
            for r in range(2, max_len // L + 1):
                num_str = block_str * r
                # length may be smaller than max_len, but the value could still exceed limit
                num = int(num_str)
                if num > limit:
                    break               # larger r → larger number
                candidates.add(num)

    # Return a sorted list for binary search
    return sorted(candidates)


def main() -> None:
    ranges = read_ranges("input.txt")
    if not ranges:
        print(0)
        return

    max_hi = max(hi for _, hi in ranges)

    # All invalid IDs up to the global maximum
    invalid_ids = generate_invalid_ids(max_hi)

    total = 0
    for lo, hi in ranges:
        left = bisect.bisect_left(invalid_ids, lo)
        right = bisect.bisect_right(invalid_ids, hi)
        total += sum(invalid_ids[left:right])

    print(total)


if __name__ == "__main__":
    main()
