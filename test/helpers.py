# -*- coding: utf-8 -*-

from collections import deque
import re, sys
import codecs

def tailandgrep(fname, maxlen, rex):
    """ This searches the last 'n' lines of a file for the given regex,
        similar to 'tail -n maxlen fname | grep regex'.
        Returns the line if rex was found
    """
    try:
        with codecs.open(fname, 'r', encoding='utf8') as f:
            d = deque(f, maxlen=maxlen)
            for line in d:
                found = re.findall(rex, line)
                if found:
                    return (line)
            return ("")
    except IOError:
        return ("")


class add_log_flags(object):
    """Add additional args to enable MythTV logging."""

    additional_args = [ '--nodblog'
                      , '--loglevel'
                      , 'debug'
                      , '--verbose'
                      , 'all'
                      , '--logfile'
                      , '/tmp/my_logfile'
                      ]
    # --nodblog --loglevel debug --verbose all --logfile /tmp/my_logfile

    def __enter__(self):
        sys.argv.extend(self.additional_args)

    def __exit__(self, typ, value, traceback):
        sys.argv = [arg for arg in sys.argv if arg not in self.additional_args]


def get_test_env(TestEnv, envfile = "./.testenv"):
    """This retrieves the test environment including all hardcoded values from a
       single file. The user needs to setup this file correctly.
    """
    with codecs.open(envfile, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            if 'export' not in line:
                 continue
            # Remove leading `export `
            # then, split name / value pair
            key, value = line.replace('export ', '', 1).strip().split('=', 1)
            # value may have quotation marks (""), remove them
            value = value.replace('"','')
            TestEnv[key] = value
