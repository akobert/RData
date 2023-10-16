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
        latex.DrawLatex(0.1265, 1-t+lumiTextOffset*t, cmsText)
        pad.Update()

def makePull(data, bkg):
	pull = data.Clone("pull")
	pull.Divide(bkg)
	GoodPlotFormat(pull, "markers", ROOT.kBlack, 20)
	return pull

def makeCheap(data):
	cheapline = data.Clone("cheapline")
	cheapline.Divide(data)
	for i in range(1, cheapline.GetNbinsX()+1):
		cheapline.SetBinContent(i,1)
	cheapline.SetTitle("")
	cheapline.GetYaxis().SetTitle("Data/Total Background")
	cheapline.GetYaxis().SetTitleSize(0.08)
	cheapline.GetYaxis().SetNdivisions(6)
	cheapline.GetYaxis().SetLabelSize(0.145)
	cheapline.GetYaxis().SetTitleOffset(0.33)
	cheapline.GetYaxis().CenterTitle(True)
	cheapline.GetYaxis().SetRangeUser(0.,3.)
	GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
	cheapline.GetXaxis().SetTitleSize(0.1)
	cheapline.GetXaxis().SetLabelSize(0.16)
	cheapline.GetXaxis().SetTitleOffset(1.2)
	return cheapline
	

#Gaussian Function Fit
def fitf(x, par):
	fitval = par[0]*exp(-pow((x[0]-par[2]), 2)/(2*pow(par[1], 2)))

	return fitval

