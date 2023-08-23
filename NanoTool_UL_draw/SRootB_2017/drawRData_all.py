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

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/SRootB_2017/"+o,"RECREATE")

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.M10 = self.f.Get("SRB_all_10")

		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.M25 = self.g.Get("SRB_all_25")
		
		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.M50 = self.h.Get("SRB_all_50")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.M75 = self.i.Get("SRB_all_75")
	
		self.M10.SetLineColor(kBlack)
		self.M10.SetLineWidth(2)
		self.M10.SetMarkerColor(kBlack)
		self.M10.SetMarkerSize(2)
		
		self.M25.SetLineColor(kRed)
		self.M25.SetLineWidth(2)
		self.M25.SetMarkerColor(kRed)
		self.M25.SetMarkerSize(2)
	
		self.M25.GetYaxis().SetRangeUser(0, 25)
	
		self.M50.SetLineColor(kGreen)
		self.M50.SetLineWidth(2)
		self.M50.SetMarkerColor(kGreen)
		self.M50.SetMarkerSize(2)
		
		self.M75.SetLineColor(kBlue)
		self.M75.SetLineWidth(2)
		self.M75.SetMarkerColor(kBlue)
		self.M75.SetMarkerSize(2)
		
		ROOT.gStyle.SetOptStat(0)

		c5 = TCanvas()
		c5.cd()
#                gPad.SetLogy()
		self.M25.SetTitle("2017 S/Root(B) vs. DDT%")
		self.M25.Draw("ALP*")
		self.M10.Draw("LP*")
		self.M50.Draw("LP*")
		self.M75.Draw("LP*")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.M10, "10 GeV Signal")
                l1.AddEntry(self.M25, "25 GeV Signal")
                l1.AddEntry(self.M50, "50 GeV Signal")
                l1.AddEntry(self.M75, "75 GeV Signal")
                l1.Draw()
                gPad.Update()
		c5.SaveAs("./plots/SRootB_barrel_ALL_2017.png")
		c5.Close()
		
		
		ofile.Write()
