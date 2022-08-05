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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/RData_TTBar_UL_20_quick.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/corrected/RData_TTBar_UL_20_quick_corr.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/NanoTool/RData_TTBar_UL_20_quick_nano.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/NanoTool/corrected/RData_TTBar_UL_20_quick_nano_corr.root"
	name = "TTBar"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4)
	print("TTBar Drawing Finished")
