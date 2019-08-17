# MythTV-Python-Tests
Test Python Bindings of https://www.mythtv.org/
# MythTV-Python-Tests
Test Python Bindings of https://www.mythtv.org/


## Preconditions:


Check out python3 branch from
https://github.com/rcrdnalor/mythtv

Add files from this repo to the mythtv folder like this:

```
./mythtv/bindings/python/
├── .testenv_example
├── .coveragerc
├── delete_pycs.sh
├── empy_pytmdb3_cache.sh
├── readme
├── run_all_tests_combined.py
├── run_all_tests_separated.sh
├── MythTV
│   ├── altdict.py
│   ├── connections.py
│   ├── _conn_mysqldb.py
│   ├── _conn_oursql.py
│   ├── database.py
│   ├── dataheap.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── logging.py
│   ├── methodheap.py
│   ├── msearch.py
│   ├── mythproto.py
│   ├── static.py
│   ├── system.py
│   ├── ttvdb
│   ├── utility
│   │   ├── altdict.py
│   │   ├── dequebuffer.py
│   │   ├── dicttoxml.py
│   │   ├── dt.py
│   │   ├── enum.py
│   │   ├── __init__.py
│   │   ├── mixin.py
│   │   ├── other.py
│   │   └── singleton.py
│   └── wikiscripts
│       ├── __init__.py
│       └── wikiscripts.py
├── scripts
│   ├── mythpython
│   └── mythwikiscripts
├── setup.py
├── test
│   ├── helpers.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── test_Dataheap_Job_001.py
│   ├── test_Dataheap_Job_002.py
│   ├── test_Dataheap_Recorded_001.py
│   ├── test_Dataheap_Video_001.py
│   ├── test_Dataheap_Video_002.py
│   ├── test_Dataheap_Video_003.py
│   ├── test_Dataheap_VideoGrabber_001.py
│   ├── test_datetime_001.py
│   ├── test_datetime_002.py
│   ├── test_DictData_001.py
│   ├── test_Logging_001.py
│   ├── test_Logging_002.py
│   ├── test_Logging_003.py
│   ├── test_Logging_004.py
│   ├── test_Logging_005.py
│   ├── test_Logging_006.py
│   ├── test_Methodheap_BEEventMonitor_001.py
│   ├── test_Methodheap_Frontend_001.py
│   ├── test_Methodheap_MythBE_001.py
│   ├── test_Methodheap_MythDB_001.py
│   ├── test_Methodheap_MythSystemEvent_001.py
│   ├── test_Methodheap_MythXML_001.py
│   ├── test_Methodheap_MythXML_002.py
│   ├── test_MSearch_001.py
│   ├── test_MSearch_002.py
│   ├── test_Mythproto_001.py
│   └── test_System_001.py
└── tmdb3
    ├── LICENSE
    ├── README
    ├── scripts
    │   ├── populate_locale.py
    │   └── pytmdb3.py
    ├── setup.py
    └── tmdb3
        ├── cache_engine.py
        ├── cache_file.py
        ├── cache_null.py
        ├── cache.py
        ├── __init__.py
        ├── locales.py
        ├── pager.py
        ├── request.py
        ├── tmdb_api.py
        ├── tmdb_auth.py
        ├── tmdb_exceptions.py
        └── util.py
```

Create an '.testenv' file as described in the file '.testenv_example'.


## Ubuntu Python2:


Install coverage for python:
```
$ sudo apt-get install python-coverage
```

This installes
```
/usr/bin/python2-coverage
```

Create an '.testenv' file as described in the file '.testenv_example'.

Check if python2 is the default:
```
$ env python --version
$ python -- version
```

Change to the python folder:
```
$ cd mythtv/bindings/python/
```

Run a single test without coverage:
```
$ python -m unittest -v test.test_System_001
```

Run a single test with coverage:
```
$ python-coverage erase
$ python-coverage run -m unittest -v test.test_System_001
$ python-coverage report
$ python-coverage html
```

Run a combined test without coverage:
```
$ python run_all_tests_combined.py
```
This reports "(testruns, failures, errors)"

Run a combined test with coverage:
```
$ python-coverage erase
$ python-coverage run --parallel-mode --concurrency=multiprocessing run_all_tests_combined.py
$ python-coverage combine
$ python-coverage report
$ python-coverage html
```

Run all tests seperately, with coverage:
```
./run_all_tests_separated.sh
```

Note: coverage of modules using pythons 'thread' or '_thread' module does not work according
https://coverage.readthedocs.io/en/coverage-4.2/trouble.html


## Ubuntu Python3:


Make python3 the default when called via `python` or `#!/usr/bin/env python`:
Put a symlink from python3 to python on top of the `PATH` environment:
As root, type
```
# mkdir -p /opt/python3
# ln -s `which python3` /opt/python3/python
```

Then in the terminal add the path as first entry:
```
$ export PATH=/opt/python3/:$PATH
```

test with:
```
$ env python --version
```

Install Ubuntu python3 packages (Bionic):
```
python3-lxml           (4.2.1-1ubuntu0.1)
python3-mysqldb        (1.3.10-1build1)   ( https://pypi.org/project/mysqlclient/ )
python3-urllib3        (1.22-1ubuntu0.18.04.1)
python3-requests       (2.18.4-2ubuntu0.1)
python3-requests-cache (0.4.13-1)
python3-pycurl         (7.43.0.1-0.2)
python3-oauth          (1.0.1-5)
python3-future         (0.15.2-4ubuntu2)
python-urlgrabber      (3.10.2-1)
```

Install for coverage measurement:
```
$ sudo apt-get install python3-coverage
```

Caution:
There is a bug in python-urllib3 1.24, which is incompatible to python-requests and python-requests-cache:
See
```
https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=913205
https://github.com/urllib3/urllib3/issues/1456
https://forum.mythtv.org/viewtopic.php?f=36&t=3274
```
Solution: Downgrade python-urllib3 to version 1.22


Don't forget to delete all byte code files of python (*.pyc) before running any test with python2 and python3:
Run
```
$ find . -name "*.pyc" -type f -delete
or
$ ./delete_pycs.sh
```

Run the tests as described in previous section.
