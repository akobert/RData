import ROOT
from ROOT import *
import os
from array import array
import math
from math import *
import sys
import glob
import csv
import ctypes
from ctypes import *
import XRootD
from pyxrootd import client
import numpy as np

from drawRData import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/M10_UL_nano_10_2017_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/M25_UL_nano_10_2017_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/M50_UL_nano_10_2017_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/M75_UL_nano_10_2017_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/WGamma_UL_nano_10_2017_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/ZGamma_UL_nano_10_2017_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/GJ_UL_10_2017.root"
	ifile8 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/TTBar_UL_nano_10_2017_merged.root"
	ifile9 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/Data_UL_10_2017.root"
	ifile10 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel_test/QCD_UL_10_2017.root"
	name = "btag_10_2017_test"
	ofile = "btag_10_2017_test_plots.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, ifile9, ifile10, ofile)
	print("Kinematic Drawing Finished")
