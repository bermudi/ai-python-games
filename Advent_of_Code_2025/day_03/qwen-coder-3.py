# Read input from input.txt
with open("input.txt") as f:
    banks = [line.strip() for line in f if line.strip()]

total_output = 0

for bank in banks:
    max_joltage = 0
    # Try every pair of indices (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form two-digit number using digits at positions i and j
            num = int(bank[i] + bank[j])
            if num > max_joltage:
                max_joltage = num
    total_output += max_joltage

print(total_output)