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

from drawRData_Sig_Accept import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")

	Mass = np.array([10, 20, 25, 50, 75, 100, 125, 150], dtype="int")
	All = np.array([2461.0, 2701.0, 2846.0, 3185.0, 3180.0, 2587.0, 2250.0, 2383.0], dtype="float") #Events After Selection
	Pass = np.array([318.0, 437.0, 522.0, 693.0, 848.0, 576.0, 400.0, 393.0], dtype="float") #Passing N2DDT Events
	Fail = np.array([2143.0, 2264.0, 2324.0, 2492.0, 2332.0, 2011.0, 1850.0, 1990.0], dtype="float") #Failing N2DDT Events
	Total = np.array([254454.0, 245574.0, 251926.0, 251364.0, 250935.0, 253395.0, 242353.0, 256233.0], dtype="float") #Total Events Generated

	Filter = np.array([0.9493, 0.9469, 0.9369, 0.9423, 0.9487, 0.9498, 0.954, 0.9646]) #Filter Efficiency of Signal MC Generation

	print(Total)

	for i in range(0, Total.size):
		Total[i] = Total[i]/Filter[i]
	
	print(Total)

	name = "Sig_Accept"
	tag = "(2016)"
	RData = drawRData(name, Mass, All, Pass, Fail, Total, tag)
	print("Signal Acceptance Drawing Finished")
