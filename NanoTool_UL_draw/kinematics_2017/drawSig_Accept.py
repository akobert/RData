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
	All = np.array([3305.0, 3739.0, 3969.0, 4689.0, 4760.0, 3801.0, 3297.0, 3204.0], dtype="float") #Events After Selection
	Pass = np.array([428.0, 586.0, 668.0, 1047.0, 1204.0, 904.0, 624.0, 521.0], dtype="float") #Passing N2DDT Events
	Fail = np.array([2877.0, 3153.0, 3301.0, 3642.0, 3556.0, 2897.0, 2673.0, 2683.0], dtype="float") #Failing N2DDT Events
	Total = np.array([499072.0, 487317.0, 495785.0, 496133.0, 496846.0, 490390.0, 496239.0, 496687.0], dtype="float") #Total Events Generated

	Filter = np.array([0.9493, 0.9469, 0.9369, 0.9423, 0.9487, 0.9498, 0.954, 0.9646]) #Filter Efficiency of Signal MC Generation

	print(Total)

	for i in range(0, Total.size):
		Total[i] = Total[i]/Filter[i]
	
	print(Total)

	name = "Sig_Accept"
	tag = "(2017)"
	RData = drawRData(name, Mass, All, Pass, Fail, Total, tag)
	print("Signal Acceptance Drawing Finished")
