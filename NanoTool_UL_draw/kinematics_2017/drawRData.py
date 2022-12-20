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

def GoodPlotFormat(H, *args): # Handy little script for color/line/fill/point/etc...
        try: H.SetStats(0)
        except: print " ------------ [  No stats box found!  ]"
        if args[0] == 'thickline':
                H.SetLineColor(args[1])
                H.SetLineWidth(2)
        if args[0] == 'thinline':
                H.SetLineColor(args[1])
                H.SetLineWidth(1)
                H.SetLineStyle(args[2])
        if args[0] == 'fill':
                H.SetLineColor(args[1])
                #H.SetFillColorAlpha(args[1], 1.0)
                H.SetFillColor(args[1])
                H.SetFillStyle(args[2])
        if args[0] == 'markers':
                H.SetLineColor(args[1])
                H.SetMarkerColor(args[1])
                H.SetMarkerStyle(args[2])
                H.SetMarkerSize(1.1)
        H.GetXaxis().SetTitleSize(0.04)

        if args[0] == 'dashed':
                H.SetLineColor(args[1])
                H.SetLineWidth(1)
                H.SetLineStyle(7)
def convertAsymGraph(TG, template, name):
        Hist = template.Clone(name)
        for i in range(1,Hist.GetNbinsX()+1):
                Hist.SetBinContent(i,0.)

#       print("Number of points: "+str(TG.GetN()))

        for i in range(TG.GetN()):
        #       Hist.SetBinContent(i+1,TG.GetY()[i]*(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
                Hist.SetBinContent(i+1,TG.GetY()[i])
#               print("Y= "+str(TG.GetY()[i]))
#               print("error xlow + error xhigh = "+str(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
                Hist.SetBinError(i+1, TG.GetErrorY(i))
        return Hist

def convertBinNHist(H, template, name):
        Hist = template.Clone(name)
        for i in range(1,Hist.GetNbinsX()+1):
                Hist.SetBinContent(i,H.GetBinContent(i))
                Hist.SetBinError(i,H.GetBinError(i))
        return Hist

def MakeNBinsFromMinToMax(N,Min,Max): # helper for making large bin arrays makes N bins between Min and Max (same as you're feed to a TH1F)
        BINS = []
        for i in range(N+1):
                BINS.append(Min+(i*(Max-Min)/N))
        return BINS

def DBBW(H):
        for i in range(1,H.GetNbinsX()+1):
                C = H.GetBinContent(i)
                E = H.GetBinError(i)
                W = H.GetBinWidth(i)
                H.SetBinContent(i, C/W)
                H.SetBinError(i, E/W)
        return H
def AddCMSLumi(pad, fb, extra):
        cmsText     = "CMS " + extra
        cmsTextFont   = 61
        lumiTextSize     = 0.45
        lumiTextOffset   = 0.15
        cmsTextSize      = 0.5
        cmsTextOffset    = 0.15
        H = pad.GetWh()
        W = pad.GetWw()
        l = pad.GetLeftMargin()
        t = pad.GetTopMargin()
        r = pad.GetRightMargin()
        b = pad.GetBottomMargin()
        e = 0.025
        pad.cd()
        lumiText = str(fb)+" fb^{-1} (13 TeV)"
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(kBlack)
        extraTextSize = 0.76*cmsTextSize
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(lumiTextSize*t)
        latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
        pad.cd()
        latex.SetTextFont(cmsTextFont)
        latex.SetTextSize(cmsTextSize*t)
        latex.SetTextAlign(11)
        latex.DrawLatex(0.1265, 0.825, cmsText)
        pad.Update()

