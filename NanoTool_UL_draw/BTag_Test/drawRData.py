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

from drawRData_BTag import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	GJ_Select = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/GJ100to200_UL_nano_Select_merged_10.root"
	GJ_Fat = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/GJ100to200_UL_nano_Fat_merged_10.root"
	GJ_PN = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/GJ100to200_UL_nano_PN_merged_10.root"
	GJ_PN_high = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/GJ100to200_UL_nano_PN_high_merged_10.root"
	WG_Select = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/WGamma_UL_nano_Select_merged_10.root"
	WG_Fat = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/WGamma_UL_nano_Fat_merged_10.root"
	WG_PN = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/WGamma_UL_nano_PN_merged_10.root"
	WG_PN_high = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/WGamma_UL_nano_PN_high_merged_10.root"
	ZG_Select = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/ZGamma_UL_nano_Select_merged_10.root"
	ZG_Fat = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/ZGamma_UL_nano_Fat_merged_10.root"
	ZG_PN = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/ZGamma_UL_nano_PN_merged_10.root"
	ZG_PN_high = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/ZGamma_UL_nano_PN_high_merged_10.root"
	M50_Select = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/M50_UL_nano_Select_merged_10.root"
	M50_Fat = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/M50_UL_nano_Fat_merged_10.root"
	M50_PN = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/M50_UL_nano_PN_merged_10.root"
	M50_PN_high = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/M50_UL_nano_PN_high_merged_10.root"
	DataC_Select = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/DataC_UL_nano_Select_merged_10.root"
	DataC_Fat = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/DataC_UL_nano_Fat_merged_10.root"
	DataC_PN = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/DataC_UL_nano_PN_merged_10.root"
	DataC_PN_high = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/BTag_Test/DataC_UL_nano_PN_high_merged_10.root"
	name = "BTag_Test"
	RData = drawRData(name, GJ_Select, GJ_Fat, GJ_PN, GJ_PN_high, WG_Select, WG_Fat, WG_PN, WG_PN_high, ZG_Select, ZG_Fat, ZG_PN, ZG_PN_high, M50_Select, M50_Fat, M50_PN, M50_PN_high, DataC_Select, DataC_Fat, DataC_PN, DataC_PN_high)
	print("BTag Test Drawing Finished")
