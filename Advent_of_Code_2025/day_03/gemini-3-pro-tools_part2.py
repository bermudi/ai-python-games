def solve_part_two():
    total_output_joltage = 0
    filename = 'input.txt'
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse all digits from the line
        digits = [int(c) for c in line if c.isdigit()]
        
        target_length = 12
        n = len(digits)
        
        # If a line has fewer than 12 digits, it cannot form a 12-digit number
        if n < target_length:
            continue
            
        # We need to remove (n - 12) digits to keep the best 12
        to_remove = n - target_length
        
        stack = []
        for digit in digits:
            # Greedy approach: If the current digit is larger than the last one 
            # we picked, and we still have "removals" available, replace the 
            # last one. This ensures higher digits appear as early as possible.
            while to_remove > 0 and stack and stack[-1] < digit:
                stack.pop()
                to_remove -= 1
            stack.append(digit)
            
        # If we still have removals left (e.g., if the sequence was 9876...),
        # remove them from the end of the stack.
        while to_remove > 0:
            stack.pop()
            to_remove -= 1
            
        # The stack should now contain exactly 12 digits.
        # Join them to form the number.
        best_digits = stack[:target_length]
        bank_value = int("".join(map(str, best_digits)))
        
        total_output_joltage += bank_value

    print(f"Total Output Joltage: {total_output_joltage}")

if __name__ == "__main__":
    solve_part_two()