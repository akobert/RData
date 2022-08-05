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

from drawRData import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./RData_GJets_background_20.root"
	ifile2 = "./RData_QCD_background_20.root"
	ifile3 = "./RData_TTBar_background_20.root"
	name = "Background_20"
	RData = drawRData(name, ifile1, ifile2, ifile3)
	print("Background Drawing Finished")
