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

from drawRData_Trigger_Custom import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./RData_Trigger_Data_r9_CutBased.root"
	ifile2 = "./RData_Trigger_Data_r9_MVA1.root"
	ifile3 = "./RData_Trigger_Data_r9_MVA2.root"
	ifile4 = "./RData_Trigger_Data_r9_MVA3.root"
	name = "trigger_Data_r9"
	tag = "(Data)"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, tag)
	print("Trigger Data R9 Drawing Finished")
