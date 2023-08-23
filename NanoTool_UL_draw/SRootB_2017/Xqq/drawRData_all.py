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
	def __init__(self, name, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/SRootB_2017/Xqq/"+o,"RECREATE")

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.M10 = self.f.Get("SRB_all_10")
		self.M10_all = self.f.Get("SRBALL_all_10")

		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.M25 = self.g.Get("SRB_all_25")
		self.M25_all = self.g.Get("SRBALL_all_25")
		
		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.M50 = self.h.Get("SRB_all_50")
		self.M50_all = self.h.Get("SRBALL_all_50")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.M75 = self.i.Get("SRB_all_75")
		self.M75_all = self.i.Get("SRBALL_all_75")
		
		self.j = TFile.Open(sfile5, "READ")
		self.j.ls();

		self.WG = self.j.Get("SRB_all_80.379")
		self.WG_all = self.j.Get("SRBALL_all_80.379")
		
		self.k = TFile.Open(sfile6, "READ")
		self.k.ls();

		self.ZG = self.k.Get("SRB_all_91.188")
		self.ZG_all = self.k.Get("SRBALL_all_91.188")
	
		self.M10.SetLineColor(kBlack)
		self.M10.SetLineWidth(2)
		self.M10.SetMarkerColor(kBlack)
		self.M10.SetMarkerSize(2)
		
		self.M10_all.SetLineColor(kBlack)
		self.M10_all.SetLineWidth(2)
		self.M10_all.SetMarkerColor(kBlack)
		self.M10_all.SetMarkerSize(2)
		
		self.M25.SetLineColor(kRed)
		self.M25.SetLineWidth(2)
		self.M25.SetMarkerColor(kRed)
		self.M25.SetMarkerSize(2)
		
		self.M25_all.SetLineColor(kRed)
		self.M25_all.SetLineWidth(2)
		self.M25_all.SetMarkerColor(kRed)
		self.M25_all.SetMarkerSize(2)
	
		self.M25.GetYaxis().SetRangeUser(0, 20)
		self.M25_all.GetYaxis().SetRangeUser(0, 25)
	
		self.M50.SetLineColor(kGreen)
		self.M50.SetLineWidth(2)
		self.M50.SetMarkerColor(kGreen)
		self.M50.SetMarkerSize(2)
		
		self.M50_all.SetLineColor(kGreen)
		self.M50_all.SetLineWidth(2)
		self.M50_all.SetMarkerColor(kGreen)
		self.M50_all.SetMarkerSize(2)
		
		self.M75.SetLineColor(kBlue)
		self.M75.SetLineWidth(2)
		self.M75.SetMarkerColor(kBlue)
		self.M75.SetMarkerSize(2)
		
		self.M75_all.SetLineColor(kBlue)
		self.M75_all.SetLineWidth(2)
		self.M75_all.SetMarkerColor(kBlue)
		self.M75_all.SetMarkerSize(2)
		
		self.WG.SetLineColor(kYellow)
		self.WG.SetLineWidth(2)
		self.WG.SetMarkerColor(kYellow)
		self.WG.SetMarkerSize(2)
		
		self.WG_all.SetLineColor(kYellow)
		self.WG_all.SetLineWidth(2)
		self.WG_all.SetMarkerColor(kYellow)
		self.WG_all.SetMarkerSize(2)
		
		self.ZG.SetLineColor(kCyan)
		self.ZG.SetLineWidth(2)
		self.ZG.SetMarkerColor(kCyan)
		self.ZG.SetMarkerSize(2)
		
		self.ZG_all.SetLineColor(kCyan)
		self.ZG_all.SetLineWidth(2)
		self.ZG_all.SetMarkerColor(kCyan)
		self.ZG_all.SetMarkerSize(2)
		
		ROOT.gStyle.SetOptStat(0)

		c5 = TCanvas()
		c5.cd()
		self.M25.SetTitle("2017 S/Root(B) vs. Xqq/(Xqq+QCD) Score Cut")
		self.M25.Draw("ALP*")
		self.M10.Draw("LP*")
		self.M50.Draw("LP*")
		self.M75.Draw("LP*")
		self.WG.Draw("LP*")
		self.ZG.Draw("LP*")
                l1 = TLegend(.1, .75, .4, .9)
                l1.AddEntry(self.M10, "10 GeV Signal")
                l1.AddEntry(self.M25, "25 GeV Signal")
                l1.AddEntry(self.M50, "50 GeV Signal")
                l1.AddEntry(self.M75, "75 GeV Signal")
                l1.AddEntry(self.WG, "W+Gamma GeV Signal")
                l1.AddEntry(self.ZG, "Z+Gamma GeV Signal")
                l1.Draw()
                gPad.Update()
		c5.SaveAs("./plots/SRootB_barrel_Xqq_2017.png")
		c5.Close()
		
		c6 = TCanvas()
		c6.cd()
		self.M25_all.SetTitle("2017 S/Root(B) vs. (Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD) Score Cut")
		self.M25_all.Draw("ALP*")
		self.M10_all.Draw("LP*")
		self.M50_all.Draw("LP*")
		self.M75_all.Draw("LP*")
		self.WG_all.Draw("LP*")
		self.ZG_all.Draw("LP*")
                l1 = TLegend(.1, .75, .4, .9)
                l1.AddEntry(self.M10_all, "10 GeV Signal")
                l1.AddEntry(self.M25_all, "25 GeV Signal")
                l1.AddEntry(self.M50_all, "50 GeV Signal")
                l1.AddEntry(self.M75_all, "75 GeV Signal")
                l1.AddEntry(self.WG_all, "W+Gamma GeV Signal")
                l1.AddEntry(self.ZG_all, "Z+Gamma GeV Signal")
                l1.Draw()
                gPad.Update()
		c6.SaveAs("./plots/SRootB_barrel_XqqALL_2017.png")
		c6.Close()
		
		ofile.Write()
