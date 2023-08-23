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
def FindAndSetMax(*args):
        if len(args) == 1: args = args[0]
        maximum = 0.0
        for i in args:
                i.SetStats(0)
                t = i.GetMaximum()
                if t > maximum:
                        maximum = t
        for j in args:
                j.GetYaxis().SetRangeUser(1,maximum*1.35)#should be 1.35 (below as well)
                j.SetLineWidth(2)
        return maximum*1.35
class drawRData:
	def __init__(self, name, sfile1, sfile2, sfile3, sfile4, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/SRootB_barrel/"+o,"RECREATE")

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.M10 = self.f.Get("SRB_all_10")
		self.M10_high = self.f.Get("SRB_high_10")

		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.M25 = self.g.Get("SRB_all_25")
		self.M25_high = self.g.Get("SRB_high_25")
		
		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.M50 = self.h.Get("SRB_all_50")
		self.M50_high = self.h.Get("SRB_high_50")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.M75 = self.i.Get("SRB_all_75")
		self.M75_high = self.i.Get("SRB_high_75")
	
		self.M10.SetLineColor(kBlack)
		self.M10.SetLineWidth(2)
		self.M10.SetMarkerColor(kBlack)
		self.M10.SetMarkerSize(2)
		
		self.M10_high.SetLineColor(kBlack)
		self.M10_high.SetLineWidth(2)
		self.M10_high.SetMarkerColor(kBlack)
		self.M10_high.SetMarkerSize(2)
	
		self.M10.GetYaxis().SetRangeUser(0, 40)
                self.M10_high.GetYaxis().SetRangeUser(0, 40)
	
		self.M25.SetLineColor(kRed)
		self.M25.SetLineWidth(2)
		self.M25.SetMarkerColor(kRed)
		self.M25.SetMarkerSize(2)
		
		self.M25_high.SetLineColor(kRed)
		self.M25_high.SetLineWidth(2)
		self.M25_high.SetMarkerColor(kRed)
		self.M25_high.SetMarkerSize(2)
		
		self.M50.SetLineColor(kGreen)
		self.M50.SetLineWidth(2)
		self.M50.SetMarkerColor(kGreen)
		self.M50.SetMarkerSize(2)
		
		self.M50_high.SetLineColor(kGreen)
		self.M50_high.SetLineWidth(2)
		self.M50_high.SetMarkerColor(kGreen)
		self.M50_high.SetMarkerSize(2)
		
		self.M75.SetLineColor(kBlue)
		self.M75.SetLineWidth(2)
		self.M75.SetMarkerColor(kBlue)
		self.M75.SetMarkerSize(2)
		
		self.M75_high.SetLineColor(kBlue)
		self.M75_high.SetLineWidth(2)
		self.M75_high.SetMarkerColor(kBlue)
		self.M75_high.SetMarkerSize(2)

		ROOT.gStyle.SetOptStat(0)

		c5 = TCanvas()
		c5.cd()
#                gPad.SetLogy()
		self.M10.SetTitle("2018 S/Root(B) vs. DDT%")
		self.M10.Draw("ALP*")
		self.M25.Draw("LP*")
		self.M50.Draw("LP*")
		self.M75.Draw("LP*")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.M10, "10 GeV Signal")
                l1.AddEntry(self.M25, "25 GeV Signal")
                l1.AddEntry(self.M50, "50 GeV Signal")
                l1.AddEntry(self.M75, "75 GeV Signal")
                l1.Draw()
                gPad.Update()
		c5.SaveAs("./plots/SRootB_barrel_ALL.png")
		c5.Close()
		
		c6 = TCanvas()
		c6.cd()
#                gPad.SetLogy()
		self.M10_high.SetTitle("2018 S/Root(B) vs. DDT% (Jet pT > 200)")
		self.M10_high.Draw("ALP*")
		self.M25_high.Draw("LP*")
		self.M50_high.Draw("LP*")
		self.M75_high.Draw("LP*")
                l2 = TLegend(.6, .75, .9, .9)
                l2.AddEntry(self.M10_high, "10 GeV Signal")
                l2.AddEntry(self.M25_high, "25 GeV Signal")
                l2.AddEntry(self.M50_high, "50 GeV Signal")
                l2.AddEntry(self.M75_high, "75 GeV Signal")
                l2.Draw()
                gPad.Update()
		c6.SaveAs("./plots/SRootB_barrel_ALL_high.png")
		c6.Close()

		
		ofile.Write()
