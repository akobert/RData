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
	ifile1 = "./RData_10GeV_CutBased.root"
	ifile2 = "./RData_25GeV_CutBased.root"
	ifile3 = "./RData_150GeV_CutBased.root"
	ifile4 = "./RData_50GeV_CutBased.root"
	ifile5 = "./RData_75GeV_CutBased.root"
	ifile6 = "./RData_100GeV_CutBased.root"
	bfile1 = "./RData_GJets_CutBased.root"
	name = "CutBased"
	RData = drawRData(name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, bfile1)
	print("CutBased SRB Drawing Done")
