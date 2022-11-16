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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/GJ_UL.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/GJ_UL.root"
	name = "GJ"
	t = -1 #true value
	ofile = "GJ_plots.root"
	RData = drawRData(name, ifile1, ifile2, t, ofile)
	print("GJ Drawing Finished")
