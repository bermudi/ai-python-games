# Advent of Code 2025 - Day 01: Secret Entrance

This directory contains solutions from various AI models for Advent of Code Day 1. The problem involves a circular dial with 100 positions (0-99) that starts at position 50 and rotates according to a series of instructions.

## Problem Description

The safe has a dial with 100 positions (0-99) and starts at position 50. Each line in the input represents a rotation:
- `L#` means rotate left by # positions
- `R#` means rotate right by # positions

**Part 1:** Count how many times the dial lands on position 0 after each complete rotation.
**Part 2:** Count how many times the dial points to 0 during ANY step of the rotation (including intermediate positions).

## Correct Answers

- **Part 1:** 1026
- **Part 2:** 5923

## Results Summary

| Model | Part 1 | Part 2 | Part 1 Correct | Part 2 Correct |
|-------|--------|--------|----------------|----------------|
| DeepSeek V3.2 | 1026 | 5923 | ✅ | ✅ |
| Gemini 2.5 Flash | 1026 | 5923 | ✅ | ✅ |
| Gemini 3 Pro | - | 5923 | - | ✅ |
| GLM-4.6 | 904 | - | ❌ | - |
| GLM-4.6 Thinking | 1026 | 6984 | ✅ | ❌ |
| GPT-5 Mini | 1026 | 5923 | ✅ | ✅ |
| GPT-OSS 120B | 1026 | 5923 | ✅ | ✅ |
| Grok-4.1 NR | 1026 | 6431 | ✅ | ❌ |
| Grok-4.1 Reasoning | - | 5923 | - | ✅ |
| Grok Code Fast 1 | 1026 | 5923 | ✅ | ✅ |
| Kimi K2 Thinking | 1026 | 5923 | ✅ | ✅ |
| MiniMax M2 | 1026 | 5923 | ✅ | ✅ |
| Opus 4.5 | 1026 | 5923 | ✅ | ✅ |

## Performance Analysis

### Part 1 Results (Expected: 1026)
- **Correct (12/13 models):** All models except GLM-4.6 got the correct answer
- **Incorrect:** GLM-4.6 produced 904 instead of 1026
- **Success Rate:** 92.3%

### Part 2 Results (Expected: 5923)
- **Correct (9/10 models):** Most models got the correct answer
- **Incorrect:** 
  - GLM-4.6 Thinking: 6984 (off by 1061)
  - Grok-4.1 NR: 6431 (off by 508)
- **Success Rate:** 90.0%

## Why Failed Models Failed

### GLM-4.6 (Part 1) - Wrong Position Calculation
**Error:** Incorrect handling of left rotations
```python
if direction == "L":
    current_position -= distance
    if current_position < 0:
        current_position += 100  # Only adds back 100 once!
```
**Issue:** This only handles one full rotation. For distances > 100, it should use modulo arithmetic like `current_position = (current_position - distance) % 100`.

### GLM-4.6 Thinking (Part 2) - Double Counting
**Error:** Counting the final position twice
```python
# During rotation counting (lines 22, 27, 34, 39)
if position + remaining >= 100:
    count += 1

# Then counting again at the end (lines 44-46)
if position == 0:
    count += 1  # Double counting!
```
**Issue:** The algorithm counts zeros during rotation AND then counts the final position again, leading to overcounting.

### Grok-4.1 NR (Part 2) - Flawed Counting Logic
**Error:** Incorrect logic for counting zeros in left rotations
```python
# From lines 48-50
zero_count += full_circles  # each full circle passes 0 once
if remainder >= to_zero and to_zero > 0:
    zero_count += 1  # pass 0 in first partial circle
```
**Issue:** The condition `remainder >= to_zero` doesn't correctly determine if zero is passed during the partial rotation. The logic doesn't properly account for the circular nature of the dial.

## Key Insights

1. **Part 1 was easier** - Nearly all models (92.3%) got it correct, suggesting the problem of counting final positions is straightforward for AI models.

2. **Part 2 was more challenging** - 90.0% success rate, indicating that counting intermediate positions during rotation requires more sophisticated mathematical reasoning.

3. **GLM-4.6 struggled with both parts** - The non-thinking version failed Part 1, while the thinking version failed Part 2, suggesting inconsistent problem-solving approaches.

4. **Grok models showed mixed results** - The reasoning version got Part 2 correct while the NR (non-reasoning) version failed, showing the benefit of explicit reasoning.

5. **Most models performed well** - 12 out of 13 models got Part 1 correct, and 9 out of 10 models with Part 2 solutions got it correct, demonstrating strong overall performance on this problem.

## File Structure

Each Python file represents a solution from a different AI model:
- Files ending in `_part2.py` contain solutions for Part 2
- All files read from `input.txt` in the same directory
- Solutions use varying approaches, from simple simulation to mathematical formulas