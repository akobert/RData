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

from drawRData_xqq import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/GJ_UL_2016.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/M10_UL_nano_2016_merged.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/M25_UL_nano_2016_merged.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/M50_UL_nano_2016_merged.root"
	ifile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/M75_UL_nano_2016_merged.root"
	ifile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/WGamma_UL_nano_2016_merged.root"
	ifile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/ZGamma_UL_nano_2016_merged.root"
	name = "Xqq"
	ofile = "xqq.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ofile)
	print("Xqq Drawing Finished")
