def main():
    total_joltage = 0
    
    with open('input.txt', 'r') as file:
        for line in file:
            bank = line.strip()
            if not bank:
                continue
            
            n = len(bank)
            if n < 12:
                continue
            
            # dp[i][k] = largest k-digit number using first i digits
            dp = [[0] * 13 for _ in range(n + 1)]
            
            # Base case: single digit
            for i in range(1, n + 1):
                dp[i][1] = max(dp[i-1][1], int(bank[i-1]))
            
            # Fill DP table
            for i in range(1, n + 1):
                for k in range(2, 13):
                    # Don't take current digit
                    dp[i][k] = dp[i-1][k]
                    
                    # Take current digit (if we had k-1 digits before)
                    if k - 1 >= 1 and dp[i-1][k-1] > 0:
                        current_digit = int(bank[i-1])
                        new_num = dp[i-1][k-1] * 10 + current_digit
                        dp[i][k] = max(dp[i][k], new_num)
            
            total_joltage += dp[n][12]
    
    print(f"Total output joltage: {total_joltage}")

if __name__ == "__main__":
    main()