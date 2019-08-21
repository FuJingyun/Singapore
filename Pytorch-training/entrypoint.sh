#!/bin/bash
mkdir -p "./files/snapshot"
dt=$(date '+%d-%m-%Y-%H:%M:%S');
printLog(){ ( echo "$@" && "$@" 2>&1 ) | tee ./files/snapshot/${dt}output.txt ;}

prefix=$(python3 -c "import sys, json; f = open(sys.argv[1]); print(json.load(f)['dataset_prefix']); f.close()" $1)

`sleep 15; tensorboard --logdir "./files/snapshot" --port=6015` &
echo "Using json file: '$1'"
printLog python3 -u training.py $1
