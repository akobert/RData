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

from drawRData_photon import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./RData_Data_UL.root"
	ifile2 = "./RData_GJets_UL_20.root"
	ifile3 = "../signalMC/RData_25GeV_20.root"
	name = "photon"
	RData = drawRData(name, ifile1, ifile2, ifile3)
	print("photon Drawing Finished")
