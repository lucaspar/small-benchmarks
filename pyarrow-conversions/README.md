# Performance comparison for conversions from PyArrow array

Measuring conversions from PyArrow to: Polars Series, Pandas Series, NumPy array, and native Python list.

```log
	Memory increase: 381.85 MB
Created array with size: 50,000,000 and type double
Testing polars:
	Memory increase: 2.06 MB
	Conversion time from pyarrow to polars:	0.0004 seconds
Testing numpy:
	Memory increase: 192.0 KB
	Conversion time from pyarrow to numpy:	0.0002 seconds
Testing list:
	Memory increase: 1.87 GB
	Conversion time from pyarrow to list:	11.1212 seconds
Testing pandas:
	Memory increase: 192.0 KB
	Conversion time from pyarrow to pandas:	0.0092 seconds
```
