#!/bin/bash

python setup_5.py
python setup_10.py
python setup_15.py
python setup_20.py
python setup_25.py
python setup_30.py
python setup_50.py

condor_submit run_5.jdl
condor_submit run_10.jdl
condor_submit run_15.jdl
condor_submit run_20.jdl
condor_submit run_25.jdl
condor_submit run_30.jdl
condor_submit run_50.jdl
