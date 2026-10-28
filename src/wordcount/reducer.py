#!/usr/bin/env python3
"""Word count reducer for Hadoop Streaming.

Input lines arrive sorted by key: "word<TAB>count".
The reducer sums counts for each run of identical keys.
"""
import sys


def main(stream=sys.stdin, out=sys.stdout):
    current, total = None, 0
    for line in stream:
        key, _, value = line.rstrip("\n").partition("\t")
        if key != current:
            if current is not None:
                out.write(f"{current}\t{total}\n")
            current, total = key, 0
        total += int(value)
    if current is not None:
        out.write(f"{current}\t{total}\n")


if __name__ == "__main__":
    main()
