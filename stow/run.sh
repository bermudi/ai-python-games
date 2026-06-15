#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODELS_FILE="$SCRIPT_DIR/models.txt"
RESULTS_FILE="$SCRIPT_DIR/results.txt"
PI_TIMEOUT=600  # 10 minutes per pi invocation

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ ! -f "$MODELS_FILE" ]; then
  echo -e "${RED}models.txt not found. Create it with one model per line.${NC}"
  exit 1
fi

echo "=== Stow 2026 Benchmark ==="
echo "Started at $(date)"
echo ""

# Use fd 3 to avoid stdin corruption from subprocesses
while IFS= read -r model <&3; do
  # Skip empty lines and comments
  [[ -z "$model" || "$model" == \#* ]] && continue

  MODEL_NAME=$(echo "$model" | tr '/' '_')
  OUTPUT_DIR="$SCRIPT_DIR/outputs/$MODEL_NAME"
  SESSION_DIR="$OUTPUT_DIR/sessions"
  PLAN_FILE="$OUTPUT_DIR/IMPLEMENTATION_PLAN.md"
  READY_FILE="$OUTPUT_DIR/PLAN_READY"
  DONE_FILE="$OUTPUT_DIR/BUILD_DONE"
  MAX_PLAN_ITERS=10
  MAX_BUILD_ITERS=8
  PLAN_ITERS=0
  BUILD_ITERS=0

  echo "──────────────────────────────────────────────"
  echo -e "Model: ${YELLOW}$model${NC}"
  echo "Output: $OUTPUT_DIR"
  echo ""

  # Setup
  mkdir -p "$OUTPUT_DIR" "$SESSION_DIR"
  cp "$SCRIPT_DIR/spec.md" "$OUTPUT_DIR/spec.md"
  cd "$OUTPUT_DIR" && git init && git config user.email "benchmark@stow.local" && git config user.name "Stow Benchmark"

  # ── Phase 1: Planning (Ralph Loop) ──
  echo -e "${YELLOW}[Phase 1] Planning...${NC}"
  PLAN_START=$(date +%s)

  while [ ! -f "$READY_FILE" ] && [ $PLAN_ITERS -lt $MAX_PLAN_ITERS ]; do
    PLAN_ITERS=$((PLAN_ITERS + 1))
    echo "  Iteration $PLAN_ITERS/$MAX_PLAN_ITERS... "

    cd "$OUTPUT_DIR"
    if timeout $PI_TIMEOUT pi -p \
         --model "$model" \
         --session-dir "$SESSION_DIR" \
         @"$SCRIPT_DIR/PROMPT_plan.md" \
         2>&1; then
      echo "  ✓"
    else
      echo -e "  ${RED}✗ pi timed out or exited with error${NC}"
    fi
  done

  PLAN_END=$(date +%s)
  PLAN_DURATION=$((PLAN_END - PLAN_START))

  if [ -f "$READY_FILE" ]; then
    echo -e "${GREEN}[Phase 1] Plan complete in ${PLAN_DURATION}s (${PLAN_ITERS} iterations)${NC}"
  else
    echo -e "${RED}[Phase 1] Plan did not complete after ${PLAN_ITERS} iterations (${PLAN_DURATION}s)${NC}"
  fi
  echo ""

  # ── Phase 2: Build (Ralph Loop) ──
  echo -e "${YELLOW}[Phase 2] Building...${NC}"
  BUILD_START=$(date +%s)

  while [ ! -f "$DONE_FILE" ] && [ $BUILD_ITERS -lt $MAX_BUILD_ITERS ]; do
    BUILD_ITERS=$((BUILD_ITERS + 1))
    echo "  Iteration $BUILD_ITERS/$MAX_BUILD_ITERS... "

    cd "$OUTPUT_DIR"
    if timeout $PI_TIMEOUT pi -p \
         --model "$model" \
         --session-dir "$SESSION_DIR" \
         @"$SCRIPT_DIR/PROMPT_build.md" \
         2>&1; then
      echo "  ✓"
    else
      echo -e "  ${RED}✗ pi timed out or exited with error${NC}"
    fi
  done

  BUILD_END=$(date +%s)
  BUILD_DURATION=$((BUILD_END - BUILD_START))

  if [ -f "$DONE_FILE" ]; then
    echo -e "${GREEN}[Phase 2] Build complete in ${BUILD_DURATION}s (${BUILD_ITERS} iterations)${NC}"
  else
    echo -e "${RED}[Phase 2] Build did not complete after ${BUILD_ITERS} iterations (${BUILD_DURATION}s)${NC}"
  fi
  echo ""

  # ── Record results ──
  TOTAL=$((PLAN_DURATION + BUILD_DURATION))
  echo "$model | plan: ${PLAN_DURATION}s (${PLAN_ITERS} iters) | build: ${BUILD_DURATION}s (${BUILD_ITERS} iters) | total: ${TOTAL}s" >> "$RESULTS_FILE"

done 3< "$MODELS_FILE"

echo "──────────────────────────────────────────────"
echo "Done at $(date)"
echo "Results in $RESULTS_FILE"
