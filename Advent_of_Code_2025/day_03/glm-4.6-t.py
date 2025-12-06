def max_joltage_for_bank(bank):
    max_joltage = 0
    n = len(bank)
    for i in range(n - 1):
        for j in range(i + 1, n):
            joltage = int(bank[i]) * 10 + int(bank[j])
            if joltage > max_joltage:
                max_joltage = joltage
    return max_joltage

def total_joltage(banks):
    total = 0
    for bank in banks:
        total += max_joltage_for_bank(bank)
    return total

# Read the input file
with open('input.txt', 'r') as f:
    banks = f.read().splitlines()

# Calculate the total joltage
total = total_joltage(banks)

# Print the result
print(total)