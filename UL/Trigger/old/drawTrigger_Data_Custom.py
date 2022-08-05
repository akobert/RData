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
	ifile1 = "./RData_Trigger_Data_Custom.root"
	name = "trigger_data_custom"
	tag = "(Custom) (Data)"
	RData = drawRData(name, ifile1, tag)
	print("Trigger Data Custom Drawing Finished")
