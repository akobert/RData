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

from drawRData_comp import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/MC_2017_2018_comp/GJ_UL_2017_10.root"
	ifile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/MC_2017_2018_comp/GJ_UL_2018_10.root"
	name = "MC_2017_2018_comp"
	RData = drawRData(name, ifile1, ifile2)
	print("MC 2017/2018 comparison Drawing Finished")
