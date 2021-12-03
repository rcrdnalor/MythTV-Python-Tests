#!/bin/bash

# Define a list of test_modules
declare -a test_modules_full=( \
"test_Dataheap_Job_001" \
"test_Dataheap_Job_002" \
"test_Dataheap_Recorded_001" \
"test_Dataheap_Recorded_002" \
"test_Dataheap_Recorded_003" \
"test_Dataheap_Video_001" \
"test_Dataheap_Video_002" \
"test_Dataheap_Video_003" \
"test_Dataheap_Video_004" \
"test_Dataheap_Video_005" \
"test_Dataheap_VideoGrabber_001" \
"test_datetime_000" \
"test_datetime_001" \
"test_datetime_002" \
"test_datetime_003" \
"test_DBCache_001" \
"test_DictData_001" \
"test_DictInv_001" \
"test_enum_001" \
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
"test_OrdDict_001" \
"test_System_001" \
"test_repr_001" \
"test_singleton_001" \
)

# Define a list of test_modules for mysql access
declare -a test_modules_minimal=( \
"test_DBCache_001" \
"test_Dataheap_Job_002" \
"test_Dataheap_Recorded_001" \
"test_Dataheap_Recorded_002" \
"test_Dataheap_Recorded_003" \
"test_Dataheap_Video_003" \
"test_Dataheap_Video_004" \
"test_Dataheap_Video_005" \
"test_Methodheap_MythBE_001" \
"test_Methodheap_MythDB_001" \
)

usage()
{
    echo "usage: run_all_tests_separated.sh  [[--minimal]] | [-h]]"
}

is_python2() {
    python << EOF
import sys
if sys.version_info[0] == 2:
    sys.exit(0)
else:
    sys.exit(1)
EOF
}

minimal=0

while [ "$1" != "" ]; do
    case $1 in
        -m | --minimal )    minimal=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done


if [ "$minimal" = "1" ]; then
    test_modules=${test_modules_minimal[@]}
else
    test_modules=${test_modules_full[@]}
fi


if is_python2; then
    TPYTHONCOVERAGE="python-coverage"
else
    TPYTHONCOVERAGE="python3-coverage"
fi

echo "Using ${TPYTHONCOVERAGE}."
echo
echo "Using the following tests:"
for m in ${test_modules[@]}; do
    echo test.$m
done

# exit 1

# erase last coverage
${TPYTHONCOVERAGE} erase

# run coverage on all defined modules and add results
for m in ${test_modules[@]}; do
    ${TPYTHONCOVERAGE} run -a -m unittest -v test.$m
done

${TPYTHONCOVERAGE} report

${TPYTHONCOVERAGE} html
