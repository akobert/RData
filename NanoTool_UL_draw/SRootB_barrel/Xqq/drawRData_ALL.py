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

from drawRData_all import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./M10_Xqq.root"
	ifile2 = "./M25_Xqq.root"
	ifile3 = "./M50_Xqq.root"
	ifile4 = "./M75_Xqq.root"
	ifile5 = "./WGamma_Xqq.root"
	ifile6 = "./ZGamma_Xqq.root"
	name = "All"
	ofile = "SRootB_Xqq.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ofile)
	print("SRB Xqq Drawing Finished")
