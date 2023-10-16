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

from drawRData_Fit import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Wpeak/Data_UL_10_2017.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Wpeak/TTBar_UL_nano_10_2017_merged.root"
	name = "wpeak_10_2017"
	ofile = "wpeak_10_2017_plots.root"
	RData = drawRData_Fit(name, ifile1, ifile2, ofile)
	print("Wpeak Fit Drawing Finished")