class drawRData:
	def __init__(self, name, ifile1, ifile2, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/Wpeak_2017/"+o,"RECREATE")
		
		self.c = TFile.Open(ifile1, "READ")
		self.c.ls();

		self.h1_Data = self.c.Get("softdrop")
		self.h2_Data = self.c.Get("thin_softdrop")
		self.h2_1_Data = self.c.Get("thin_uncorr_softdrop")
		self.h5_Data = self.c.Get("rho")
		self.h6_Data = self.c.Get("muon_pt_thin")
		
		self.h8_Data = self.c.Get("PuppiMETPT")
		self.h9_Data = self.c.Get("METplusMUON")
		

		self.p1_Data = self.c.Get("pass_soft")
		self.p2_Data = self.c.Get("pass_soft_thin")
		self.p2_1_Data = self.c.Get("pass_soft_uncorr_thin")
		

		GoodPlotFormat(self.h1_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h2_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h2_1_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h5_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h6_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h8_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.h9_Data, 'thickline', ROOT.kBlack)
		
		GoodPlotFormat(self.p1_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.p2_Data, 'thickline', ROOT.kBlack)
		GoodPlotFormat(self.p2_1_Data, 'thickline', ROOT.kBlack)
		

		self.d = TFile.Open(ifile2, "READ")
		self.d.ls();
		
		self.h1_TTBar = self.d.Get("softdrop")
		self.h2_TTBar = self.d.Get("thin_softdrop")
		self.h2_1_TTBar = self.d.Get("thin_uncorr_softdrop")
		self.h5_TTBar = self.d.Get("rho")
		self.h6_TTBar = self.d.Get("muon_pt_thin")
		
		self.h8_TTBar = self.d.Get("PuppiMETPT")
		self.h9_TTBar = self.d.Get("METplusMUON")
		

		self.p1_TTBar = self.d.Get("pass_soft")
		self.p2_TTBar = self.d.Get("pass_soft_thin")
		self.p2_1_TTBar = self.d.Get("pass_soft_uncorr_thin")
		

		GoodPlotFormat(self.h1_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h2_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h2_1_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h5_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h6_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h8_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.h9_TTBar, 'thickline', ROOT.kGreen)
		
		GoodPlotFormat(self.p1_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.p2_TTBar, 'thickline', ROOT.kGreen)
		GoodPlotFormat(self.p2_1_TTBar, 'thickline', ROOT.kGreen)

		


		FindAndSetMax(self.h1_Data, self.h1_TTBar)
		FindAndSetMax(self.p1_Data, self.p1_TTBar)
		FindAndSetMax(self.h2_Data, self.h2_TTBar)
		FindAndSetMax(self.p2_Data, self.p2_TTBar)
		

		LUMI = 41.84 
        	cmsextra = "Preliminary"
		
		#Plots
		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
#		c1.SetLogy()
		self.h1_Data.SetTitle("Softdrop Mass")
		self.h1_Data.Draw("hist")
		self.h1_TTBar.Draw("same hist")
		l1 = TLegend(.53, .68, .89, .89)
		l1.SetFillColor(0)
		l1.SetLineColor(0)
                l1.AddEntry(self.h1_Data, "SingleMuon 2017 Data")
                l1.AddEntry(self.h1_TTBar, "TTBar (Truth Matched)")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c1.SaveAs("./plots/"+name+"_soft.png")
#		c1.SaveAs("./plots/"+name+"_soft.root")
		c1.Close()
		
		c1_p = TCanvas()
		c1_p.cd()
#		c1_p.SetLogy()
		self.p1_Data.SetTitle("Softdrop Mass")
		self.p1_Data.Draw("hist")
		self.p1_TTBar.Draw("same hist")
		l1_p = TLegend(.53, .68, .89, .89)
		l1_p.SetFillColor(0)
		l1_p.SetLineColor(0)
                l1_p.AddEntry(self.p1_Data, "SingleMuon 2017 Data")
                l1_p.AddEntry(self.p1_TTBar, "TTBar (Truth Matched)")
                l1_p.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c1_p.SaveAs("./plots/"+name+"_pass_soft.png")
#		c1_p.SaveAs("./plots/"+name+"_pass_soft.root")
		c1_p.Close()
		
		c2 = TCanvas()
		c2.cd()
#		c2.SetLogy()
		self.h2_Data.SetTitle("Softdrop Mass")
		self.h2_Data.Draw("hist")
		self.h2_TTBar.Draw("same hist")
		l2 = TLegend(.53, .68, .89, .89)
		l2.SetFillColor(0)
		l2.SetLineColor(0)
                l2.AddEntry(self.h2_Data, "SingleMuon 2017 Data")
                l2.AddEntry(self.h2_TTBar, "TTBar (Truth Matched)")
                l2.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c2.SaveAs("./plots/"+name+"_thin_soft.png")
#		c2.SaveAs("./plots/"+name+"_thin_soft.root")
		c2.Close()
		
		c2_p = TCanvas()
		c2_p.cd()
#		c2_p.SetLogy()
		self.p2_Data.SetTitle("Passing Softdrop Mass")
		self.p2_Data.Draw("hist")
		self.p2_TTBar.Draw("same hist")
		l2_p = TLegend(.53, .68, .89, .89)
		l2_p.SetFillColor(0)
		l2_p.SetLineColor(0)
                l2_p.AddEntry(self.p2_Data, "SingleMuon 2017 Data")
                l2_p.AddEntry(self.p2_TTBar, "TTBar (Truth Matched)")
                l2_p.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c2_p.SaveAs("./plots/"+name+"_thin_pass_soft.png")
#		c2_p.SaveAs("./plots/"+name+"_thin_pass_soft.root")
		c2_p.Close()
		
		FindAndSetMax(self.h2_Data, self.h2_1_Data)
		FindAndSetMax(self.h2_TTBar, self.h2_1_TTBar)
		FindAndSetMax(self.p2_Data, self.p2_1_Data)
		FindAndSetMax(self.p2_TTBar, self.p2_1_TTBar)

		GoodPlotFormat(self.h2_Data, 'thickline', ROOT.kBlue)
		GoodPlotFormat(self.h2_1_Data, 'thickline', ROOT.kRed)
		GoodPlotFormat(self.h2_TTBar, 'thickline', ROOT.kBlue)
		GoodPlotFormat(self.h2_1_TTBar, 'thickline', ROOT.kRed)
		
		GoodPlotFormat(self.p2_Data, 'thickline', ROOT.kBlue)
		GoodPlotFormat(self.p2_1_Data, 'thickline', ROOT.kRed)
		GoodPlotFormat(self.p2_TTBar, 'thickline', ROOT.kBlue)
		GoodPlotFormat(self.p2_1_TTBar, 'thickline', ROOT.kRed)
		

		c2_1_TTBar = TCanvas()
		c2_1_TTBar.cd()
#		c2_1_TTBar.SetLogy()
		self.h2_TTBar.SetTitle("Softdrop Mass")
		self.h2_TTBar.Draw("hist")
		self.h2_1_TTBar.Draw("same hist")
		l2_1_TTBar = TLegend(.53, .68, .89, .89)
		l2_1_TTBar.SetFillColor(0)
		l2_1_TTBar.SetLineColor(0)
                l2_1_TTBar.AddEntry(self.h2_TTBar, "TTBar Corrected (Truth Matched)")
                l2_1_TTBar.AddEntry(self.h2_1_TTBar, "TTBar Uncorrected (Truth Matched)")
                l2_1_TTBar.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c2_1_TTBar.SaveAs("./plots/"+name+"_thin_soft_TTBar.png")
#		c2_1_TTBar.SaveAs("./plots/"+name+"_thin_soft_TTBar.root")
		c2_1_TTBar.Close()
		

		c2_1_p_TTBar = TCanvas()
		c2_1_p_TTBar.cd()
#		c2_1_p_TTBar.SetLogy()
		self.p2_TTBar.SetTitle("Passing Softdrop Mass")
		self.p2_TTBar.Draw("hist")
		self.p2_1_TTBar.Draw("same hist")
		l2_1_p_TTBar = TLegend(.53, .68, .89, .89)
		l2_1_p_TTBar.SetFillColor(0)
		l2_1_p_TTBar.SetLineColor(0)
                l2_1_p_TTBar.AddEntry(self.p2_TTBar, "TTBar Corrected (Truth Matched)")
                l2_1_p_TTBar.AddEntry(self.p2_1_TTBar, "TTBar Uncorrected (Truth Matched)")
                l2_1_p_TTBar.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		wmass.SetLineColor(kViolet)
		wmass.SetLineWidth(2)
		wmass.Draw("same")
		c2_1_p_TTBar.SaveAs("./plots/"+name+"_thin_pass_soft_TTBar.png")
#		c2_1_p_TTBar.SaveAs("./plots/"+name+"_thin_pass_soft_TTBar.root")
		c2_1_p_TTBar.Close()
		
		
		FindAndSetMax(self.h8_Data, self.h8_TTBar)
		FindAndSetMax(self.h9_Data, self.h9_TTBar)
		
		c8 = TCanvas()
		c8.cd()
#		c8.SetLogy()
		self.h8_Data.SetTitle("Puppi MET pT")
		self.h8_Data.Draw("hist")
		self.h8_TTBar.Draw("same hist")
		l8 = TLegend(.53, .68, .89, .89)
		l8.SetFillColor(0)
		l8.SetLineColor(0)
                l8.AddEntry(self.h8_Data, "SingleMuon 2017 Data")
                l8.AddEntry(self.h8_TTBar, "TTBar (Truth Matched)")
                l8.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c8.SaveAs("./plots/"+name+"_MET.png")
#		c8.SaveAs("./plots/"+name+"_MET.root")
		c8.Close()
		
		c9 = TCanvas()
		c9.cd()
#		c9.SetLogy()
		self.h9_Data.SetTitle("Puppi MET pT + Muon pT")
		self.h9_Data.Draw("hist")
		self.h9_TTBar.Draw("same hist")
		l9 = TLegend(.53, .68, .89, .89)
		l9.SetFillColor(0)
		l9.SetLineColor(0)
                l9.AddEntry(self.h9_Data, "SingleMuon 2017 Data")
                l9.AddEntry(self.h9_TTBar, "TTBar (Truth Matched)")
                l9.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c9.SaveAs("./plots/"+name+"_METplusMuon.png")
#		c9.SaveAs("./plots/"+name+"_METplusMuon.root")
		c9.Close()

