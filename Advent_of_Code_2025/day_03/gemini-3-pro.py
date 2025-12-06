def solve():
    total_output_joltage = 0
    
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: input.txt not found. Please create the file with your puzzle input.")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Convert the string of characters into a list of integers
        digits = [int(char) for char in line]
        
        # We need to find the max joltage for this specific bank
        bank_max_joltage = 0
        
        # Iterate through all possible pairs (i, j) where i comes before j
        # The first battery selected (index i) becomes the tens digit
        # The second battery selected (index j) becomes the ones digit
        for i in range(len(digits)):
            for j in range(i + 1, len(digits)):
                # Calculate joltage: first digit * 10 + second digit
                current_joltage = digits[i] * 10 + digits[j]
                
                if current_joltage > bank_max_joltage:
                    bank_max_joltage = current_joltage
        
        # Add the max for this bank to the total sum
        total_output_joltage += bank_max_joltage

    print(total_output_joltage)

if __name__ == "__main__":
    solve()