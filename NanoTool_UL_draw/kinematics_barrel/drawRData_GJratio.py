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

from drawRData_GJpf import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage_barrel/GJ_UL_10.root"
	name = "corr_btag_10_barrel_GJratio"
	RData = drawRData(name, ifile1)
	print("GJratio (Barrel) Drawing Finished")
