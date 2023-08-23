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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/Xqq_Test/ZGamma_UL_nano_2016_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/Xqq_Test/GJ_UL_2016.root"
	name = "ZGamma"
	t = 91.188 #true value
	ofile = "ZGamma_Xqq.root"
	low = 75
	high = 105
	RData = drawRData(name, ifile1, bfile1, t, ofile, low, high)
	print("ZGamma Drawing Finished")
