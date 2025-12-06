def solve():
    position = 50  # dial starts at 50
    zero_count = 0  # count of times dial points to 0 after a rotation

    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:  # skip empty lines
                continue

            direction = line[0]
            distance = int(line[1:])

            if direction == 'L':
                position = (position - distance) % 100
            else:  # direction == 'R'
                position = (position + distance) % 100

            if position == 0:
                zero_count += 1

    print(zero_count)

if __name__ == "__main__":
    solve()
