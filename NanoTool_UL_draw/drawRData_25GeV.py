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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M25_UL_nano_merged.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M25_UL_nano_merged.root"
	name = "25GeV"
	t = 25 #true value
	ofile = "M25_plots.root"
	RData = drawRData(name, ifile1, ifile2, t, ofile)
	print("25GeV Drawing Finished")
