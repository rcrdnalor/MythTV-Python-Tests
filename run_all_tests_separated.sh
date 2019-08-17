#!/bin/bash

# Defime a list of test_modules
declare -a test_modules=( \
"test_Dataheap_Job_001" \
"test_Dataheap_Job_002" \
"test_Dataheap_Recorded_001" \
"test_Dataheap_Video_001" \
"test_Dataheap_Video_002" \
"test_Dataheap_Video_003" \
"test_Dataheap_VideoGrabber_001" \
"test_datetime_001" \
"test_datetime_002" \
"test_DictData_001" \
"test_Logging_001" \
"test_Logging_002" \
"test_Logging_003" \
"test_Logging_004" \
"test_Logging_005" \
"test_Logging_006" \
"test_Methodheap_BEEventMonitor_001" \
"test_Methodheap_Frontend_001" \
"test_Methodheap_MythBE_001" \
"test_Methodheap_MythDB_001" \
"test_Methodheap_MythSystemEvent_001" \
"test_Methodheap_MythXML_001" \
"test_Methodheap_MythXML_002" \
"test_MSearch_001" \
"test_MSearch_002" \
"test_Mythproto_001" \
"test_System_001" \
)


# erase last coverage
python2-coverage erase

# run coverage on all defined modules and add results
for m in ${test_modules[@]}; do
    python2-coverage run -a -m unittest -v test.$m
done

python2-coverage report

python2-coverage html
