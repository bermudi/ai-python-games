import os

# math.floor and math.ceil are explicitly used for clarity in the formulas.


def solve_secret_entrance_part2(input_data):
    """
    Calculates the number of times the safe dial points to 0 during any click
    of a rotation, including the final position.

    Args:
        input_data (str): A multi-line string where each line represents a rotation
                          (e.g., "L68", "R48").

    Returns:
        int: The total number of times the dial lands on 0 during all rotations.
    """
    current_position = 50  # The dial starts pointing at 50
    zero_count = 0  # Counter for how many times the dial lands on 0

    # Split the input data into individual rotation instructions
    lines = input_data.strip().split("\n")

    for line in lines:
        if not line:  # Skip empty lines
            continue

        direction = line[0]
        distance = int(line[1:])

        prev_pos = current_position  # Store position before rotation for counting logic

        if direction == "R":
            # For a right rotation, we count multiples of 100 in the range (prev_pos, prev_pos + distance].
            # The number of multiples of N in (A, B] is floor(B/N) - floor(A/N).
            # Using Python's floor division (//) which works correctly for negative numbers as well.
            zero_count_this_rotation = (prev_pos + distance) // 100 - prev_pos // 100
            current_position = (prev_pos + distance) % 100
        elif direction == "L":
            # For a left rotation, we count multiples of 100 in the range [prev_pos - distance, prev_pos - 1].
            # The number of multiples of N in [A, B] is floor(B/N) - floor((A-1)/N).
            # Here, A = prev_pos - distance, B = prev_pos - 1.
            zero_count_this_rotation = (prev_pos - 1) // 100 - (
                prev_pos - distance - 1
            ) // 100
            current_position = (prev_pos - distance) % 100
        else:
            raise ValueError(f"Invalid direction '{direction}' found in line: {line}")

        zero_count += zero_count_this_rotation

    return zero_count


# --- Main execution block ---
if __name__ == "__main__":
    # Example input from the problem description for Part 2
    example_input_part2 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    example_password_part2 = solve_secret_entrance_part2(example_input_part2)
    print(f"Example Part 2 password (should be 6): {example_password_part2}\n")

    # Read the actual puzzle input from 'input.txt'
    input_file_name = "input.txt"

    if not os.path.exists(input_file_name):
        print(f"Error: The file '{input_file_name}' was not found.")
        print("Please create an 'input.txt' file in the same directory as this script")
        print("and paste your puzzle input into it.")
    else:
        try:
            with open(input_file_name, "r") as f:
                puzzle_input = f.read()

            actual_password_part2 = solve_secret_entrance_part2(puzzle_input)
            print(
                f"Actual Part 2 password from '{input_file_name}': {actual_password_part2}"
            )
        except Exception as e:
            print(
                f"An error occurred while reading or processing '{input_file_name}': {e}"
            )
