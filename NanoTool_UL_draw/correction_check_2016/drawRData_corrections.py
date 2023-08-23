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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M10_UL_nano_10_2016_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M20_UL_nano_10_2016_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M25_UL_nano_10_2016_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M50_UL_nano_10_2016_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M75_UL_nano_10_2016_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M100_UL_nano_10_2016_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_10_2016_merged.root"
	ifile8 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/M150_UL_nano_10_2016_merged.root"
	name = "2016 Correction Comparison"
	ofile = "correction_comp_2016.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, ofile)
	print("Correction Comparison Drawing Finished")
