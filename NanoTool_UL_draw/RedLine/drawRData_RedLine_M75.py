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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage_barrel/M75_UL_nano_merged_10.root"
#	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/Data_UL_10.root"
	name = "M75"
	ofile = "corr_btag_10_M75_redline.root"
	RData = drawRData(name, ifile1, ofile)
	print("M75 RedLine Drawing Finished")
