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

		self.GJp1 = self.f.Get("pass_soft")
		self.GJp1_1 = self.f.Get("pass_soft_over")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.QCDp1 = self.g.Get("pass_soft")
		self.QCDp1_1 = self.g.Get("pass_soft_over")
		
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.TTp1 = self.h.Get("pass_soft")

		
		self.comb1 = TH1F("comb1", "Background Softdrop Mass", 40, 0, 200)
		self.comb1_over = TH1F("comb1_over", "Background Softdrop Mass With Overlap Removed", 40, 0, 200)
		
		self.comb1.Add(self.GJp1)
		self.comb1.Add(self.QCDp1)
		self.comb1.Add(self.TTp1)
		
		self.comb1_over.Add(self.GJp1_1)
		self.comb1_over.Add(self.QCDp1_1)
		self.comb1_over.Add(self.TTp1)
		
		
		self.GJp1.SetLineColor(kBlue)
		self.GJp1_1.SetLineColor(kCyan)
		self.QCDp1.SetLineColor(kRed)
		self.QCDp1_1.SetLineColor(kOrange)
		self.TTp1.SetLineColor(kPurple)
		self.comb1.SetLineColor(kBlack)
		self.comb1_over.SetLineColor(kBlack)
		
		
		

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.comb1.SetTitle("Background Softdrop Mass")
		self.comb1.Draw("hist")
		self.GJp1.Draw("same hist")
		self.QCDp1.Draw("same hist")
		self.TTp1.Draw("same hist")
		l1 = TLegend(.6, .75, .9, .9)
		l1.AddEntry(self.GJp1, "GJets")
                l1.AddEntry(self.QCDp1, "QCD")
                l1.AddEntry(self.TTp1, "TTBar")
                l1.Draw()
		gPad.SetLogy()
		c1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+name+"_soft.png")
		c1.Close()

		c2 = TCanvas()
		c2.cd()
		self.comb1_over.SetTitle("Background Softdrop Mass With Overlap Removed")
		self.comb1_over.Draw("hist")
		self.GJp1_1.Draw("same hist")
		self.QCDp1_1.Draw("same hist")
		self.TTp1.Draw("same hist")
		l2 = TLegend(.6, .75, .9, .9)
		l2.AddEntry(self.GJp1_1, "GJets")
                l2.AddEntry(self.QCDp1_1, "QCD")
                l2.AddEntry(self.TTp1, "TTBar")
                l2.Draw()
		gPad.SetLogy()
		c2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+name+"_soft_over.png")
		c2.Close()

		
		
		
		
