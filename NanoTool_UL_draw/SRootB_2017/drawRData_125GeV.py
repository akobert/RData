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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_5_2017_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_10_2017_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_15_2017_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_20_2017_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_25_2017_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_30_2017_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/M125_UL_nano_50_2017_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_5_2017.root"
	bfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_10_2017.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_15_2017.root"
	bfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_20_2017.root"
	bfile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_25_2017.root"
	bfile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_30_2017.root"
	bfile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/GJ_UL_50_2017.root"
	name = "125GeV"
	t = 125 #true value
	ofile = "M125_percentage_barrel.root"
	low = 100
	high = 150
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, bfile1, bfile2, bfile3, bfile4, bfile5, bfile6, bfile7, t, ofile, low, high)
	print("125GeV Drawing Finished")
