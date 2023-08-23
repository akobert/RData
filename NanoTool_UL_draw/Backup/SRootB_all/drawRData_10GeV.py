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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_5_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_10_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_15_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_20_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_25_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_30_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/M10_UL_nano_50_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_5.root"
	bfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_10.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_15.root"
	bfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_20.root"
	bfile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_25.root"
	bfile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_30.root"
	bfile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_percentage/GJ_UL_50.root"
	
	ifile_btag1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_5_merged.root"
	ifile_btag2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_10_merged.root"
	ifile_btag3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_15_merged.root"
	ifile_btag4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag/M10_UL_nano_merged.root"
	ifile_btag5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_25_merged.root"
	ifile_btag6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_30_merged.root"
	ifile_btag7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/M10_UL_nano_50_merged.root"
	bfile_btag1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_5.root"
	bfile_btag2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_10.root"
	bfile_btag3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_15.root"
	bfile_btag4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag/GJ_UL.root"
	bfile_btag5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_25.root"
	bfile_btag6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_30.root"
	bfile_btag7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_btag_percentage/GJ_UL_50.root"

	name = "10GeV"
	t = 10 #true value
	ofile = "M10_percentage.root"
	low = 5
	high = 15
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, bfile1, bfile2, bfile3, bfile4, bfile5, bfile6, bfile7, ifile_btag1, ifile_btag2, ifile_btag3, ifile_btag4, ifile_btag5, ifile_btag6, ifile_btag7, bfile_btag1, bfile_btag2, bfile_btag3, bfile_btag4, bfile_btag5, bfile_btag6, bfile_btag7, t, ofile, low, high)
	print("10GeV Drawing Finished")
