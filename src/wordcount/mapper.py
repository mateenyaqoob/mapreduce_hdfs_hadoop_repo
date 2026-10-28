#!/usr/bin/env python3
"""Word count mapper for Hadoop Streaming.

Reads text lines from stdin, emits "word<TAB>1" for each word.
"""
import sys


def main(stream=sys.stdin, out=sys.stdout):
    for line in stream:
        for word in line.split():
            out.write(f"{word.lower()}\t1\n")


if __name__ == "__main__":
    main()
