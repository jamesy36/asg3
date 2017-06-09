#!/bin/bash
python PRM.py $1 setup.txt
sleep 15
port_a=$(($1+5005))
port_b=$(($1+5000))
python CLI.py $port_a $port_b
