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
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/RData_75GeV_20.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/corrected/RData_75GeV_20_corr.root"
	ifile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/RData_75GeV_20_nano.root"
	ifile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_75GeV_20_nano_corr.root"
	name = "75GeV"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4)
	print("75GeV Drawing Finished")
