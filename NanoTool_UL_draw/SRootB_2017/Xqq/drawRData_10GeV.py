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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Xqq_Test/M10_UL_nano_2017_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Xqq_Test/GJ_UL_2017.root"
	name = "10GeV"
	t = 10 #true value
	ofile = "M10_Xqq.root"
	low = 5
	high = 15
	RData = drawRData(name, ifile1, bfile1, t, ofile, low, high)
	print("10GeV Drawing Finished")
