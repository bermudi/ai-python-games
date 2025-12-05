#!/usr/bin/env python3
# compute_password_method_CLICK.py
def compute_counts(filename='input.txt'):
    with open(filename, 'r') as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    # Part 1: count times dial is 0 at the end of a rotation
    pos = 50
    part1 = 0

    # Part 2: count times dial is 0 on any click (including intermediate clicks)
    A = 50  # absolute (unwrapped) position
    part2 = 0

    for line in lines:
        d = line[0]
        n = int(line[1:])

        if d == 'R':
            # zeros in (A, A+n] -> floor((A+n)/100) - floor(A/100)
            part2 += (A + n) // 100 - (A // 100)
            A += n
            pos = (pos + n) % 100
        elif d == 'L':
            # zeros in [A-n, A-1] -> floor((A-1)/100) - floor((A-n-1)/100)
            part2 += (A - 1) // 100 - ((A - n - 1) // 100)
            A -= n
            pos = (pos - n) % 100
        else:
            raise ValueError("bad direction in line: " + line)

        if pos == 0:
            part1 += 1

    return part1, part2

if __name__ == '__main__':
    p1, p2 = compute_counts('input.txt')
    print(p1)  # should be 1026 for your input (part 1)
    print(p2)  # the answer for part 2 (method 0x434C49434B)
