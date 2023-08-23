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
	All = np.array([26610.0, 27165.0, 27668.0, 25843.0, 21215.0, 19368.0, 20344.0, 21462.0], dtype="float") #Events After Selection
	Pass = np.array([3412.0, 4521.0, 5104.0, 5480.0, 3665.0, 2792.0, 2623.0, 2593.0], dtype="float") #Passing N2DDT Events
	Fail = np.array([23198.0, 22644.0, 22564.0, 20363.0, 17550.0, 16576.0, 17721.0, 18869.0], dtype="float") #Failing N2DDT Events
	Total = np.array([501525.0, 493822.0, 496157.0, 492039.0, 496487.0, 473228.0, 492822.0, 473228.0], dtype="float") #Total Events Generated

	Filter = np.array([0.9493, 0.9469, 0.9369, 0.9423, 0.9487, 0.9498, 0.954, 0.9646]) #Filter Efficiency of Signal MC Generation

	print(Total)

	for i in range(0, Total.size):
		Total[i] = Total[i]/Filter[i]
	
	print(Total)

	name = "Sig_Accept"
	tag = "(2018)"
	RData = drawRData(name, Mass, All, Pass, Fail, Total, tag)
	print("Signal Acceptance Drawing Finished")
