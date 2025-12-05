def count_zeros(position, direction, distance):
    if direction == 'L':
        first_k = position if position != 0 else 100
    else:  # R
        first_k = (100 - position) % 100
        if first_k == 0:
            first_k = 100
    
    if distance < first_k:
        return 0
    return (distance - first_k) // 100 + 1

def solve(input_text):
    lines = input_text.strip().split('\n')
    
    position = 50
    zero_count = 0
    
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        
        zero_count += count_zeros(position, direction, distance)
        
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
    
    return zero_count

with open('input.txt', 'r') as f:
    input_text = f.read()

print(solve(input_text))
