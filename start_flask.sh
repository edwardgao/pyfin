#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$PYTHONPATH:$DIR

export FLASK_APP=${DIR}/site/index.py
LC_ALL=zh_CN.UTF-8 flask run
