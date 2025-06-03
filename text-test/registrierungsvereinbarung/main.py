import re
import sys

def get_longest_unique_words(text: str, limit: int = 10) -> list[str]:
    # Normalize text: lowercase, keep German letters, split on non-letter
    words = re.findall(r"[a-zA-ZäöüÄÖÜß]+", text.lower())
    unique_words = set(words)
    # Sort by length (desc), then alphabetical for tie-breaking
    sorted_words = sorted(unique_words, key=lambda w: (-len(w), w))
    return sorted_words[:limit]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
            sys.exit(1)
    else:
        print("Please enter the German text to analyze (finish by pressing Enter on an empty line):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        input_text = '\n'.join(lines)
    result = get_longest_unique_words(input_text)
    print("\nLongest unique words:")
    for i, word in enumerate(result, 1):
        print(f"{i}. {word}")