class drawRData:
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, ifile9, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/kinematics_2017/"+o,"RECREATE")
		
		self.c = TFile.Open(ifile1, "READ")
		self.c.ls();

		self.h1_sig10 = self.c.Get("softdrop")
		self.h2_sig10 = self.c.Get("jet_pt")
		self.h2_1_sig10 = self.c.Get("thin_jet_pt")
		self.h3_sig10 = self.c.Get("jet_eta")
		self.h4_sig10 = self.c.Get("photon_pt")
		self.h5_sig10 = self.c.Get("rho")
		self.h6_sig10 = self.c.Get("N2")
		self.h7_sig10 = self.c.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_sig10 = self.c.Get("PuppiMETPT")
		self.h9_sig10 = self.c.Get("ak4_btag")
		

		self.p1_sig10 = self.c.Get("pass_soft")
		self.p1_1_sig10 = self.c.Get("pass_soft_thin")
		self.p2_sig10 = self.c.Get("pass_jet_pt")
		self.p3_sig10 = self.c.Get("pass_jet_eta")
		self.p4_sig10 = self.c.Get("pass_photon_pt")
		self.p5_sig10 = self.c.Get("pass_rho")
		
		self.f1_sig10 = self.c.Get("fail_soft")
		self.f1_1_sig10 = self.c.Get("fail_soft_thin")
		self.f2_sig10 = self.c.Get("fail_jet_pt")
		self.f3_sig10 = self.c.Get("fail_jet_eta")
		self.f4_sig10 = self.c.Get("fail_photon_pt")
		self.f5_sig10 = self.c.Get("fail_rho")

		GoodPlotFormat(self.h1_sig10, 'thickline', 4)
		GoodPlotFormat(self.h2_sig10, 'thickline', 4)
		GoodPlotFormat(self.h4_sig10, 'thickline', 4)

		self.d = TFile.Open(ifile2, "READ")
		self.d.ls();

		self.h1_sig25 = self.d.Get("softdrop")
		self.h2_sig25 = self.d.Get("jet_pt")
		self.h2_1_sig25 = self.d.Get("thin_jet_pt")
		self.h3_sig25 = self.d.Get("jet_eta")
		self.h4_sig25 = self.d.Get("photon_pt")
		self.h5_sig25 = self.d.Get("rho")
		self.h6_sig25 = self.d.Get("N2")
		self.h7_sig25 = self.d.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_sig25 = self.d.Get("PuppiMETPT")
		self.h9_sig25 = self.d.Get("ak4_btag")
		

		self.p1_sig25 = self.d.Get("pass_soft")
		self.p1_1_sig25 = self.d.Get("pass_soft_thin")
		self.p2_sig25 = self.d.Get("pass_jet_pt")
		self.p3_sig25 = self.d.Get("pass_jet_eta")
		self.p4_sig25 = self.d.Get("pass_photon_pt")
		self.p5_sig25 = self.d.Get("pass_rho")
		
		self.f1_sig25 = self.d.Get("fail_soft")
		self.f1_1_sig25 = self.d.Get("fail_soft_thin")
		self.f2_sig25 = self.d.Get("fail_jet_pt")
		self.f3_sig25 = self.d.Get("fail_jet_eta")
		self.f4_sig25 = self.d.Get("fail_photon_pt")
		self.f5_sig25 = self.d.Get("fail_rho")

		GoodPlotFormat(self.h1_sig25, 'thickline', 3)
		GoodPlotFormat(self.h2_sig25, 'thickline', 3)
		GoodPlotFormat(self.h4_sig25, 'thickline', 3)
		
		self.e = TFile.Open(ifile3, "READ")
		self.e.ls();

		self.h1_sig50 = self.e.Get("softdrop")
		self.h2_sig50 = self.e.Get("jet_pt")
		self.h2_1_sig50 = self.e.Get("thin_jet_pt")
		self.h3_sig50 = self.e.Get("jet_eta")
		self.h4_sig50 = self.e.Get("photon_pt")
		self.h5_sig50 = self.e.Get("rho")
		self.h6_sig50 = self.e.Get("N2")
		self.h7_sig50 = self.e.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_sig50 = self.e.Get("PuppiMETPT")
		self.h9_sig50 = self.e.Get("ak4_btag")
		

		self.p1_sig50 = self.e.Get("pass_soft")
		self.p1_1_sig50 = self.e.Get("pass_soft_thin")
		self.p2_sig50 = self.e.Get("pass_jet_pt")
		self.p3_sig50 = self.e.Get("pass_jet_eta")
		self.p4_sig50 = self.e.Get("pass_photon_pt")
		self.p5_sig50 = self.e.Get("pass_rho")
		
		self.f1_sig50 = self.e.Get("fail_soft")
		self.f1_1_sig50 = self.e.Get("fail_soft_thin")
		self.f2_sig50 = self.e.Get("fail_jet_pt")
		self.f3_sig50 = self.e.Get("fail_jet_eta")
		self.f4_sig50 = self.e.Get("fail_photon_pt")
		self.f5_sig50 = self.e.Get("fail_rho")

		GoodPlotFormat(self.h1_sig50, 'thickline', 2)
		GoodPlotFormat(self.h2_sig50, 'thickline', 2)
		GoodPlotFormat(self.h4_sig50, 'thickline', 2)
		
		self.f = TFile.Open(ifile4, "READ")
		self.f.ls();

		self.h1_sig75 = self.f.Get("softdrop")
		self.h2_sig75 = self.f.Get("jet_pt")
		self.h2_1_sig75 = self.f.Get("thin_jet_pt")
		self.h3_sig75 = self.f.Get("jet_eta")
		self.h4_sig75 = self.f.Get("photon_pt")
		self.h5_sig75 = self.f.Get("rho")
		self.h6_sig75 = self.f.Get("N2")
		self.h7_sig75 = self.f.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_sig75 = self.f.Get("PuppiMETPT")
		self.h9_sig75 = self.f.Get("ak4_btag")
		

		self.p1_sig75 = self.f.Get("pass_soft")
		self.p1_1_sig75 = self.f.Get("pass_soft_thin")
		self.p2_sig75 = self.f.Get("pass_jet_pt")
		self.p3_sig75 = self.f.Get("pass_jet_eta")
		self.p4_sig75 = self.f.Get("pass_photon_pt")
		self.p5_sig75 = self.f.Get("pass_rho")
		
		self.f1_sig75 = self.f.Get("fail_soft")
		self.f1_1_sig75 = self.f.Get("fail_soft_thin")
		self.f2_sig75 = self.f.Get("fail_jet_pt")
		self.f3_sig75 = self.f.Get("fail_jet_eta")
		self.f4_sig75 = self.f.Get("fail_photon_pt")
		self.f5_sig75 = self.f.Get("fail_rho")

		GoodPlotFormat(self.h1_sig75, 'thickline', 6)
		GoodPlotFormat(self.h2_sig75, 'thickline', 6)
		GoodPlotFormat(self.h4_sig75, 'thickline', 6)

		self.g = TFile.Open(ifile5, "READ")
		self.g.ls();

		self.h1_WG = self.g.Get("softdrop")
		self.h2_WG = self.g.Get("jet_pt")
		self.h2_1_WG = self.g.Get("thin_jet_pt")
		self.h3_WG = self.g.Get("jet_eta")
		self.h4_WG = self.g.Get("photon_pt")
		self.h5_WG = self.g.Get("rho")
		self.h6_WG = self.g.Get("N2")
		self.h7_WG = self.g.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_WG = self.g.Get("PuppiMETPT")
		self.h9_WG = self.g.Get("ak4_btag")
		

		self.p1_WG = self.g.Get("pass_soft")
		self.p1_1_WG = self.g.Get("pass_soft_thin")
		self.p2_WG = self.g.Get("pass_jet_pt")
		self.p3_WG = self.g.Get("pass_jet_eta")
		self.p4_WG = self.g.Get("pass_photon_pt")
		self.p5_WG = self.g.Get("pass_rho")
		
		self.f1_WG = self.g.Get("fail_soft")
		self.f1_1_WG = self.g.Get("fail_soft_thin")
		self.f2_WG = self.g.Get("fail_jet_pt")
		self.f3_WG = self.g.Get("fail_jet_eta")
		self.f4_WG = self.g.Get("fail_photon_pt")
		self.f5_WG = self.g.Get("fail_rho")
		
		#GoodPlotFormat(self.h1_WG, 'fill', 5, 3003)
		GoodPlotFormat(self.h1_WG, 'fill', 5, 1001)
		GoodPlotFormat(self.h2_WG, 'fill', 5, 1001)
		GoodPlotFormat(self.h4_WG, 'fill', 5, 1001)
		
		self.h = TFile.Open(ifile6, "READ")
		self.h.ls();

		self.h1_ZG = self.h.Get("softdrop")
		self.h2_ZG = self.h.Get("jet_pt")
		self.h2_1_ZG = self.h.Get("thin_jet_pt")
		self.h3_ZG = self.h.Get("jet_eta")
		self.h4_ZG = self.h.Get("photon_pt")
		self.h5_ZG = self.h.Get("rho")
		self.h6_ZG = self.h.Get("N2")
		self.h7_ZG = self.h.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_ZG = self.h.Get("PuppiMETPT")
		self.h9_ZG = self.h.Get("ak4_btag")
		

		self.p1_ZG = self.h.Get("pass_soft")
		self.p1_1_ZG = self.h.Get("pass_soft_thin")
		self.p2_ZG = self.h.Get("pass_jet_pt")
		self.p3_ZG = self.h.Get("pass_jet_eta")
		self.p4_ZG = self.h.Get("pass_photon_pt")
		self.p5_ZG = self.h.Get("pass_rho")
		
		self.f1_ZG = self.h.Get("fail_soft")
		self.f1_1_ZG = self.h.Get("fail_soft_thin")
		self.f2_ZG = self.h.Get("fail_jet_pt")
		self.f3_ZG = self.h.Get("fail_jet_eta")
		self.f4_ZG = self.h.Get("fail_photon_pt")
		self.f5_ZG = self.h.Get("fail_rho")
		
		#GoodPlotFormat(self.h1_ZG, 'fill', 6, 3003)
		GoodPlotFormat(self.h1_ZG, 'fill', 40, 1001)
		GoodPlotFormat(self.h2_ZG, 'fill', 40, 1001)
		GoodPlotFormat(self.h4_ZG, 'fill', 40, 1001)
		
		self.i = TFile.Open(ifile7, "READ")
		self.i.ls();

		self.h1_GJ = self.i.Get("softdrop")
		self.h2_GJ = self.i.Get("jet_pt")
		self.h2_1_GJ = self.i.Get("thin_jet_pt")
		self.h3_GJ = self.i.Get("jet_eta")
		self.h4_GJ = self.i.Get("photon_pt")
		self.h5_GJ = self.i.Get("rho")
		self.h6_GJ = self.i.Get("N2")
		self.h7_GJ = self.i.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_GJ = self.i.Get("PuppiMETPT")
		self.h9_GJ = self.i.Get("ak4_btag")
		

		self.p1_GJ = self.i.Get("pass_soft")
		self.p1_1_GJ = self.i.Get("pass_soft_thin")
		self.p2_GJ = self.i.Get("pass_jet_pt")
		self.p3_GJ = self.i.Get("pass_jet_eta")
		self.p4_GJ = self.i.Get("pass_photon_pt")
		self.p5_GJ = self.i.Get("pass_rho")
		
		self.f1_GJ = self.i.Get("fail_soft")
		self.f1_1_GJ = self.i.Get("fail_soft_thin")
		self.f2_GJ = self.i.Get("fail_jet_pt")
		self.f3_GJ = self.i.Get("fail_jet_eta")
		self.f4_GJ = self.i.Get("fail_photon_pt")
		self.f5_GJ = self.i.Get("fail_rho")
		
		#GoodPlotFormat(self.h1_GJ, 'fill', 38, 3144)
		GoodPlotFormat(self.h1_GJ, 'fill', 38, 1001)
		GoodPlotFormat(self.h2_GJ, 'fill', 38, 1001)
		GoodPlotFormat(self.h4_GJ, 'fill', 38, 1001)
		
		self.j = TFile.Open(ifile8, "READ")
		self.j.ls();

		self.h1_TT = self.j.Get("softdrop")
		self.h2_TT = self.j.Get("jet_pt")
		self.h2_1_TT = self.j.Get("thin_jet_pt")
		self.h3_TT = self.j.Get("jet_eta")
		self.h4_TT = self.j.Get("photon_pt")
		self.h5_TT = self.j.Get("rho")
		self.h6_TT = self.j.Get("N2")
		self.h7_TT = self.j.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_TT = self.j.Get("PuppiMETPT")
		self.h9_TT = self.j.Get("ak4_btag")
		

		self.p1_TT = self.j.Get("pass_soft")
		self.p1_1_TT = self.j.Get("pass_soft_thin")
		self.p2_TT = self.j.Get("pass_jet_pt")
		self.p3_TT = self.j.Get("pass_jet_eta")
		self.p4_TT = self.j.Get("pass_photon_pt")
		self.p5_TT = self.j.Get("pass_rho")
		
		self.f1_TT = self.j.Get("fail_soft")
		self.f1_1_TT = self.j.Get("fail_soft_thin")
		self.f2_TT = self.j.Get("fail_jet_pt")
		self.f3_TT = self.j.Get("fail_jet_eta")
		self.f4_TT = self.j.Get("fail_photon_pt")
		self.f5_TT = self.j.Get("fail_rho")
		
		#GoodPlotFormat(self.h1_TT, 'fill', 30, 3003)
		GoodPlotFormat(self.h1_TT, 'fill', 30, 1001)
		GoodPlotFormat(self.h2_TT, 'fill', 30, 1001)
		GoodPlotFormat(self.h4_TT, 'fill', 30, 1001)
		
		self.k = TFile.Open(ifile9, "READ")
		self.k.ls();

		self.h1_Data = self.k.Get("softdrop")
		self.h2_Data = self.k.Get("jet_pt")
		self.h2_1_Data = self.k.Get("thin_jet_pt")
		self.h3_Data = self.k.Get("jet_eta")
		self.h4_Data = self.k.Get("photon_pt")
		self.h5_Data = self.k.Get("rho")
		self.h6_Data = self.k.Get("N2")
		self.h7_Data = self.k.Get("n2ddt")

		#These do have b-veto applied, may need to remake without them
		self.h8_Data = self.k.Get("PuppiMETPT")
		self.h9_Data = self.k.Get("ak4_btag")
		

		self.p1_Data = self.k.Get("pass_soft")
		self.p1_1_Data = self.k.Get("pass_soft_thin")
		self.p2_Data = self.k.Get("pass_jet_pt")
		self.p3_Data = self.k.Get("pass_jet_eta")
		self.p4_Data = self.k.Get("pass_photon_pt")
		self.p5_Data = self.k.Get("pass_rho")
		
		self.f1_Data = self.k.Get("fail_soft")
		self.f1_1_Data = self.k.Get("fail_soft_thin")
		self.f2_Data = self.k.Get("fail_jet_pt")
		self.f3_Data = self.k.Get("fail_jet_eta")
		self.f4_Data = self.k.Get("fail_photon_pt")
		self.f5_Data = self.k.Get("fail_rho")
		
		GoodPlotFormat(self.h1_Data, "markers", ROOT.kBlack, 20)
		GoodPlotFormat(self.h2_Data, "markers", ROOT.kBlack, 20)
		GoodPlotFormat(self.h4_Data, "markers", ROOT.kBlack, 20)


		#Scale MC to 10% of Data
		self.h1_sig10.Scale(.1)	
		self.h2_sig10.Scale(.1)	
		self.h2_1_sig10.Scale(.1)	
		self.h3_sig10.Scale(.1)	
		self.h4_sig10.Scale(.1)	
		self.h5_sig10.Scale(.1)	
		self.h6_sig10.Scale(.1)	
		self.h7_sig10.Scale(.1)	
		self.h8_sig10.Scale(.1)	
		self.h9_sig10.Scale(.1)	
		self.p1_sig10.Scale(.1)	
		self.p1_1_sig10.Scale(.1)	
		self.p2_sig10.Scale(.1)	
		self.p3_sig10.Scale(.1)	
		self.p4_sig10.Scale(.1)	
		self.p5_sig10.Scale(.1)	
		self.f1_sig10.Scale(.1)	
		self.f1_1_sig10.Scale(.1)	
		self.f2_sig10.Scale(.1)	
		self.f3_sig10.Scale(.1)	
		self.f4_sig10.Scale(.1)	
		self.f5_sig10.Scale(.1)	


		self.h1_sig25.Scale(.1)	
		self.h2_sig25.Scale(.1)	
		self.h2_1_sig25.Scale(.1)	
		self.h3_sig25.Scale(.1)	
		self.h4_sig25.Scale(.1)	
		self.h5_sig25.Scale(.1)	
		self.h6_sig25.Scale(.1)	
		self.h7_sig25.Scale(.1)	
		self.h8_sig25.Scale(.1)	
		self.h9_sig25.Scale(.1)	
		self.p1_sig25.Scale(.1)	
		self.p1_1_sig25.Scale(.1)	
		self.p2_sig25.Scale(.1)	
		self.p3_sig25.Scale(.1)	
		self.p4_sig25.Scale(.1)	
		self.p5_sig25.Scale(.1)	
		self.f1_sig25.Scale(.1)	
		self.f1_1_sig25.Scale(.1)	
		self.f2_sig25.Scale(.1)	
		self.f3_sig25.Scale(.1)	
		self.f4_sig25.Scale(.1)	
		self.f5_sig25.Scale(.1)	
		
		self.h1_sig50.Scale(.1)	
		self.h2_sig50.Scale(.1)	
		self.h2_1_sig50.Scale(.1)	
		self.h3_sig50.Scale(.1)	
		self.h4_sig50.Scale(.1)	
		self.h5_sig50.Scale(.1)	
		self.h6_sig50.Scale(.1)	
		self.h7_sig50.Scale(.1)	
		self.h8_sig50.Scale(.1)	
		self.h9_sig50.Scale(.1)	
		self.p1_sig50.Scale(.1)	
		self.p1_1_sig50.Scale(.1)	
		self.p2_sig50.Scale(.1)	
		self.p3_sig50.Scale(.1)	
		self.p4_sig50.Scale(.1)	
		self.p5_sig50.Scale(.1)	
		self.f1_sig50.Scale(.1)	
		self.f1_1_sig50.Scale(.1)	
		self.f2_sig50.Scale(.1)	
		self.f3_sig50.Scale(.1)	
		self.f4_sig50.Scale(.1)	
		self.f5_sig50.Scale(.1)	
		
		self.h1_sig75.Scale(.1)	
		self.h2_sig75.Scale(.1)	
		self.h2_1_sig75.Scale(.1)	
		self.h3_sig75.Scale(.1)	
		self.h4_sig75.Scale(.1)	
		self.h5_sig75.Scale(.1)	
		self.h6_sig75.Scale(.1)	
		self.h7_sig75.Scale(.1)	
		self.h8_sig75.Scale(.1)	
		self.h9_sig75.Scale(.1)	
		self.p1_sig75.Scale(.1)	
		self.p1_1_sig75.Scale(.1)	
		self.p2_sig75.Scale(.1)	
		self.p3_sig75.Scale(.1)	
		self.p4_sig75.Scale(.1)	
		self.p5_sig75.Scale(.1)	
		self.f1_sig75.Scale(.1)	
		self.f1_1_sig75.Scale(.1)	
		self.f2_sig75.Scale(.1)	
		self.f3_sig75.Scale(.1)	
		self.f4_sig75.Scale(.1)	
		self.f5_sig75.Scale(.1)	
		
		self.h1_WG.Scale(.1)	
		self.h2_WG.Scale(.1)	
		self.h2_1_WG.Scale(.1)	
		self.h3_WG.Scale(.1)	
		self.h4_WG.Scale(.1)	
		self.h5_WG.Scale(.1)	
		self.h6_WG.Scale(.1)	
		self.h7_WG.Scale(.1)	
		self.h8_WG.Scale(.1)	
		self.h9_WG.Scale(.1)	
		self.p1_WG.Scale(.1)	
		self.p1_1_WG.Scale(.1)	
		self.p2_WG.Scale(.1)	
		self.p3_WG.Scale(.1)	
		self.p4_WG.Scale(.1)	
		self.p5_WG.Scale(.1)	
		self.f1_WG.Scale(.1)	
		self.f1_1_WG.Scale(.1)	
		self.f2_WG.Scale(.1)	
		self.f3_WG.Scale(.1)	
		self.f4_WG.Scale(.1)	
		self.f5_WG.Scale(.1)	
		
		self.h1_ZG.Scale(.1)	
		self.h2_ZG.Scale(.1)	
		self.h2_1_ZG.Scale(.1)	
		self.h3_ZG.Scale(.1)	
		self.h4_ZG.Scale(.1)	
		self.h5_ZG.Scale(.1)	
		self.h6_ZG.Scale(.1)	
		self.h7_ZG.Scale(.1)	
		self.h8_ZG.Scale(.1)	
		self.h9_ZG.Scale(.1)	
		self.p1_ZG.Scale(.1)	
		self.p1_1_ZG.Scale(.1)	
		self.p2_ZG.Scale(.1)	
		self.p3_ZG.Scale(.1)	
		self.p4_ZG.Scale(.1)	
		self.p5_ZG.Scale(.1)	
		self.f1_ZG.Scale(.1)	
		self.f1_1_ZG.Scale(.1)	
		self.f2_ZG.Scale(.1)	
		self.f3_ZG.Scale(.1)	
		self.f4_ZG.Scale(.1)	
		self.f5_ZG.Scale(.1)	
		
		self.h1_GJ.Scale(.1)	
		self.h2_GJ.Scale(.1)	
		self.h2_1_GJ.Scale(.1)	
		self.h3_GJ.Scale(.1)	
		self.h4_GJ.Scale(.1)	
		self.h5_GJ.Scale(.1)	
		self.h6_GJ.Scale(.1)	
		self.h7_GJ.Scale(.1)	
		self.h8_GJ.Scale(.1)	
		self.h9_GJ.Scale(.1)	
		self.p1_GJ.Scale(.1)	
		self.p1_1_GJ.Scale(.1)	
		self.p2_GJ.Scale(.1)	
		self.p3_GJ.Scale(.1)	
		self.p4_GJ.Scale(.1)	
		self.p5_GJ.Scale(.1)	
		self.f1_GJ.Scale(.1)	
		self.f1_1_GJ.Scale(.1)	
		self.f2_GJ.Scale(.1)	
		self.f3_GJ.Scale(.1)	
		self.f4_GJ.Scale(.1)	
		self.f5_GJ.Scale(.1)	
		
		self.h1_TT.Scale(.1)	
		self.h2_TT.Scale(.1)	
		self.h2_1_TT.Scale(.1)	
		self.h3_TT.Scale(.1)	
		self.h4_TT.Scale(.1)	
		self.h5_TT.Scale(.1)	
		self.h6_TT.Scale(.1)	
		self.h7_TT.Scale(.1)	
		self.h8_TT.Scale(.1)	
		self.h9_TT.Scale(.1)	
		self.p1_TT.Scale(.1)	
		self.p1_1_TT.Scale(.1)	
		self.p2_TT.Scale(.1)	
		self.p3_TT.Scale(.1)	
		self.p4_TT.Scale(.1)	
		self.p5_TT.Scale(.1)	
		self.f1_TT.Scale(.1)	
		self.f1_1_TT.Scale(.1)	
		self.f2_TT.Scale(.1)	
		self.f3_TT.Scale(.1)	
		self.f4_TT.Scale(.1)	
		self.f5_TT.Scale(.1)	


		FindAndSetMax(self.h1_sig10, self.h1_sig25, self.h1_sig50, self.h1_sig75, self.h1_WG, self.h1_ZG, self.h1_GJ, self.h1_TT, self.h1_Data)
		FindAndSetMax(self.h2_sig10, self.h2_sig25, self.h2_sig50, self.h2_sig75, self.h2_WG, self.h2_ZG, self.h2_GJ, self.h2_TT, self.h2_Data)
		FindAndSetMax(self.h4_sig10, self.h4_sig25, self.h4_sig50, self.h4_sig75, self.h4_WG, self.h4_ZG, self.h4_GJ, self.h4_TT, self.h4_Data)
		

		LUMI = 5.9 #Temporary luminosity with 10% of 2018 data
        	cmsextra = "Preliminary"

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		c1.SetLogy()
		self.h1_GJ.SetTitle("Softdrop Mass")
		self.h1_GJ.Draw("hist")
		self.h1_Data.Draw("same histe")
		self.h1_WG.Draw("same hist")
		self.h1_TT.Draw("same hist")
		self.h1_ZG.Draw("same hist")
		self.h1_sig10.Draw("same hist")
		self.h1_sig25.Draw("same hist")
		self.h1_sig50.Draw("same hist")
		self.h1_sig75.Draw("same hist")
		l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_Data, "10% of 2018 Data")
                l1.AddEntry(self.h1_GJ, "Gamma+Jet MC")
                l1.AddEntry(self.h1_TT, "TTBar MC")
                l1.AddEntry(self.h1_WG, "W+Gamma MC")
                l1.AddEntry(self.h1_ZG, "Z+Gamma MC")
		l1.AddEntry(self.h1_sig10, "Z' 10 GeV MC")
		l1.AddEntry(self.h1_sig25, "Z' 25 GeV MC")
		l1.AddEntry(self.h1_sig50, "Z' 50 GeV MC")
		l1.AddEntry(self.h1_sig75, "Z' 75 GeV MC")
                l1.Draw()
