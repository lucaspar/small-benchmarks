"""Benchmarks different key-value store approaches."""
import os
import shelve
import time

import loguru

log = loguru.logger


def main():

    num_iter = 1_000_000
    dir_path = "data"
    os.makedirs(dir_path, exist_ok=True)
    log.info("Benchmarking for {:,} iterations".format(num_iter))

    benchmark_shelve(num_iter=num_iter, dir_path=dir_path)


def log_time_delta(tic: float):
    """Logs time delta."""
    log.info("\t{:.4f} s".format(time.time() - tic))


def benchmark_shelve(num_iter: int, dir_path: str = "data"):
    """Benchmarks shelve key-value store."""

    db_name = os.path.join(dir_path, "shelve")
    num_outer_loops = 2

    # initialize
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
