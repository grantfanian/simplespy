#!/bin/bash
# I would
# source ./env.sh
nohup python util.py >> util.log 2>&1 &
nohup gunicorn -w 4 -b 0.0.0.0:3000 wsgi:app >> gunicorn.log 2>&1 &