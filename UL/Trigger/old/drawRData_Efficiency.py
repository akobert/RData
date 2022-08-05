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
	def __init__(self, name, ifile1, ifile2, ifile3, tag):
		gROOT.SetBatch(True)

		#background files
		
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.GJ_mva = self.f.Get("h5_mvaID")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.Data_mva = self.g.Get("h5_mvaID")
			
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.Sig25_mva = self.h.Get("h5_mvaID")
			
		#Normalize Histograms
		self.GJ_mva.Scale(1/self.GJ_mva.Integral())
		self.Data_mva.Scale(1/self.Data_mva.Integral())
		self.Sig25_mva.Scale(1/self.Sig25_mva.Integral())
		
		self.GJ_mva.SetLineColor(kOrange)
		self.Data_mva.SetLineColor(kBlack)
		self.Sig25_mva.SetLineColor(kCyan)
	
		self.Data_mva.SetAxisRange(0,.2,"Y")

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.Data_mva.SetTitle("Normalized MVA Scores")
		self.Data_mva.SetXTitle("MVA Score")
		self.Data_mva.Draw("hist")
		self.GJ_mva.Draw("same hist")
		self.Sig25_mva.Draw("same hist")
		l1 = TLegend(.4, .75, .7, .9)
		l1.AddEntry(self.GJ_mva, "GJets")
                l1.AddEntry(self.Data_mva, "Data")
                l1.AddEntry(self.Sig25_mva, "25 GeV Signal")
                l1.Draw()
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		c1.SaveAs("./"+name+".root")
		c1.Close()

