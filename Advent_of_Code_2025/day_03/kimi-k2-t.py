#!/usr/bin/env python3
import sys

def max_joltage(bank: str) -> int:
    """
    Return the largest two‑digit number that can be formed by picking
    two digits from `bank` (i < j, order preserved).
    """
    bank = bank.strip()
    n = len(bank)
    if n < 2:
        return 0                     # not enough batteries – shouldn't happen

    digits = [int(ch) for ch in bank]

    # suffix_max[i] = max digit strictly to the right of i
    suffix_max = [0] * n
    suffix_max[-1] = -1               # no digit after the last position
    for i in range(n - 2, -1, -1):
        suffix_max[i] = max(digits[i + 1], suffix_max[i + 1])

    best = -1
    # last digit cannot be the tens digit, so stop at n-2
    for i in range(n - 1):
        cand = 10 * digits[i] + suffix_max[i]
        if cand > best:
            best = cand

    return best


def total_joltage(filename: str) -> int:
    """Read all banks from `filename` and sum their maximal joltages."""
    total = 0
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:                  # ignore empty lines
                total += max_joltage(line)
    return total


if __name__ == "__main__":
    # The puzzle asks for reading from "input.txt"
    answer = total_joltage("input.txt")
    print(answer)