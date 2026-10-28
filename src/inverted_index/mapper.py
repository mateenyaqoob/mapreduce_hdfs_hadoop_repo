#!/usr/bin/env python3
"""Inverted index mapper for Hadoop Streaming.

Input lines have the form "doc_id<TAB>text".
Emits "word<TAB>doc_id" once per distinct word in each document.
"""
import sys


def main(stream=sys.stdin, out=sys.stdout):
    for line in stream:
        doc_id, _, text = line.rstrip("\n").partition("\t")
        if not doc_id:
            continue
        for word in set(text.lower().split()):
            out.write(f"{word}\t{doc_id}\n")


if __name__ == "__main__":
    main()
