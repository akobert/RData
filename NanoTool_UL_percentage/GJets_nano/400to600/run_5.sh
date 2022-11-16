#!/bin/bash

cluster=$1
process=$2

# CMSSW setup etc
export SCRAM_ARCH="slc7_amd64_gcc820"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh

cd /home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJets_nano/400to600

eval `scramv1 runtime -sh`

python GJ400to600_$2_5.py >& /home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/CondorFiles/logfiles_GJ400to600_nano_$1_$2_5.log
