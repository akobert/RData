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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/Xqq_Test_2018/WGamma_UL_nano_2018_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/Xqq_Test_2018/GJ_UL_2018.root"
	name = "WGamma"
	t = 80.379 #true value
	ofile = "WGamma_Xqq.root"
	low = 65
	high = 95
	RData = drawRData(name, ifile1, bfile1, t, ofile, low, high)
	print("WGamma Drawing Finished")
