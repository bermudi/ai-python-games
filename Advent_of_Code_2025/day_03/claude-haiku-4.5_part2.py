with open('input.txt', 'r') as f:
    lines = f.readlines()

total = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # We need to select exactly 12 digits from the bank
    # to form the largest possible 12-digit number
    # while maintaining their order in the original string
    
    n = len(line)
    num_to_select = 12
    
    # Greedy approach: at each step, pick the largest digit
    # such that we can still select enough remaining digits
    selected = []
    start_pos = 0
    
    for step in range(num_to_select):
        # How many more digits do we need after this one?
        remaining_needed = num_to_select - step - 1
        
        # What's the latest position we can pick from?
        # We need at least remaining_needed digits after our pick
        max_pos = n - remaining_needed - 1
        
        # Find the largest digit in the range [start_pos, max_pos]
        best_digit = -1
        best_pos = -1
        
        for pos in range(start_pos, max_pos + 1):
            if int(line[pos]) > best_digit:
                best_digit = int(line[pos])
                best_pos = pos
        
        selected.append(str(best_digit))
        start_pos = best_pos + 1
    
    # Convert selected digits to a number
    joltage = int(''.join(selected))
    total += joltage

print(total)