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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/Xqq_Test/M75_UL_nano_2016_merged.root"
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/Xqq_Test/GJ_UL_2016.root"
	name = "75GeV"
	t = 75 #true value
	ofile = "M75_Xqq.root"
	low = 60
	high = 90
	RData = drawRData(name, ifile1, bfile1, t, ofile, low, high)
	print("75GeV Drawing Finished")
