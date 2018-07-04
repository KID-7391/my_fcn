#!/usr/bin/env sh
set -e

export PYTHONPATH='/home/wen/caffe-master/python'

python solve.py 2>&1 | tee Log/caffe.log
