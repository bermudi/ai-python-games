import os

def calculate_max_joltage_for_bank(bank_string: str) -> int:
    """
    Calculates the maximum possible two-digit joltage from a single battery bank string.

    The joltage is formed by selecting exactly two batteries (digits) from the bank string.
    The first selected battery's digit forms the tens place, and the second selected
    battery's digit forms the units place. The second battery must appear after the
    first battery in the original string.

    Args:
        bank_string: A string representing a bank of batteries, where each character
                     is a digit from '1' to '9'.

    Returns:
        The largest possible two-digit joltage that can be produced from the bank.
        Returns 0 if the bank string has fewer than two batteries, as no joltage
        can be produced in that case.
    """
    max_joltage = 0  # Initialize with 0. The smallest possible joltage is 11 (e.g., from "11").
    n = len(bank_string)

    # A bank must have at least two batteries to produce a joltage
    if n < 2:
        return 0

    # Iterate through all possible positions for the first battery (tens digit)
    # The first battery can be at any index from 0 up to n-2 (to leave space for a second battery)
    for i in range(n - 1):
        # Iterate through all possible positions for the second battery (units digit)
        # The second battery must be at an index greater than the first battery's index
        for j in range(i + 1, n):
            # Extract the digits and convert them to integers
            digit1 = int(bank_string[i])
            digit2 = int(bank_string[j])

            # Form the two-digit joltage value
            current_joltage = digit1 * 10 + digit2

            # Update the maximum joltage found so far for this bank
            if current_joltage > max_joltage:
                max_joltage = current_joltage
    return max_joltage

def solve():
    """
    Reads battery bank data from 'input.txt', calculates the maximum joltage
    for each bank, and then sums these maximums to find the total output joltage.
    """
    total_output_joltage = 0
    input_file_name = "input.txt"

    # Check if the input file exists before attempting to open it
    if not os.path.exists(input_file_name):
        print(f"Error: The input file '{input_file_name}' was not found.")
        print("Please ensure 'input.txt' is in the same directory as the script,")
        print("and contains your puzzle input (one battery bank string per line).")
        return

    try:
        with open(input_file_name, "r") as f:
            # Enumerate lines to provide line number in case of an issue (optional, but good practice)
            for line_num, line in enumerate(f, 1):
                bank_string = line.strip() # Remove leading/trailing whitespace, including newline characters

                if not bank_string:
                    # Skip empty lines, as they don't represent a battery bank
                    # print(f"Warning: Skipping empty line {line_num} in input file.")
                    continue

                # Calculate the maximum joltage for the current bank
                max_joltage_current_bank = calculate_max_joltage_for_bank(bank_string)
                
                # Add it to the running total
                total_output_joltage += max_joltage_current_bank

    except Exception as e:
        # Catch any other potential errors during file processing
        print(f"An unexpected error occurred while processing the input file: {e}")
        return

    print(f"The total output joltage is: {total_output_joltage}")

# This ensures the solve() function is called only when the script is executed directly
if __name__ == "__main__":
    solve()