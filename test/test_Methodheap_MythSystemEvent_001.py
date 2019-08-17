# -*- coding: utf-8 -*-

import unittest

from MythTV import MythSystemEvent, MythBE, MythDB

import time
import subprocess
import os

from test.helpers import tailandgrep

class test_Methodheap_MythSystemEvent_001(unittest.TestCase):
    """Test MythSystemEvent calls a registered script on systemevent `KEY_01`.
       ### XXX hardcoded script registered to Key_01 system event.

       See https://www.mythtv.org/wiki/SYSTEM_EVENT_(Myth_Protocol)

       The preconditions for this test are described in the following steps:

       Step1: Setup on your local PC, which has mythfrontend installed,
       a system event like:

       "Key_01 /usr/local/bin/mythsystemeventtest.sh %SENDER%"

       Verify with mysql:

       $ mysql -h <backendIP> -u mythtv -p<password> mythconverg

       MariaDB [mythconverg]> select * from settings where value = 'EventCmdKey01';

       | EventCmdKey01 | /usr/local/bin/mythsystemeventtest.sh %SENDER% | <master_backend_ip>   |

       Step2: Setup a the script on your local PC that runs on a system event:

       Name: /usr/local/bin/mythsystemeventtest.sh

       #!/bin/bash

       me=$(/usr/bin/basename "${0}")

       log=/tmp/my_mse_logfile

       echo `date` "$me $@" >>$log

       exit 0

       Step3: You need to have access to the backend via ssh as user mythtv
       using pre-shared keys. Ask the internet how to install this.

       "ssh mythtv@<backend-ip> 'mythutil --systemevent KEY_01'"

       must work without asking for a password.

       Caution: The linux community consider the way of setup this ssh key
       for a user without password as security risk.
    """

    db = MythDB()
    master_hostname   = db.getMasterBackend()
    master_backend_ip = db.settings['NULL']['MasterServerIP']

    def test_test_Methodheap_MythSystemEvent_001_01(self):
        """Test if 'MythSystemEvent' calls a registered script for the
           system event 'KEY_01'.

        """
        mse = MythSystemEvent()

        time.sleep(1)

        # fire the system event 'KEY_01' from the backend
        cmd = "ssh mythtv@%s 'mythutil --systemevent KEY_01' >/dev/null" %(self.master_backend_ip)
        result = subprocess.call(cmd, shell=True)
        self.assertTrue(result == 0)

        time.sleep(1)

        s = tailandgrep("/tmp/my_mse_logfile", 3, "mythsystemeventtest.sh %s" %(self.master_hostname))
        self.assertTrue(len(s) > 0)


    def tearDown(self):
        if os.path.exists("/tmp/my_mse_logfile"):
            os.remove("/tmp/my_mse_logfile")


if __name__ == '__main__':
    unittest.main()
