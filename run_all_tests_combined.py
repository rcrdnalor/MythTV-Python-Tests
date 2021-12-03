# -*- coding: utf-8 -*-

#import unittest ### XXX do not import this here!
import importlib

import multiprocessing as mp

test_modules =  [
                  "test_Dataheap_Job_001"
                , "test_Dataheap_Job_002"
                , "test_Dataheap_Recorded_001"
                , "test_Dataheap_Recorded_002"
                , "test_Dataheap_Video_001"
                , "test_Dataheap_Video_002"
                , "test_Dataheap_Video_003"
                , "test_Dataheap_Video_004"
                , "test_Dataheap_Video_005"
                , "test_Dataheap_VideoGrabber_001"
                , "test_datetime_000"
                , "test_datetime_001"
                , "test_datetime_002"
                , "test_datetime_003"
                , "test_DBCache_001"
                , "test_DictData_001"
                , "test_DictInv_001"
                , "test_enum_001"
                , "test_Logging_001"
                , "test_Logging_002"
                , "test_Logging_003"
                , "test_Logging_004"
                , "test_Logging_005"
                , "test_Logging_006"
                , "test_Methodheap_BEEventMonitor_001"
                , "test_Methodheap_Frontend_001"
                , "test_Methodheap_MythBE_001"
                , "test_Methodheap_MythDB_001"
                , "test_Methodheap_MythSystemEvent_001"
                , "test_Methodheap_MythXML_001"
                , "test_Methodheap_MythXML_002"
                , "test_MSearch_001"
                , "test_MSearch_002"
                , "test_Mythproto_001"
                , "test_OrdDict_001"
                , "test_System_001"
                , "test_repr_001"
                , "test_singleton_001"
                ]



def run_test_module(queue, test_module):
    """Runs a single test module from 'test folder'.
       returns 'run', 'failures', 'errors' as decimal values
    """

    import unittest
    # Import the module
    m = importlib.import_module('.'+test_module, 'test')


    # initialize the test suite
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(m))

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

#   return(result.testsRun, len(result.failures), len(result.errors))
    queue.put((result.testsRun, len(result.failures), len(result.errors)))


if __name__ == '__main__':        # pragma: no cover
    r = 0; f = 0; e = 0
    for m in test_modules:
        #mp.set_start_method('fork') ### XX this is not implemented in python 2
        q = mp.Queue()
        p = mp.Process(target=run_test_module, args=(q,m))
        p.start()
        p.join() # this blocks until the process terminates
        #print(q.get())
        rq,fq,eq = q.get()
        #print(rq, fq, eq)
        r += rq; f += fq; e += eq


    print(r, f, e)
