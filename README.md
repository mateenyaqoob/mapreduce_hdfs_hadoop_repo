# MapReduce and HDFS

Material and runnable examples for the Hadoop Distributed File System (HDFS) and the MapReduce programming model.

## Contents

| Path | What it is |
|---|---|
| `docs/01-hdfs.md` | HDFS architecture, blocks, replication, fault tolerance, command reference |
| `docs/02-mapreduce.md` | MapReduce model, execution pipeline, combiners, partitioners, fault tolerance, limits |
| `src/wordcount/` | Word count as Hadoop Streaming mapper and reducer (Python) |
| `src/inverted_index/` | Inverted index as Hadoop Streaming mapper and reducer (Python) |
| `scripts/run_hadoop.sh` | Uploads input to HDFS and submits a Streaming job |
| `scripts/run_local.sh` | Runs the same mapper and reducer locally, no cluster needed |
| `tests/test_pipeline.py` | Unit tests for mappers and reducers, plus an end-to-end local run |
| `data/` | Small sample corpus |

## Quick start (no cluster)

```bash
./scripts/run_local.sh src/wordcount data/sample.txt
python -m pytest tests -q
```

`run_local.sh` mimics the MapReduce pipeline with Unix tools: `map | sort | reduce`. The `sort` stage plays the role of the framework's shuffle, so the reducer sees all values for a key together.

## Running on a Hadoop cluster

Requires Hadoop 3.x with `HADOOP_HOME` set and HDFS running.

```bash
./scripts/run_hadoop.sh wordcount data/sample.txt /user/$USER/wc-in /user/$USER/wc-out
hdfs dfs -cat /user/$USER/wc-out/part-*
```

## Learning path

1. Read `docs/01-hdfs.md`, then practice the commands on a pseudo-distributed cluster.
2. Read `docs/02-mapreduce.md` and trace `src/wordcount` through `run_local.sh`.
3. Modify the inverted index to ignore stop words, then run the tests.
4. Run both examples on HDFS and compare the job counters with the local run.

## Requirements

- Python 3.8+ (for the Streaming scripts and tests)
- pytest (for tests only)
- Hadoop 3.x (for cluster runs only)
