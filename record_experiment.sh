#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./record_experiment.sh [run_name]
# Example:
#   ./record_experiment.sh corridor_trial_01

RUN_NAME="${1:-run}"
STAMP="$(date +%Y%m%d_%H%M%S_%N)"
BAG_ROOT="${HOME}/cdoa_ros2/bags"
OUT_DIR="${BAG_ROOT}/${RUN_NAME}_${STAMP}"
META_FILE="${OUT_DIR}/run_info.txt"

mkdir -p "${BAG_ROOT}"

# Core topics for localization + wireless experiments.
TOPICS=(
  /odometry/wheels
  /cmd_vel
  /tf
  /tf_static
  /node1/network_analysis/wireless_quality
  /node2/network_analysis/wireless_quality
  /node3/network_analysis/wireless_quality
  /node4/network_analysis/wireless_quality
)

# Include /clock automatically when available (simulation or synchronized playback).
if ros2 topic list | grep -qx "/clock"; then
  TOPICS+=(/clock)
fi

# Optional extra topics can be passed through EXTRA_TOPICS env var.
# Example:
#   EXTRA_TOPICS="/imu/data /pf_pose /diagnostics" ./record_experiment.sh run02
if [[ -n "${EXTRA_TOPICS:-}" ]]; then
  read -r -a EXTRA_ARRAY <<< "${EXTRA_TOPICS}"
  TOPICS+=("${EXTRA_ARRAY[@]}")
fi

echo "Saving rosbag to: ${OUT_DIR}"
echo "Metadata file will be written to: ${META_FILE}"
echo "Press Ctrl+C to stop recording."

ros2 bag record -o "${OUT_DIR}" "${TOPICS[@]}"

if [[ -d "${OUT_DIR}" ]]; then
  {
    echo "run_name=${RUN_NAME}"
    echo "timestamp=${STAMP}"
    echo "output_dir=${OUT_DIR}"
    echo "notes=fill_me_before_report"
    echo "area_size=3.048x3.96"
    echo "anchor_positions=(0,0),(0,3.96),(3.048,3.96),(3.048,0)"
    echo "topics=${TOPICS[*]}"
  } > "${META_FILE}"
  echo "Metadata saved: ${META_FILE}"
fi
