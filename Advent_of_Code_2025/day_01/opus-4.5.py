def solve(input_text):
    lines = input_text.strip().split('\n')
    
    position = 50
    zero_count = 0
    
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        
        if direction == 'L':
            position = (position - distance) % 100
        else:  # R
            position = (position + distance) % 100
        
        if position == 0:
            zero_count += 1
    
    return zero_count

# Read the input
with open('input.txt', 'r') as f:
    input_text = f.read()

result = solve(input_text)
print(result)
