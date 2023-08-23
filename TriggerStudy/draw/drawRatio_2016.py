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

from drawRData_Ratio_2016 import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "../RData_Trigger_Data_2016.root"
	ifile2 = "../RData_Trigger_GJ_2016.root"
	name = "trig_ratio_2016"
	tag = ""
	RData = drawRData(name, ifile1, ifile2, tag)
	print("2016 Ratio Trigger Drawing Finished")
