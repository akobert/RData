#!/bin/bash

cluster=$1
process=$2

# CMSSW setup etc
export SCRAM_ARCH="slc7_amd64_gcc820"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh

cd /home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/WGamma_nano/

eval `scramv1 runtime -sh`

python WGamma$2.py >& /home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/CondorFiles/logfiles_WGamma_nano_$1_$2.log
