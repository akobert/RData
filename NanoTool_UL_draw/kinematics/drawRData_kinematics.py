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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/M10_UL_nano_merged_10.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/M25_UL_nano_merged_10.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/M50_UL_nano_merged_10.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/M75_UL_nano_merged_10.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/WGamma_UL_nano_merged_10.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/ZGamma_UL_nano_merged_10.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/GJ_UL_10.root"
	ifile8 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/TTBar_UL_nano_merged_10.root"
	ifile9 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/Data_UL_10.root"
	ifile10 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/QCD_UL_10.root"
	name = "corr_btag_10"
	ofile = "corr_btag_10_plots.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, ifile9, ifile10, ofile)
	print("Kinematic Drawing Finished")
