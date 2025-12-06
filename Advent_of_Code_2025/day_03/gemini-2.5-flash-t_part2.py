import os

# --- Part One Code (included for completeness) ---

def calculate_max_joltage_for_bank_part1(bank_string: str) -> int:
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
    max_joltage = 0
    n = len(bank_string)

    if n < 2:
        return 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            digit1 = int(bank_string[i])
            digit2 = int(bank_string[j])
            current_joltage = digit1 * 10 + digit2
            if current_joltage > max_joltage:
                max_joltage = current_joltage
    return max_joltage

def solve_part1():
    """
    Reads battery bank data from 'input.txt', calculates the maximum joltage
    for each bank, and then sums these maximums to find the total output joltage.
    """
    total_output_joltage = 0
    input_file_name = "input.txt"

    if not os.path.exists(input_file_name):
        print(f"Error: The input file '{input_file_name}' was not found.")
        print("Please ensure 'input.txt' is in the same directory as the script,")
        print("and contains your puzzle input (one battery bank string per line).")
        return

    try:
        with open(input_file_name, "r") as f:
            for line_num, line in enumerate(f, 1):
                bank_string = line.strip()

                if not bank_string:
                    continue

                max_joltage_current_bank = calculate_max_joltage_for_bank_part1(bank_string)
                total_output_joltage += max_joltage_current_bank

    except Exception as e:
        print(f"An unexpected error occurred while processing the input file: {e}")
        return

    print(f"The total output joltage (Part One) is: {total_output_joltage}")


# --- Part Two Code ---

# Define the number of batteries to select for the joltage output in Part Two
K_BATTERIES = 12

def calculate_max_joltage_for_bank_part2(bank_string: str) -> int:
    """
    Calculates the maximum possible K-digit joltage from a single battery bank string
    by selecting K batteries (digits) that maintain their relative order.

    This uses a greedy approach to find the lexicographically largest subsequence
    of length K.

    Args:
        bank_string: A string representing a bank of batteries, where each character
                     is a digit from '1' to '9'.

    Returns:
        The largest possible K-digit joltage that can be produced from the bank.
        Returns 0 if the bank string has fewer than K batteries, as a K-digit
        joltage cannot be formed.
    """
    n = len(bank_string)

    # If the bank string is shorter than K_BATTERIES, we cannot form a K-digit number.
    # The problem implies this won't happen for valid inputs.
    if n < K_BATTERIES:
        print(f"Warning: Bank string '{bank_string}' is too short ({n} digits) to form a {K_BATTERIES}-digit joltage. Returning 0.")
        return 0

    result_digits = []
    current_start_idx = 0

    # We need to pick K_BATTERIES digits
    for i in range(K_BATTERIES):
        # Determine the maximum index we can search for the current digit.
        # This index must ensure that there are enough remaining characters
        # in the bank_string to pick the remaining (K_BATTERIES - 1 - i) digits.
        #
        # The number of digits we still need to pick is `K_BATTERIES - i`.
        # The latest possible index for the current digit (`j`) is such that
        # `n - 1 - j` (number of characters AFTER `j`) >= `K_BATTERIES - 1 - i` (number of digits still needed after current one).
        # This simplifies to `j <= n - (K_BATTERIES - i)`.
        
        # The search range for the current digit is from `current_start_idx`
        # up to `max_possible_idx_for_current_digit` (inclusive).
        max_possible_idx_for_current_digit = n - (K_BATTERIES - i)

        # Find the largest digit within the allowed search range
        # Python's max() function on a string will return the character with the highest ASCII value,
        # which works perfectly for digits '0'-'9'.
        search_slice = bank_string[current_start_idx : max_possible_idx_for_current_digit + 1]
        max_char_in_range = max(search_slice)
        
        # Find the index of the *first occurrence* of this max_char within the search slice.
        # This is crucial for the greedy strategy to work correctly (to leave more options for subsequent digits).
        best_char_idx = bank_string.find(max_char_in_range, current_start_idx, max_possible_idx_for_current_digit + 1)
        
        # Append the found max digit to our result
        result_digits.append(max_char_in_range)
        
        # Update current_start_idx for the next iteration:
        # It must be one position after the digit we just picked.
        current_start_idx = best_char_idx + 1
    
    # Join the digits and convert to an integer
    return int("".join(result_digits))

def solve_part2():
    """
    Reads battery bank data from 'input.txt', calculates the maximum K-digit joltage
    for each bank using the new rules, and then sums these maximums to find the
    total output joltage.
    """
    total_output_joltage = 0
    input_file_name = "input.txt"

    if not os.path.exists(input_file_name):
        print(f"Error: The input file '{input_file_name}' was not found.")
        print("Please ensure 'input.txt' is in the same directory as the script,")
        print("and contains your puzzle input (one battery bank string per line).")
        return

    try:
        with open(input_file_name, "r") as f:
            for line_num, line in enumerate(f, 1):
                bank_string = line.strip()

                if not bank_string:
                    continue

                max_joltage_current_bank = calculate_max_joltage_for_bank_part2(bank_string)
                total_output_joltage += max_joltage_current_bank

    except Exception as e:
        print(f"An unexpected error occurred while processing the input file: {e}")
        return

    print(f"The new total output joltage (Part Two) is: {total_output_joltage}")

# This ensures the solve functions are called only when the script is executed directly
if __name__ == "__main__":
    # Uncomment the part you want to run
    # solve_part1() # For the first part of the puzzle
    solve_part2() # For the second part of the puzzle