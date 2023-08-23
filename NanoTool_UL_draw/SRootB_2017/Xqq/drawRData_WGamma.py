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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Xqq_Test/WGamma_UL_nano_2017_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Xqq_Test/GJ_UL_2017.root"
	name = "WGamma"
	t = 80.379 #true value
	ofile = "WGamma_Xqq.root"
	low = 65
	high = 95
	RData = drawRData(name, ifile1, bfile1, t, ofile, low, high)
	print("WGamma Drawing Finished")
