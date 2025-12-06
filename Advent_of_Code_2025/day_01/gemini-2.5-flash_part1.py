import os


def solve_secret_entrance(input_data):
    """
    Calculates the number of times the safe dial points to 0 after a sequence of rotations.

    Args:
        input_data (str): A multi-line string where each line represents a rotation
                          (e.g., "L68", "R48").

    Returns:
        int: The total number of times the dial lands on 0.
    """
    current_position = 50  # The dial starts pointing at 50
    zero_count = 0  # Counter for how many times the dial lands on 0

    # Split the input data into individual rotation instructions
    # .strip() removes any leading/trailing whitespace, .split('\n') breaks it into lines
    lines = input_data.strip().split("\n")

    for line in lines:
        # Skip empty lines that might result from extra newlines in the input file
        if not line:
            continue

        # Extract the direction (first character) and distance (rest of the string)
        direction = line[0]
        distance = int(line[1:])  # Convert the distance string to an integer

        if direction == "R":
            # For a right rotation, add the distance and take modulo 100
            current_position = (current_position + distance) % 100
        elif direction == "L":
            # For a left rotation, subtract the distance and take modulo 100.
            # Python's % operator handles negative results correctly for positive moduli,
            # e.g., -18 % 100 results in 82, which is correct for a circular dial.
            current_position = (current_position - distance) % 100
        else:
            # Handle unexpected directions, though the problem implies only 'L' or 'R'
            # This is a good practice for robust code.
            raise ValueError(f"Invalid direction '{direction}' found in line: {line}")

        # Check if the dial landed on 0 after this rotation
        if current_position == 0:
            zero_count += 1

    return zero_count


# --- Main execution block ---
if __name__ == "__main__":
    # Example input from the problem description for testing purposes
    example_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    example_password = solve_secret_entrance(example_input)
    print(f"Example password (should be 3): {example_password}\n")

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

            actual_password = solve_secret_entrance(puzzle_input)
            print(f"Actual password from '{input_file_name}': {actual_password}")
        except Exception as e:
            print(
                f"An error occurred while reading or processing '{input_file_name}': {e}"
            )
