# Pomotodo Analyzer

A time analyzer for [Pomotodo](https://pomotodo.com).

## Usage

```
> python pa.py -h
usage: pa.py [-h] [-f FILE] [-s {time,time_asc,title}] [-d]

Pomotodo time entry analyzer.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Pomotodo time entry file
  -s {time,time_asc,title}, --sort {time,time_asc,title}
                        Project sort type (default: time)
  -d, --days            Show days
```

## Example

```
> python pa.py -f data/pomos.csv

++++++++++++++ Pomotodo Analyzer +++++++++++++++

TOTAL: 4:21:30

[P2 2:08:59]
- #P2 E2 0:50:00
- #P2 E4 0:50:17
- #P2 E6 0:28:42

[P1 1:21:49]
- #P1 E1 0:25:00
- #P1 E5 0:56:49

[P3 0:50:42]
- #P3 E3 0:50:42
```
