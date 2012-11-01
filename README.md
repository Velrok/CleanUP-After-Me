# CleanUP-After-Me


This little helper watches a directory and will cleanup (read delete) files if space gets scarse.

## requirements

- python 2.7
- pip
- python packages
  - sh

## install
Checkout the repo.

Install all the python dependencies by running: 
```
./installDependencies.sh
```
Located in the project folder.


## usage

```
usage: cleanup.py [-h] -w WARN_LVL -c CRITICAL_LVL [-m MIN_FILE_SIZE]
                  [-p POLLING_INTERVAL]
                  watch_dir

Removes files of disk space gets scares.

positional arguments:
  watch_dir             Directory to operate on.

optional arguments:
  -h, --help            show this help message and exit
  -w WARN_LVL, --warn-lvl WARN_LVL
                        Start warning if free spaces gets less than this (in
                        MB).
  -c CRITICAL_LVL, --critical-lvl CRITICAL_LVL
                        Start deleting files if free space is below CRITICAL-
                        LVL MB until, WARN-LVL MB are free again.
  -m MIN_FILE_SIZE, --min-file-size MIN_FILE_SIZE
                        Minimun file size in MB. Files smaller will be
                        ignored.
  -p POLLING_INTERVAL, --polling-interval POLLING_INTERVAL
                        Checking / deleting interval: <number>(s|m|h|d)
```


# License

**MIT**, aka do what you want.  
Giving credit whould be greatly appreciated thou ;) .