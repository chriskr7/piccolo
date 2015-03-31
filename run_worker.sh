#!/bin/bash
source `which virtualenvwrapper.sh`
workon piccolo
nohup python worker_main.py > /dev/null 2>&1 &
deactivate
