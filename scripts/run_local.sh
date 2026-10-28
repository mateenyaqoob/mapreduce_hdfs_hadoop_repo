#!/usr/bin/env bash
# Simulate a MapReduce job locally: map | sort | reduce.
# Usage: ./scripts/run_local.sh <job_dir> <input_file>
set -euo pipefail

JOB_DIR="${1:?job directory, e.g. src/wordcount}"
INPUT="${2:?input file}"
PY="${PYTHON:-python3}"

"$PY" "$JOB_DIR/mapper.py" < "$INPUT" | sort -k1,1 | "$PY" "$JOB_DIR/reducer.py"
