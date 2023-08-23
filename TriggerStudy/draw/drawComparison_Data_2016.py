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

from drawRData_Comparison_2016 import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "../RData_Trigger_Data_2016.root"
	name = "comp_Data_2016"
	tag = "(2016 Data)"
	RData = drawRData(name, ifile1, tag)
	print("2016 Comparison Drawing Finished")
