#!/bin/bash
echo "Running, usage: ./run.sh node_number setup*.txt"

if [[ $# -eq 0]] ; then
    echo "Illegal number of parameters"
    exit 1
fi

python PRM.py $1 $2&
python mapper.py 5002 5001 1&
python mapper.py 5003 5001 2&
python reducer.py 5004 5001&
python CLI.py
