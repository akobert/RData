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

from drawRData_Efficiency import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./RData_Efficiency_GJets.root"
	ifile2 = "./RData_Efficiency_Data.root"
	ifile3 = "./RData_Efficiency_Sig25.root"
	name = "efficiency"
	tag = ""
	RData = drawRData(name, ifile1, ifile2, ifile3, tag)
	print("Efficiency Drawing Finished")
