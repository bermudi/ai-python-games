with open('input.txt', 'r') as f:
    lines = f.readlines()

total = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Find all positions and their digit values
    max_joltage = 0
    
    # Try all pairs of positions
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            # Form the number from digits at positions i and j
            joltage = int(line[i]) * 10 + int(line[j])
            max_joltage = max(max_joltage, joltage)
    
    total += max_joltage

print(total)