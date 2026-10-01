#!/bin/bash
# Measure average rate and bandwidth of ROS 2 topics.
# Usage: tests/tools/topic_rates.sh [seconds] /topic1 /topic2 ...
set -u
DUR=8
if [[ "${1:-}" =~ ^[0-9]+$ ]]; then DUR=$1; shift; fi

printf "%-48s %10s %12s\n" "topic" "rate (Hz)" "bandwidth"
for t in "$@"; do
  hz=$(timeout -s INT "$DUR" ros2 topic hz "$t" 2>&1 | grep "average rate" | tail -1 | awk '{print $3}')
  bw=$(timeout -s INT "$DUR" ros2 topic bw "$t" 2>&1 | grep -E "B/s from" | tail -1 | awk '{print $1, $2}')
  printf "%-48s %10s %12s\n" "$t" "${hz:-none}" "${bw:-none}"
done
