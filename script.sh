#!/bin/bash

trap "echo; echo 'script end'; exit" SIGINT
echo "if want end ,Ctrl + C"

module load GCCcore/11.2.0 GCC/11.2.0 Python/3.9.6

while true
do
    python manage.py crontab run 6da2da0ecaf88b312e144325c8c7f4ba
    echo run contab
    sleep 1m
done