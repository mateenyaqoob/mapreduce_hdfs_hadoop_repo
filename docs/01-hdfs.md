# HDFS

HDFS is a distributed file system designed to store very large files across commodity machines. It favors high sequential throughput and fault tolerance over low-latency random access.

## Architecture

- **NameNode**: the master. Holds the namespace (directories, file names, permissions) and the mapping from each file to its blocks and their locations. Metadata lives in memory and is persisted through an edit log and fsimage.
- **DataNodes**: workers. Store block replicas on local disks, serve reads and writes, and send periodic heartbeats and block reports to the NameNode.
- **Clients**: ask the NameNode where blocks live, then read or write blocks directly with DataNodes. Bulk data never flows through the NameNode.

## Blocks

Files are split into blocks. The default block size is 128 MB in Hadoop 2.x and later. Large blocks reduce metadata volume and favor sequential reads. A file smaller than one block does not consume a full block on disk, but each small file still costs NameNode memory, which is why many tiny files are a known problem.

## Replication

Each block has a replication factor, 3 by default. Placement is rack-aware: the first replica goes on the writer's node (or a random node), the second on a different rack, and the third on the same rack as the second but a different node. This survives both node and rack failures while keeping write traffic reasonable.

## Fault tolerance

- **Heartbeats**: a DataNode that stops heartbeating is declared dead after a timeout. Its blocks are re-replicated from surviving replicas.
- **Checksums**: data is checksummed, and a client that reads a corrupt replica reports it and reads another copy.
- **Edit log and fsimage**: protect namespace metadata. The Secondary NameNode or Standby NameNode (in HA setups) merges them periodically.
- **High availability**: a Standby NameNode with shared edit logs (QJM) allows failover. Without HA, the NameNode is a single point of failure.

## Write and read paths

Write: the client asks the NameNode to create a file, then streams data in a pipeline through the chosen DataNodes. Each replica acknowledges back up the pipeline.

Read: the client asks the NameNode for block locations, then reads from the closest replica, which may be on the same node or rack.

## Command reference

```bash
hdfs dfs -mkdir -p /user/$USER/data          # create directories
hdfs dfs -put local.txt /user/$USER/data/    # upload
hdfs dfs -get /user/$USER/data/local.txt .   # download
hdfs dfs -ls -R /user/$USER                  # list recursively
hdfs dfs -cat /user/$USER/data/local.txt     # print contents
hdfs dfs -du -h /user/$USER                  # space used
hdfs dfs -setrep -w 2 /user/$USER/data/x.txt # change replication factor and wait
hdfs dfs -rm -r /user/$USER/old              # delete recursively
hdfs fsck /user/$USER -files -blocks -locations   # check health, blocks, and replica locations
hdfs dfsadmin -report                        # cluster capacity and live DataNodes
hdfs getconf -confKey dfs.blocksize          # read a configuration value
```

## Common pitfalls

- **Small files**: thousands of tiny files exhaust NameNode heap. Combine them into SequenceFiles, Avro, or Parquet before processing.
- **Replication for scratch data**: intermediate data does not need replication 3. Lower it to reduce storage cost.
- **Assuming POSIX semantics**: HDFS files are write-once in the classic model. Appends are supported, but random in-place updates are not.
- **Forgetting the NameNode is a bottleneck**: every metadata operation goes through it, so avoid chatty clients that issue millions of small metadata calls.
