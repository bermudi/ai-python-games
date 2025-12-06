#!/usr/bin/env python3
# compute_password.py
def compute_password(filename='input.txt'):
    pos = 50
    count = 0
    with open(filename, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            dir_ = line[0]
            dist = int(line[1:]) % 100
            if dir_ == 'L':
                pos = (pos - dist) % 100
            elif dir_ == 'R':
                pos = (pos + dist) % 100
            else:
                raise ValueError("Bad direction: " + line)
            if pos == 0:
                count += 1
    return count

if __name__ == '__main__':
    print(compute_password())