#		gPad.SetLogy()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c1.SaveAs("./plots/"+name+"_soft.png")
		c1.Close()
		

		c2 = TCanvas()
		c2.cd()
		c2.SetLogy()
		self.h2_GJ.SetTitle("Jet pT")
		self.h2_GJ.Draw("hist")
		self.h2_Data.Draw("same histe")
		self.h2_WG.Draw("same hist")
		self.h2_TT.Draw("same hist")
		self.h2_ZG.Draw("same hist")
		self.h2_sig10.Draw("same hist")
		self.h2_sig25.Draw("same hist")
		self.h2_sig50.Draw("same hist")
		self.h2_sig75.Draw("same hist")
		l2 = TLegend(.6, .75, .9, .9)
                l2.AddEntry(self.h2_Data, "10% of 2018 Data")
                l2.AddEntry(self.h2_GJ, "Gamma+Jet MC")
                l2.AddEntry(self.h2_TT, "TTBar MC")
                l2.AddEntry(self.h2_WG, "W+Gamma MC")
                l2.AddEntry(self.h2_ZG, "Z+Gamma MC")
		l2.AddEntry(self.h2_sig10, "Z' 10 GeV MC")
		l2.AddEntry(self.h2_sig25, "Z' 25 GeV MC")
		l2.AddEntry(self.h2_sig50, "Z' 50 GeV MC")
		l2.AddEntry(self.h2_sig75, "Z' 75 GeV MC")
                l2.Draw()
