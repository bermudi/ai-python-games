 # Advent of Code 2025 — Day 03

This directory holds the Advent of Code 2025 Day 03 solutions generated with a variety of models. Each Python module reads `input.txt` and was executed through `uv run <script>` to validate the published answers. Both part-one and part-two scripts now follow a `_part1`/`_part2` naming pattern for clarity.

* **Part One:** `17330`
* **Part Two:** `171518260283767`

## Execution summary

The tables below capture the runtime, size, and answer status for each script. Every script that prints `17330` or `171518260283767` is marked ✅. Scripts that fell short of the published answer are noted explicitly.

### Part One (two-digit joltage per bank)

| Script | Model | Time (s) | Lines | Result |
| --- | --- | ---: | ---: | --- |
| `claude-haiku-4.5_part1.py` | Claude Haiku 4.5 | 0.822 | 23 | ✅ 17330 |
| `deepseek-v3.2-t_part1.py` | DeepSeek v3.2 | 0.033 | 24 | ✅ 17330 |
| `gemini-2.5-flash-t_part1.py` | Gemini 2.5 Flash | 0.457 | 87 | ✅ 17330 |
| `gemini-3-pro-tools_part1.py` | Gemini 3 Pro Tools | 0.035 | 48 | ✅ 17330 |
| `gemini-3-pro_part1.py` | Gemini 3 Pro | 0.106 | 39 | ✅ 17330 |
| `glm-4.6-t_part1.py` | GLM 4.6 | 0.411 | 25 | ✅ 17330 |
| `gpt-5-mini-t_part1.py` | GPT-5 Mini | 0.103 | 48 | ✅ 17330 |
| `gpt-oss-120b_part1.py` | GPT-OSS 120B | 0.043 | 52 | ✅ 17330 |
| `grok-4.1-fast-nr_part1.py` | Grok 4.1 Fast NR | 0.521 | 25 | ✅ 17330 |
| `grok-4.1-fast-r_part1.py` | Grok 4.1 Fast R | 0.040 | 20 | ✅ 17330 |
| `grok-code-fast-1_part1.py` | Grok Code Fast 1 | 0.043 | 28 | ✅ 17330 |
| `kimi-k2-t_part1.py` | Kimi K2 T | 0.036 | 46 | ✅ 17330 |
| `minimax-m2_part1.py` | Minimax M2 | 0.047 | 60 | ✅ 17330 |
| `qwen-coder-3_part1.py` | Qwen Coder 3 | 0.434 | 18 | ✅ 17330 |

### Part Two (twelve-digit joltage per bank)

| Script | Model | Time (s) | Lines | Result |
| --- | --- | ---: | ---: | --- |
| `claude-haiku-4.5_part2.py` | Claude Haiku 4.5 | 0.044 | 47 | ✅ 171518260283767 |
| `deepseek-v3.2-t_part2.py` | DeepSeek v3.2 | 0.039 | 32 | ✅ 171518260283767 |
| `gemini-2.5-flash-t_part2.py` | Gemini 2.5 Flash | 0.033 | 174 | ✅ 171518260283767 |
| `gemini-3-pro-tools_part2.py` | Gemini 3 Pro Tools | 0.038 | 56 | ✅ 171518260283767 |
| `gemini-3-pro_part2.py` | Gemini 3 Pro | 0.039 | 54 | ✅ 171518260283767 |
| `glm-4.6-t_part2.py` | GLM 4.6 | 0.030 | 40 | ✅ 171518260283767 |
| `gpt-5-mini-t_part2.py` | GPT-5 Mini | 0.045 | 57 | ✅ 171518260283767 |
| `gpt-oss-120b_part2.py` | GPT-OSS 120B | 0.052 | 61 | ✅ 171518260283767 |
| `grok-4.1-fast-nr_part2.py` | Grok 4.1 Fast NR | 0.143 | 38 | ✅ 171518260283767 (second pass) |
| `grok-4.1-fast-r_part2.py` | Grok 4.1 Fast R | 0.047 | 29 | ✅ 171518260283767 |
| `grok-code-fast-1_part2.py` | Grok Code Fast 1 | 0.029 | 25 | ✅ 171518260283767 |
| `minimax-m2_part2.py` | Minimax M2 | 0.036 | 58 | ✅ 171518260283767 |
| `qwen-coder-3_part2.py` | Qwen Coder 3 | 0.030 | 27 | ✅ 171518260283767 |

## Notes

1. All part-one scripts produce `17330`, matching the documented answer.
2. Every part-two script with substantive logic prints `171518260283767`. Grok 4.1 Fast NR required a second pass; the newer version (0.143s, 38 LOC) now produces the target result.
