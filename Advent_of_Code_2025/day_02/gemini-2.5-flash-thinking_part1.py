import sys

# Function to check if a number is an invalid product ID
def is_invalid_id(n: int) -> bool:
    """
    Checks if a given integer 'n' is an invalid product ID.

    An ID is invalid if its string representation consists of a sequence of digits
    repeated exactly twice (e.g., 55, 6464, 123123).
    Numbers with leading zeros (like '0101') are not considered valid IDs,
    and single-digit numbers are also not invalid IDs.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if 'n' is an invalid ID, False otherwise.
    """
    s = str(n)
    length = len(s)

    # 1. Handle small numbers:
    # The smallest repeating pattern is '11'. Any number less than 11
    # cannot be an invalid ID. This also correctly handles single-digit numbers and 0.
    # The problem states "None of the numbers have leading zeroes; `0101` isn't an ID at all."
    # Since we convert integers to strings, `str(101)` is "101", which doesn't have a leading zero.
    # This check ensures that numbers like 0, 1, ..., 10 are not considered invalid.
    if n < 11:
        return False

    # 2. Check for even length:
    # An invalid ID must have an even number of digits to be split into two equal halves.
    if length % 2 != 0:
        return False

    # 3. Compare halves:
    # Split the string into two halves and check if they are identical.
    mid = length // 2
    first_half = s[0:mid]
    second_half = s[mid:length]

    return first_half == second_half

def solve():
    """
    Reads product ID ranges from 'input.txt', identifies invalid IDs within those ranges,
    and calculates their sum.
    """
    total_sum_of_invalid_ids = 0

    # Attempt to read the input file
    try:
        with open('input.txt', 'r') as f:
            input_line = f.readline().strip()
    except FileNotFoundError:
        print("Error: input.txt not found. Please make sure the file is in the same directory.", file=sys.stderr)
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading input.txt: {e}", file=sys.stderr)
        return

    # Split the input line into individual range strings
    ranges_str = input_line.split(',')

    # Process each range
    for r_str in ranges_str:
        # Skip empty strings that might result from extra commas
        if not r_str:
            continue

        try:
            # Split each range string into start and end values
            start_str, end_str = r_str.split('-')
            start = int(start_str)
            end = int(end_str)
        except ValueError:
            # Handle cases where a range string is malformed (e.g., "abc", "123", "123-xyz")
            print(f"Warning: Skipping malformed range '{r_str}'. Expected 'start-end' format with integers.", file=sys.stderr)
            continue

        # Iterate through all numbers in the current range (inclusive)
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_sum_of_invalid_ids += num

    # Print the final calculated sum
    print(f"The sum of all invalid IDs is: {total_sum_of_invalid_ids}")

if __name__ == "__main__":
    solve()