#		gPad.SetLogy()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c2.SaveAs("./plots/"+name+"_jet_pt.png")
		c2.Close()

		c3 = TCanvas()
		c3.cd()
		c3.SetLogy()
		self.h4_GJ.SetTitle("Photon pT")
		self.h4_GJ.Draw("hist")
		self.h4_Data.Draw("same histe")
		self.h4_WG.Draw("same hist")
		self.h4_TT.Draw("same hist")
		self.h4_ZG.Draw("same hist")
		self.h4_sig10.Draw("same hist")
		self.h4_sig25.Draw("same hist")
		self.h4_sig50.Draw("same hist")
		self.h4_sig75.Draw("same hist")
		l3 = TLegend(.6, .75, .9, .9)
                l3.AddEntry(self.h4_Data, "10% of 2018 Data")
                l3.AddEntry(self.h4_GJ, "Gamma+Jet MC")
                l3.AddEntry(self.h4_TT, "TTBar MC")
                l3.AddEntry(self.h4_WG, "W+Gamma MC")
                l3.AddEntry(self.h4_ZG, "Z+Gamma MC")
		l3.AddEntry(self.h4_sig10, "Z' 10 GeV MC")
		l3.AddEntry(self.h4_sig25, "Z' 25 GeV MC")
		l3.AddEntry(self.h4_sig50, "Z' 50 GeV MC")
		l3.AddEntry(self.h4_sig75, "Z' 75 GeV MC")
                l3.Draw()
#		gPad.SetLogy()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c3.SaveAs("./plots/"+name+"_photon_pt.png")
		c3.Close()

