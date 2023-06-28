# Performance comparison for key-value stores

Currently only measuring Python standard library's `shelve` module.

```log
INFO     | __main__:main:16 - Benchmarking for 1,000,000 iterations
DEBUG    | __main__:benchmark_shelve:33 - Initializing shelve
DEBUG    | __main__:benchmark_shelve:38 - Benchmarking shelve READS with writeback=False
DEBUG    | __main__:benchmark_shelve:41 - 	Run 1/2
INFO     | __main__:log_time_delta:23 - 	1.0757 s
DEBUG    | __main__:benchmark_shelve:41 - 	Run 2/2
INFO     | __main__:log_time_delta:23 - 	1.0742 s
DEBUG    | __main__:benchmark_shelve:47 - Benchmarking shelve READS with writeback=True
DEBUG    | __main__:benchmark_shelve:50 - 	Run 1/2
INFO     | __main__:log_time_delta:23 - 	1.3253 s
DEBUG    | __main__:benchmark_shelve:50 - 	Run 2/2
INFO     | __main__:log_time_delta:23 - 	0.1630 s
DEBUG    | __main__:benchmark_shelve:56 - Benchmarking shelve WRITES with writeback=False
DEBUG    | __main__:benchmark_shelve:59 - 	Run 1/2
INFO     | __main__:log_time_delta:23 - 	5.6554 s
DEBUG    | __main__:benchmark_shelve:59 - 	Run 2/2
INFO     | __main__:log_time_delta:23 - 	2.0140 s
DEBUG    | __main__:benchmark_shelve:65 - Benchmarking shelve WRITES with writeback=True
DEBUG    | __main__:benchmark_shelve:68 - 	Run 1/2
INFO     | __main__:log_time_delta:23 - 	2.3394 s
DEBUG    | __main__:benchmark_shelve:68 - 	Run 2/2
INFO     | __main__:log_time_delta:23 - 	2.2951 s
```
