# MapReduce

MapReduce is a programming model for processing large datasets in parallel across a cluster. The programmer writes two functions, `map` and `reduce`. The runtime handles partitioning the input, scheduling tasks, moving intermediate data, retrying failures, and collecting output.

## The model

```
map:    (k1, v1)        -> list(k2, v2)
reduce: (k2, list(v2))  -> list(k3, v3)
```

Map runs independently on each input record. Reduce receives all values for one key. The framework guarantees that every value with the same intermediate key reaches the same reducer.

## Execution pipeline

1. **Input splits.** The input is divided into splits, usually one per HDFS block. Each split becomes one map task.
2. **Map.** Each mapper emits intermediate pairs. Output is buffered in memory, spilled to local disk when full, and partitioned by key.
3. **Shuffle and sort.** Reducers fetch their partitions from every mapper over the network. Each partition is merged and sorted by key.
4. **Reduce.** For each key, the reducer receives the key and an iterator over its values, and emits output.
5. **Output.** Each reducer writes one file, `part-r-NNNNN`, to HDFS.

## Word count, traced

Input: `"the cat sat"` and `"the dog ran"`.

| Stage | Contents |
|---|---|
| Map output | (the,1) (cat,1) (sat,1) (the,1) (dog,1) (ran,1) |
| After shuffle | the:[1,1] cat:[1] sat:[1] dog:[1] ran:[1] |
| Reduce output | (the,2) (cat,1) (sat,1) (dog,1) (ran,1) |

## Combiners

A combiner runs the reduce logic on each mapper's local output before the shuffle. It reduces network traffic. It is only valid when the operation is associative and commutative: sums, counts, and maxima qualify, while a median does not.

## Partitioners

The default partitioner hashes the key modulo the number of reducers. A custom partitioner can route keys using domain knowledge, for example to keep ordering or to balance known heavy keys. Hot keys that dominate a partition create stragglers. Remedies include key salting (split a hot key into sub-keys, then aggregate in a second job) and sampling to build range partitions.

## Data locality

The scheduler prefers to run a map task on a node that stores its block (node-local), then on the same rack (rack-local), and only then anywhere (off-rack). Reducers always fetch over the network.

## Fault tolerance

- **Worker failure**: tasks on a failed node are re-executed. Completed map outputs on that node are lost, so those maps re-run. Reduce output is in HDFS and survives.
- **Stragglers**: slow tasks can trigger speculative backup copies. The first attempt to finish wins.
- **Master**: in classic MapReduce the job coordinator is a single point of failure. YARN separates per-job coordination (ApplicationMaster) from cluster resource management (ResourceManager).

## Common patterns

- **Filtering**: map-only job that emits only matching records.
- **Top-N**: each mapper keeps a local top-N, then one reducer merges.
- **Inverted index**: emit (term, docID), reducer builds a sorted posting list.
- **Reduce-side join**: tag records by source, emit the join key, match inside the reducer.
- **Secondary sort**: use a composite key so values arrive in a chosen order.
- **Iterative algorithms**: chain jobs. Each iteration rereads and rewrites HDFS, which is slow.

## Limitations

- Every stage writes to disk, which hurts iterative and interactive workloads.
- Job startup and scheduling overhead dominate short jobs.
- The two-phase model is awkward for multi-stage pipelines, graphs, and streams.

These limits motivated in-memory engines such as Apache Spark.

## Hadoop Streaming

Streaming lets any executable act as mapper or reducer. Mappers read lines from stdin and write `key<TAB>value` lines to stdout. Reducers receive the lines sorted by key, so they only need to detect key changes.
