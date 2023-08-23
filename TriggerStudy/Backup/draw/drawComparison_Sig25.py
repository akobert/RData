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

from drawRData_Comparison import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./RData_Trigger_Signal.root"
	ifile2 = "./RData_Trigger_Signal_mva.root"
	ifile3 = "./RData_Trigger_Signal_mva2.root"
	ifile4 = "./RData_Trigger_Signal_mva3.root"
	name = "comp_Signal"
	tag = "(25 GeV Signal)"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, tag)
	print("Comparison Drawing Finished")
