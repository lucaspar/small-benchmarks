"""Benchmark the conversion of pyarrow arrays to polars, numpy, and lists."""
import time
from typing import Callable

import numpy as np
import pandas as pd
import polars as pl
import psutil
import pyarrow as pa


def get_memory_usage() -> float:
    """Returns the memory usage of the current process, in bytes."""

    process = psutil.Process()
    physical_mem = process.memory_info().rss
    # virtual_mem = process.memory_info().vms
    return physical_mem


def pretty_memory_usage(mem_bytes: float) -> str:
    """Pretty prints the memory usage in KB, MB, GB, etc."""
    unit = "B"
    for unit in ["", "K", "M", "G", "T", "P"]:
        if mem_bytes < 1_024:
            break
        mem_bytes /= 1_024
    # round to two decimal places
    mem_bytes = round(mem_bytes, 2)
    return f"{mem_bytes} {unit}B"


def measure_memory(func: Callable) -> Callable:
    """Decorator to measure the memory difference of a function."""

    def wrapper(*args, **kwargs):
        current_memory = get_memory_usage()
        res = func(*args, **kwargs)
        memory_increase = get_memory_usage() - current_memory
        # to make sure res is actually in memory
        assert res is not None and len(res) > 0, "Result is empty"
        print(f"\tMemory increase: {pretty_memory_usage(memory_increase)}")
        return res

    return wrapper


@measure_memory
def setup(arrow_size: int = 50_000_000, target_type: type = float) -> pa.Array:
    """Creates a pyarrow array of the given size."""
    if target_type == float:
        arr = pa.array(np.random.rand(arrow_size))
    elif target_type == int:
        arr = pa.array(np.random.randint(0, 100, arrow_size))
    else:
        raise ValueError(f"Unknown type: {target_type}")

    return arr


@measure_memory
def convert_to_polars(arr: pa.Array) -> pl.Series:
    """Converts the array to a polars series."""
    polar_series = pl.from_arrow(arr)
    assert len(polar_series) == len(arr), "Lengths do not match"
    assert isinstance(polar_series, pl.Series), "Not a polars series"
    return polar_series


@measure_memory
def convert_to_numpy(arr: pa.Array) -> np.ndarray:
    """Converts the array to a numpy array."""
    np_array = arr.to_numpy()
    assert len(np_array) == len(arr), "Lengths do not match"
    return np_array


@measure_memory
def convert_to_list(arr: pa.Array) -> list:
    """Converts the array to a list."""
    list_ = arr.tolist()
    assert len(list_) == len(arr), "Lengths do not match"
    return list_


@measure_memory
def convert_to_pandas(arr: pa.Array) -> pd.Series:
    """Converts the array to a pandas series."""
    pandas_series = arr.to_pandas()
    assert len(pandas_series) == len(arr), "Lengths do not match"
    return pandas_series


def benchmark(name: str, callback: Callable, kwargs: dict):
    """Runs the benchmark for the given callback."""
    print(f"Testing {name}:")
    start = time.time()
    callback(**kwargs)
    print(
        f"\tConversion time from pyarrow to {name}:\t{time.time() - start:.4f} seconds"
    )


def main():
    """Run the benchmark for each conversion."""

    arr = setup(arrow_size=50_000_000, target_type=float)
    print(f"Created array with size: {len(arr):,} and type {arr.type}")
    kwargs = {"arr": arr}

    tests = [
        dict(name="polars", callback=convert_to_polars, kwargs=kwargs),
        dict(name="numpy", callback=convert_to_numpy, kwargs=kwargs),
        dict(name="list", callback=convert_to_list, kwargs=kwargs),
        dict(name="pandas", callback=convert_to_pandas, kwargs=kwargs),
    ]

    for test in tests:
        benchmark(**test)


if __name__ == "__main__":
    main()
