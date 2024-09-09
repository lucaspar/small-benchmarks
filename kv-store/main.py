"""Benchmarks different key-value store approaches."""

import shelve
import time
from pathlib import Path

import loguru

log = loguru.logger


def main() -> None:
    """Benchmarking main function."""
    num_iter = 1_000_000
    dir_path = Path("data")
    dir_path.mkdir(parents=True, exist_ok=True)
    log.info(f"Benchmarking for {num_iter:,} iterations")
    benchmark_shelve(num_iter=num_iter, dir_path=dir_path)


def log_time_delta(tic: float) -> None:
    """Logs time delta."""
    log.info(f"\t{time.time() - tic:.4f} s")


def benchmark_shelve(num_iter: int, dir_path: Path = Path("data")) -> None:
    """Benchmarks shelve key-value store."""
    db_name = dir_path / "shelve"
    num_outer_loops = 2

    log.debug("Initializing shelve")
    with shelve.open(db_name, flag="c") as sdb:
        for i in range(num_iter):
            sdb[f"{i}"] = "{i*2}"

    log.debug("Benchmarking shelve READS with writeback=False")
    with shelve.open(db_name, writeback=False, flag="r") as sdb:
        for run in range(num_outer_loops):
            log.debug(f"\tRun {run+1}/{num_outer_loops}")
            start = time.time()
            for i in range(num_iter):
                _ = sdb[f"{i}"]
            log_time_delta(start)

    log.debug("Benchmarking shelve READS with writeback=True")
    with shelve.open(db_name, writeback=True, flag="w") as sdb:
        for run in range(num_outer_loops):
            log.debug(f"\tRun {run+1}/{num_outer_loops}")
            start = time.time()
            for i in range(num_iter):
                _ = sdb[f"{i}"]
            log_time_delta(start)

    log.debug("Benchmarking shelve WRITES with writeback=False")
    with shelve.open(db_name, writeback=False, flag="w") as sdb:
        for run in range(num_outer_loops):
            log.debug(f"\tRun {run+1}/{num_outer_loops}")
            start = time.time()
            for i in range(num_iter):
                sdb[f"{i}"] = f"{i*2}"
            log_time_delta(start)

    log.debug("Benchmarking shelve WRITES with writeback=True")
    with shelve.open(db_name, writeback=True, flag="w") as sdb:
        for run in range(num_outer_loops):
            log.debug(f"\tRun {run+1}/{num_outer_loops}")
            start = time.time()
            for i in range(num_iter):
                sdb[f"{i}"] = f"{i*2}"
            log_time_delta(start)


if __name__ == "__main__":
    main()
