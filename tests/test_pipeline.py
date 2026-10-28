import importlib.util
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(mod, text):
    out = io.StringIO()
    mod.main(io.StringIO(text), out)
    return out.getvalue()


def test_wordcount_mapper_lowercases_and_splits():
    wc = load("src/wordcount/mapper.py", "wc_map")
    assert run(wc, "The the CAT\n") == "the\t1\nthe\t1\ncat\t1\n"


def test_wordcount_reducer_sums_sorted_runs():
    red = load("src/wordcount/reducer.py", "wc_red")
    assert run(red, "cat\t1\ndog\t1\ndog\t1\n") == "cat\t1\ndog\t2\n"


def test_wordcount_reducer_empty_input():
    red = load("src/wordcount/reducer.py", "wc_red2")
    assert run(red, "") == ""


def test_inverted_index_dedupes_within_document():
    mapper = load("src/inverted_index/mapper.py", "ii_map")
    lines = set(run(mapper, "d1\tbig big data\n").splitlines())
    assert lines == {"big\td1", "data\td1"}


def test_inverted_index_reducer_builds_posting_list():
    red = load("src/inverted_index/reducer.py", "ii_red")
    out = run(red, "big\td2\nbig\td1\ndata\td1\n")
    assert out == "big\td1,d2\ndata\td1\n"


def test_end_to_end_local_wordcount():
    script = ROOT / "scripts" / "run_local.sh"
    result = subprocess.run(
        ["bash", str(script), "src/wordcount", str(ROOT / "data" / "sample.txt")],
        capture_output=True, text=True, env={"PYTHON": sys.executable, "PATH": "/usr/bin:/bin"},
        check=True,
    )
    counts = dict(line.split("\t") for line in result.stdout.strip().splitlines())
    assert counts["big"] == "2"
    assert counts["data"] == "2"
    assert counts["the"] == "2"
