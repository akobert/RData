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
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, tag):
		gROOT.SetBatch(True)

		#background files
		
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.OR_cut = self.f.Get("photon_pt_OR")
		self.notrig_cut = self.f.Get("photon_pt_notrig")

		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();
		
		self.OR_mva = self.g.Get("photon_pt_OR")
		self.notrig_mva = self.g.Get("photon_pt_notrig")

			
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();
		
		self.OR_mva2 = self.h.Get("photon_pt_OR")
		self.notrig_mva2 = self.h.Get("photon_pt_notrig")
		
		self.j = TFile.Open(ifile4, "READ")
		self.j.ls();
		
		self.OR_mva3 = self.j.Get("photon_pt_OR")
		self.notrig_mva3 = self.j.Get("photon_pt_notrig")

		ROOT.gInterpreter.Declare("Double_t widebins[26] = {0, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")


                self.effOR_cut = TH1F("effOR_cut", "Photon Trigger Efficiency "+tag, 25, widebins)
                self.effOR_mva = TH1F("effOR_mva", "Photon Trigger Efficiency "+tag, 25, widebins)
                self.effOR_mva2 = TH1F("effOR_mva2", "Photon Trigger Efficiency "+tag, 25, widebins)
                self.effOR_mva3 = TH1F("effOR_mva3", "Photon Trigger Efficiency "+tag, 25, widebins)

                for i in range(1, self.effOR_cut.GetNbinsX()+1):

                        if self.OR_cut.GetBinContent(i) != 0 and self.notrig_cut.GetBinContent(i) != 0:
                                self.effOR_cut.SetBinContent(i, self.OR_cut.GetBinContent(i)/self.notrig_cut.GetBinContent(i))
                                self.effOR_cut.SetBinError(i, error(self.OR_cut.GetBinContent(i), self.notrig_cut.GetBinContent(i)))
                        if self.OR_mva.GetBinContent(i) != 0 and self.notrig_mva.GetBinContent(i) != 0:
                                self.effOR_mva.SetBinContent(i, self.OR_mva.GetBinContent(i)/self.notrig_mva.GetBinContent(i))
                                self.effOR_mva.SetBinError(i, error(self.OR_mva.GetBinContent(i), self.notrig_mva.GetBinContent(i)))
                        if self.OR_mva2.GetBinContent(i) != 0 and self.notrig_mva2.GetBinContent(i) != 0:
                                self.effOR_mva2.SetBinContent(i, self.OR_mva2.GetBinContent(i)/self.notrig_mva2.GetBinContent(i))
                                self.effOR_mva2.SetBinError(i, error(self.OR_mva2.GetBinContent(i), self.notrig_mva2.GetBinContent(i)))
                        if self.OR_mva3.GetBinContent(i) != 0 and self.notrig_mva3.GetBinContent(i) != 0:
                                self.effOR_mva3.SetBinContent(i, self.OR_mva3.GetBinContent(i)/self.notrig_mva3.GetBinContent(i))
                                self.effOR_mva3.SetBinError(i, error(self.OR_mva3.GetBinContent(i), self.notrig_mva3.GetBinContent(i)))
		
	
		
		self.effOR_cut.SetLineColor(kBlue)
		self.effOR_mva.SetLineColor(kBlack)
		self.effOR_mva2.SetLineColor(kGreen)
		self.effOR_mva3.SetLineColor(kRed)
	
		self.effOR_cut.SetAxisRange(0.9,1.1,"Y")

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.effOR_cut.SetTitle("OR Trigger Efficiency "+tag)
		self.effOR_cut.SetXTitle("Photon pT")
		self.effOR_cut.Draw("histe")
		self.effOR_mva.Draw("same histe")
		self.effOR_mva2.Draw("same histe")
		self.effOR_mva3.Draw("same histe")
		l1 = TLegend(.6, .25, .9, .4)
		l1.AddEntry(self.effOR_cut, "Cut Based")
                l1.AddEntry(self.effOR_mva, "MVA > .8")
                l1.AddEntry(self.effOR_mva2, "MVA > .85")
                l1.AddEntry(self.effOR_mva3, "MVA > .9")
                l1.Draw()
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		c1.SaveAs("./"+name+".root")
		c1.Close()

