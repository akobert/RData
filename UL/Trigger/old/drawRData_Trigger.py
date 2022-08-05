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

		self.notrig = self.f.Get("h4_notrig")
		self.T110 = self.f.Get("h4_110")
		self.T200 = self.f.Get("h4_200")
		self.TOR = self.f.Get("h4_OR")
		
		ROOT.gInterpreter.Declare("Double_t widebins[26] = {0, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")


		self.eff110 = TH1F("eff110", "Photon Trigger Efficiency "+tag, 25, widebins)
		self.eff200 = TH1F("eff200", "Photon Trigger Efficiency "+tag, 25, widebins)
		self.effOR = TH1F("effOR", "Photon Trigger Efficiency "+tag, 25, widebins)

		for i in range(1, self.T110.GetNbinsX()+1):
			if self.T110.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.eff110.SetBinContent(i, self.T110.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.eff110.SetBinError(i, error(self.T110.GetBinContent(i), self.notrig.GetBinContent(i)))
			
			if self.T200.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.eff200.SetBinContent(i, self.T200.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.eff200.SetBinError(i, error(self.T200.GetBinContent(i), self.notrig.GetBinContent(i)))
				
			if self.TOR.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.effOR.SetBinContent(i, self.TOR.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.effOR.SetBinError(i, error(self.TOR.GetBinContent(i), self.notrig.GetBinContent(i)))
			

			
			
		
		
		self.eff200.SetLineColor(kRed)
		self.effOR.SetLineColor(kViolet)
	
		self.eff110.SetAxisRange(0,1.2, "Y")	
		self.eff200.SetAxisRange(0,1.2, "Y")	
		self.effOR.SetAxisRange(0,1.2, "Y")	

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.eff110.SetXTitle("Photon pT")
		self.eff110.Draw("histe")
		self.eff200.Draw("same histe")
		self.effOR.Draw("same histe")
		l1 = TLegend(.6, .25, .9, .4)
		l1.AddEntry(self.eff110, "Photon110")
                l1.AddEntry(self.eff200, "Photon200")
                l1.AddEntry(self.effOR, "OR")
                l1.Draw()
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		c1.SaveAs("./"+name+".root")
		c1.Close()

		self.notrig.SetLineColor(kGreen)
		self.T110.SetLineColor(kBlue)
		self.T200.SetLineColor(kRed)
		self.TOR.SetLineColor(kViolet)

		c2 = TCanvas()
		c2.cd()
		self.notrig.SetTitle("Photon pT "+tag)
		self.notrig.SetXTitle("Photon pT")
		self.notrig.Draw("histe")
		self.T110.Draw("same histe")
		self.T200.Draw("same histe")
		self.TOR.Draw("same histe")
		l2 = TLegend(.6, .75, .9, .9)
		l2.AddEntry(self.T110, "Photon110")
                l2.AddEntry(self.T200, "Photon200")
                l2.AddEntry(self.TOR, "OR")
                l2.AddEntry(self.notrig, "No Trigger")
                l2.Draw()
		gPad.SetLogy()
		c2.SaveAs("./photon_pt_"+name+".png")
		c2.SaveAs("./photon_pt_"+name+".root")
		c2.Close()

