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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_5_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_10_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_15_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag/M50_UL_nano_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_25_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_30_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M50_UL_nano_50_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_5.root"
	bfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_10.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_15.root"
	bfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag/GJ_UL.root"
	bfile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_25.root"
	bfile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_30.root"
	bfile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_50.root"
	name = "50GeV"
	t = 50 #true value
	ofile = "M50_percentage.root"
	low = 35
	high = 65
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, bfile1, bfile2, bfile3, bfile4, bfile5, bfile6, bfile7, t, ofile, low, high)
	print("50GeV Drawing Finished")
