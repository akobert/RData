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

class drawRData:
	def __init__(self, name, ifile1, ifile2, ifile3):
		gROOT.SetBatch(True)

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.Data = self.f.Get("fail_photon_pt")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.GJ = self.g.Get("fail_photon_pt")
		
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.sig25 = self.h.Get("fail_photon_pt")

		
#		self.comb1 = TH1F("comb1", "Background Softdrop Mass", 40, 0, 200)
#		self.comb1_over = TH1F("comb1_over", "Background Softdrop Mass With Overlap Removed", 40, 0, 200)
		
#		self.comb1.Add(self.GJp1)
#		self.comb1.Add(self.QCDp1)
#		self.comb1.Add(self.TTp1)
		
#		self.comb1_over.Add(self.GJp1_1)
#		self.comb1_over.Add(self.QCDp1_1)
#		self.comb1_over.Add(self.TTp1)
		
		
		self.GJ.SetLineColor(kGreen)
		self.Data.SetLineColor(kBlack)
		self.sig25.SetLineColor(kRed)
	
		self.GJ.Scale(1.0/self.GJ.Integral())	
		self.Data.Scale(1.0/self.Data.Integral())	
		self.sig25.Scale(1.0/self.sig25.Integral())	
		
		

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.GJ.SetTitle("Failing Photon pT")
		self.GJ.Draw("hist")
		self.Data.Draw("same hist")
		self.sig25.Draw("same hist")
		l1 = TLegend(.6, .75, .9, .9)
		l1.AddEntry(self.GJ, "GJets")
                l1.AddEntry(self.Data, "Data")
                l1.AddEntry(self.sig25, "25 GeV Signal")
                l1.Draw()
#		gPad.SetLogy()
		c1.SaveAs("./RData_"+name+".png")
		c1.Close()

		self.GJ.Divide(self.Data)

		c2 = TCanvas()
		c2.cd()
		self.GJ.SetTitle("Failing Photon pT GJets/Data")
		self.GJ.Draw("hist")
		c2.SaveAs("./RData_"+name+"_ratio.png")
		c2.Close()
		
		
		
