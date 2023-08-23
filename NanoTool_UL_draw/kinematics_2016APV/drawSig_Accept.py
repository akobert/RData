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
	All = np.array([2483.0, 2812.0, 2891.0, 3305.0, 3106.0, 2617.0, 2260.0, 2315.0], dtype="float") #Events After Selection
	Pass = np.array([311.0, 422.0, 497.0, 687.0, 786.0, 521.0, 375.0, 357.0], dtype="float") #Passing N2DDT Events
	Fail = np.array([2172.0, 2390.0, 2394.0, 2618.0, 2320.0, 2096.0, 1885.0, 1958.0], dtype="float") #Failing N2DDT Events
	Total = np.array([257744.0, 251258.0, 254158.0, 254679.0, 247171.0, 247060.0, 250341.0, 247184.0], dtype="float") #Total Events Generated

	Filter = np.array([0.9493, 0.9469, 0.9369, 0.9423, 0.9487, 0.9498, 0.954, 0.9646]) #Filter Efficiency of Signal MC Generation

	print(Total)

	for i in range(0, Total.size):
		Total[i] = Total[i]/Filter[i]
	
	print(Total)

	name = "Sig_Accept"
	tag = "(2016APV)"
	RData = drawRData(name, Mass, All, Pass, Fail, Total, tag)
	print("Signal Acceptance Drawing Finished")
