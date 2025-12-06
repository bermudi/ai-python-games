import sys

def solve():
    total_output_joltage = 0
    REQUIRED_LENGTH = 12
    
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: input.txt not found. Please ensure the file exists.")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Convert line to list of integers
        digits = [int(c) for c in line if c.isdigit()]
        
        n = len(digits)
        if n < REQUIRED_LENGTH:
            continue
            
        stack = []
        
        for i, digit in enumerate(digits):
            # Calculate how many digits are available in the input (current + future)
            remaining_in_input = n - i
            
            # Greedy approach: maintain a monotonically decreasing stack (lexicographically largest),
            # but only pop if we have enough digits left to satisfy the length requirement.
            while stack and stack[-1] < digit:
                # If we pop the top element, will we still have enough digits 
                # (current stack size - 1 + remaining input) to reach REQUIRED_LENGTH?
                if (len(stack) - 1) + remaining_in_input >= REQUIRED_LENGTH:
                    stack.pop()
                else:
                    break
            
            stack.append(digit)
        
        # We only want the first 12 digits
        best_digits = stack[:REQUIRED_LENGTH]
        
        # Form the number and add to total
        bank_value = int("".join(map(str, best_digits)))
        total_output_joltage += bank_value

    print(total_output_joltage)

if __name__ == "__main__":
    solve()