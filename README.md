# MythTV-Python-Tests
Test Python Bindings of https://www.mythtv.org/

## Test Setup

The tests itself run on a PC (PC1) from terminal:

    - needed software: python2 and python3, dependencies for MythtTV Python Bindings
    - valid MythTV's config.xml for the user running the tests

The tests need a separate MythTV backend running on PC2 with all tuners available.

Some tests need a MythTV frontend running on PC3 with enabled Network Remote Control Port on 6546.

All PCs can be virtual machines as well connected via separate IP addresses.

```
                     
      +------------+                  +------------+
      |   PC2      |                  |   PC3      |
      |  MythtV    |                  |  MythtV    |
      |  Backend   |------------------|  Frontend  |
      |  Server    |                  |  +Display  |
      +------------+                  +------------+
                  \                    /
                   \                  /
                    \                / 
                     \              /
                      \            /
                      +------------+  
                      |   PC1      |
                      | Terminal   |
                      | Python     |
                      | config.xml |
                      +------------+
```



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

Set the pythonpath to the folder holding the bindings "MythTV":
Example:
```
$ export PYTHONPATH=`pwd`
```

Create a symlinks for tmdb3 and other metadata grabber 
```
$ cd MythTV
$ ln -s ../tmdb3/tmdb3 tmdb3
$ ln -s ../tvmaze
$ ln -s ../ttvdbv4
```

Create symlink for the metadata grabber scripts:

Note: This is needed for testing the 'tmdb3' api together with the 'MythTV' bindings. 
```
$ mkdir -p $PYTHONPATH/share/mythtv
$ ln -s $PYTHONPATH/../../programs/scripts/metadata $PYTHONPATH/share/mythtv/
```

Clear the tmdb3 cache and python '*.pyc' files:
```
$ ./empy_pytmdb3_cache.sh
$ ./delete_pycs.sh
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
$ export PYTHONPATH=`pwd`
$ ./empy_pytmdb3_cache.sh
$ ./delete_pycs.sh
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

Run the tests as described in previous section, but with python3:

Run a combined test with python3-coverage:
```
$ export PYTHONPATH=`pwd`
$ ./empy_pytmdb3_cache.sh
$ ./delete_pycs.sh
$ python3-coverage erase
$ python3-coverage run --parallel-mode --concurrency=multiprocessing run_all_tests_combined.py
$ python3-coverage combine
$ python3-coverage report
$ python3-coverage html
```

### Install python 3.8 and create virtual environment

See
```
https://askubuntu.com/questions/1197683/how-do-i-install-python-3-8-in-lubuntu-18-04
```
```
$ sudo apt-get install python3.8 python3.8-dev python3.8-venv
```

Create virtual environment:
```
$ mkdir dev3.8
$ python3.8 -m venv dev3.8/
```

Activate virtual environment, upgrade pip:
```
$ source ./dev3.8/bin/activate
(dev3.8) $ python --version
Python 3.8.3
(dev3.8) $ python3 --version
Python 3.8.3

(dev3.8) $ which pip3
... /dev3.8/bin/pip3

Upgrade pip:
(dev3.8) $ pip3 install --upgrade pip
```


Ubuntu 20.04:
Installed python modules:

* lxml 4.5.0
* MySQLdb 1.4.4
* requests 2.22.0
* requests_cache 0.4.13
* future 0.18.2


Install these modules in the virtual environment:
```
(dev3.8) $ pip3 install lxml==4.5.0
(dev3.8) $ pip3 install mysqlclient==1.4.4
(dev3.8) $ pip3 install requests==2.22.0
(dev3.8) $ pip3 install requests-cache==0.4.13
(dev3.8) $ pip3 install future==0.18.2
```

Test it:
```
(dev3.8) $ python3
Python 3.8.3 (default, May 14 2020, 20:11:43) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import lxml
>>> lxml.__version__
'4.5.0'

>>> import MySQLdb
>>> MySQLdb.__version__
'1.4.4'

>>> import requests
>>> requests.__version__
'2.22.0'

>>> import requests_cache
>>> requests_cache.__version__
'0.4.13'

>>> import future
>>> future.__version__
'0.18.2'
>>> 
```

Revise installed modules
```
(dev3.8) $ ls -la ./dev3.8/lib/python3.8/site-packages/
```

Additional notes:
testing needs python package 'coverage' : coverage 4.5.2  (as of Ubuntu 20.04)
```
(dev3.8) $ pip3 install coverage==4.5.2
```

Create a 'MYTHCONFDIR' from the MythTV version under test:
```
$ mkdir mythconfdir3.8
```
Copy the config.xml of the master backend to this folder
Export the 'MYTHCONFDIR':
```
(dev3.8) $ export MYTHCONFDIR=`pwd`/mythconfdir3.8
```

