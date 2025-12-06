# ------------------------------------------------------------
# Advent of Code – Day 1 (Safe dial)
# Reads the rotation list from 'input.txt' and prints the password
# ------------------------------------------------------------

def main() -> None:
    # 1. read input
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # 2. initialise
    pos = 50          # starting point
    zero_cnt = 0      # how many times we land on 0

    # 3. process each rotation
    for instr in lines:
        direction = instr[0]                # 'L' or 'R'
        distance = int(instr[1:])            # the numeric part

        # decide sign of the move
        delta = -distance if direction == 'L' else distance

        # update position on a circular dial of size 100
        pos = (pos + delta) % 100

        # count occurrences of 0
        if pos == 0:
            zero_cnt += 1

    # 4. output the password
    print(zero_cnt)


if __name__ == "__main__":
    main()