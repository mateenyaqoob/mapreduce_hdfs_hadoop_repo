#!/usr/bin/env bash
# Submit a Hadoop Streaming job.
# Usage: ./scripts/run_hadoop.sh <job_name> <local_input> <hdfs_input_dir> <hdfs_output_dir>
# job_name is one of: wordcount, inverted_index
set -euo pipefail

JOB="${1:?job name: wordcount or inverted_index}"
LOCAL_INPUT="${2:?local input file}"
HDFS_IN="${3:?HDFS input directory}"
HDFS_OUT="${4:?HDFS output directory (must not exist)}"

: "${HADOOP_HOME:?set HADOOP_HOME}"
JOB_DIR="src/$JOB"
STREAMING_JAR=$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n 1)

hdfs dfs -mkdir -p "$HDFS_IN"
hdfs dfs -put -f "$LOCAL_INPUT" "$HDFS_IN/"

hadoop jar "$STREAMING_JAR" \
  -D mapreduce.job.name="$JOB" \
  -input "$HDFS_IN" \
  -output "$HDFS_OUT" \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file "$JOB_DIR/mapper.py" \
  -file "$JOB_DIR/reducer.py"

echo "Results in $HDFS_OUT:"
hdfs dfs -cat "$HDFS_OUT/part-*" | head -n 20
