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

from drawRData_all import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./M10_percentage_barrel.root"
	ifile2 = "./M25_percentage_barrel.root"
	ifile3 = "./M50_percentage_barrel.root"
	ifile4 = "./M75_percentage_barrel.root"
	name = "All"
	ofile = "SRootB.root"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ofile)
	print("SRB Drawing Finished")
