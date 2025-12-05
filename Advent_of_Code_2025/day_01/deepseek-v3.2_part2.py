def count_zeros_during_rotation(start, direction, distance):
    if direction == 'R':
        r = (-start) % 100
    else:  # 'L'
        r = start % 100
    if r == 0:
        return distance // 100
    else:
        if distance >= r:
            return (distance - r) // 100 + 1
        else:
            return 0

pos = 50
total = 0
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        dir = line[0]
        dist = int(line[1:])
        total += count_zeros_during_rotation(pos, dir, dist)
        if dir == 'R':
            pos = (pos + dist) % 100
        else:
            pos = (pos - dist) % 100

print(total)
