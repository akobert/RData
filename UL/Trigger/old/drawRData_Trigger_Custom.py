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

#from future import division

def error(num, den):
#	r = num.GetBinContent(n)/den.GetBinContent(n)

#	return r*sqrt(pow(num.GetBinError(n)/num.GetBinContent(n),2) + pow(den.GetBinError(n)/den.GetBinContent(n),2))
	
	z = den - num
	error = 0
	if den != 0:
		err_num = sqrt(num) if num != 0 else 1.6
		err_z = sqrt(z) if z !=0 else 1.6
		error = sqrt((z*z*err_num*err_num) + (num*num*err_z*err_z))/(den*den)
	return error
	

class drawRData:
	def __init__(self, name, ifile1, tag):
		gROOT.SetBatch(True)

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();
		
		self.notrig = self.f.Get("photon_pt_mva_notrig")
		self.r110 = self.f.Get("photon_pt_mva_110")
		self.r200 = self.f.Get("photon_pt_mva_200")
		self.rOR = self.f.Get("photon_pt_mva_OR")

		

	#	self.eff110 = TH1F("eff110", "Photon Trigger Efficiency "+tag, 50, 0, 1000)
	#	self.eff200 = TH1F("eff200", "Photon Trigger Efficiency "+tag, 50, 0, 1000)
	#	self.effOR = TH1F("effOR", "Photon Trigger Efficiency "+tag, 50, 0, 1000)
		self.r110.Divide(self.notrig)
		self.r200.Divide(self.notrig)
		self.rOR.Divide(self.notrig)

	
		self.r110.SetAxisRange(0,1.0, "Z")	
		self.r200.SetAxisRange(0,1.0, "Z")	
		self.rOR.SetAxisRange(0,1.0, "Z")	

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.r110.Draw("COLZ")
		c1.SaveAs("./"+name+"_110.png")
		c1.SaveAs("./"+name+"_110.root")
		c1.Close()
		
		c2 = TCanvas()
		c2.cd()
		self.r200.Draw("COLZ")
		c2.SaveAs("./"+name+"_200.png")
		c2.SaveAs("./"+name+"_200.root")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.rOR.Draw("COLZ")
		c3.SaveAs("./"+name+"_OR.png")
		c3.SaveAs("./"+name+"_OR.root")
		c3.Close()

