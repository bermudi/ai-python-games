def main():
    total_joltage = 0
    
    with open('input.txt', 'r') as file:
        for line in file:
            bank = line.strip()
            if not bank:
                continue
                
            max_joltage = 0
            
            # Check all possible pairs of positions (i < j)
            for i in range(len(bank)):
                for j in range(i + 1, len(bank)):
                    # Form the 2-digit number: 10*digit[i] + digit[j]
                    joltage = 10 * int(bank[i]) + int(bank[j])
                    if joltage > max_joltage:
                        max_joltage = joltage
            
            total_joltage += max_joltage
    
    print(f"Total output joltage: {total_joltage}")

if __name__ == "__main__":
    main()