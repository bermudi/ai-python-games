with open('input.txt', 'r') as file:
    lines = file.read().strip().splitlines()

position = 50
count = 0

for line in lines:
    direction = line[0]
    distance = int(line[1:])
    if direction == 'L':
        position = (position - distance) % 100
    else:
        position = (position + distance) % 100
    if position == 0:
        count += 1

print(count)
