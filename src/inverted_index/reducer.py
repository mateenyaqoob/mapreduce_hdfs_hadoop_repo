#!/usr/bin/env python3
"""Inverted index reducer for Hadoop Streaming.

Input lines arrive sorted by word: "word<TAB>doc_id".
Emits "word<TAB>doc1,doc2,..." with document IDs sorted and de-duplicated.
"""
import sys


def flush(word, docs, out):
    if word is not None:
        out.write(f"{word}\t{','.join(sorted(set(docs)))}\n")


def main(stream=sys.stdin, out=sys.stdout):
    current, docs = None, []
    for line in stream:
        word, _, doc_id = line.rstrip("\n").partition("\t")
        if word != current:
            flush(current, docs, out)
            current, docs = word, []
        docs.append(doc_id)
    flush(current, docs, out)


if __name__ == "__main__":
    main()
