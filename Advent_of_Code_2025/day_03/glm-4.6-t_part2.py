def max_joltage_for_bank(bank, k=12):
    result = []
    start = 0
    remaining = k
    
    while remaining > 0:
        # Find the largest digit in the range [start, len(bank) - remaining]
        max_digit = '0'
        max_index = -1
        
        for i in range(start, len(bank) - remaining + 1):
            if bank[i] > max_digit:
                max_digit = bank[i]
                max_index = i
                
                # If we found '9', we can break early since it's the largest digit
                if max_digit == '9':
                    break
        
        result.append(max_digit)
        start = max_index + 1
        remaining -= 1
    
    return int(''.join(result))

def total_joltage(banks, k=12):
    total = 0
    for bank in banks:
        total += max_joltage_for_bank(bank, k)
    return total

# Read the input file
with open('input.txt', 'r') as f:
    banks = f.read().splitlines()

# Calculate the total joltage
total = total_joltage(banks)

# Print the result
print(total)