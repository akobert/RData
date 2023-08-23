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
	cheapline.GetYaxis().SetTitle("Data/Total Background")
	cheapline.GetYaxis().SetTitleSize(0.1)
	cheapline.GetYaxis().SetNdivisions(6)
	cheapline.GetYaxis().SetLabelSize(0.145)
	cheapline.GetYaxis().SetTitleOffset(0.275)
	cheapline.GetYaxis().CenterTitle(True)
	cheapline.GetYaxis().SetRangeUser(0.,3.)
	GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
	cheapline.GetXaxis().SetTitleSize(0.1925)
	cheapline.GetXaxis().SetLabelSize(0.16)
	cheapline.GetXaxis().SetTitleOffset(0.84)
	return cheapline


def redLine(line, hist, p, n2ddt=1): #n2ddt=1 means n2ddt, n2ddt=0 means n2
        for i in range(1, hist.GetNbinsX()+1):
                tot = 0
                for j in range(1, hist.GetNbinsY()+1):
                        tot += hist.GetBinContent(i, j)
                if tot != 0:
                        part = 0
                        for k in range(1, hist.GetNbinsY()+1):
                                part += hist.GetBinContent(i, k)
                                if (part/tot) > p:
					if n2ddt == 1:
                                        	line.SetBinContent(i, (k*.01)-0.5) #.01 is n2ddt bin width
					if n2ddt == 0:
                                        	line.SetBinContent(i, (k*.01))

                                        break
                else:
			if n2ddt == 1:
                        	line.SetBinContent(i, -0.5)	
			if n2ddt == 0:
                        	line.SetBinContent(i, 0.0)	


class drawRData:
	def __init__(self, name, ifile1, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/RedLine/"+o,"RECREATE")
		
		self.i = TFile.Open(ifile1, "READ")
		self.i.ls();

		self.h1 = self.i.Get("soft_n2ddt")
		self.h2 = self.i.Get("pt_n2ddt")
		
		self.h3 = self.i.Get("soft_n2")
		self.h4 = self.i.Get("pt_n2")


		self.softline_10 = TH1F("softline_10", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_10 = TH1F("ptline_10", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_20 = TH1F("softline_20", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_20 = TH1F("ptline_20", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_30 = TH1F("softline_30", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_30 = TH1F("ptline_30", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_40 = TH1F("softline_40", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_40 = TH1F("ptline_40", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_50 = TH1F("softline_50", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_50 = TH1F("ptline_50", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_60 = TH1F("softline_60", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_60 = TH1F("ptline_60", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_70 = TH1F("softline_70", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_70 = TH1F("ptline_70", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_80 = TH1F("softline_80", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_80 = TH1F("ptline_80", "", self.h2.GetNbinsX(), 0, 2000)
		self.softline_90 = TH1F("softline_90", "", self.h1.GetNbinsX(), 0, 200)
		self.ptline_90 = TH1F("ptline_90", "", self.h2.GetNbinsX(), 0, 2000)
		
		self.softline_10_n2 = TH1F("softline_10_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_10_n2 = TH1F("ptline_10_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_20_n2 = TH1F("softline_20_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_20_n2 = TH1F("ptline_20_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_30_n2 = TH1F("softline_30_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_30_n2 = TH1F("ptline_30_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_40_n2 = TH1F("softline_40_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_40_n2 = TH1F("ptline_40_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_50_n2 = TH1F("softline_50_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_50_n2 = TH1F("ptline_50_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_60_n2 = TH1F("softline_60_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_60_n2 = TH1F("ptline_60_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_70_n2 = TH1F("softline_70_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_70_n2 = TH1F("ptline_70_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_80_n2 = TH1F("softline_80_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_80_n2 = TH1F("ptline_80_n2", "", self.h4.GetNbinsX(), 0, 2000)
		self.softline_90_n2 = TH1F("softline_90_n2", "", self.h3.GetNbinsX(), 0, 200)
		self.ptline_90_n2 = TH1F("ptline_90_n2", "", self.h4.GetNbinsX(), 0, 2000)
		

		redLine(self.softline_10, self.h1, .1, 1)
		redLine(self.ptline_10, self.h2, .1, 1)
		redLine(self.softline_20, self.h1, .2, 1)
		redLine(self.ptline_20, self.h2, .2, 1)
		redLine(self.softline_30, self.h1, .3, 1)
		redLine(self.ptline_30, self.h2, .3, 1)
		redLine(self.softline_40, self.h1, .4, 1)
		redLine(self.ptline_40, self.h2, .4, 1)
		redLine(self.softline_50, self.h1, .5, 1)
		redLine(self.ptline_50, self.h2, .5, 1)
		redLine(self.softline_60, self.h1, .6, 1)
		redLine(self.ptline_60, self.h2, .6, 1)
		redLine(self.softline_70, self.h1, .7, 1)
		redLine(self.ptline_70, self.h2, .7, 1)
		redLine(self.softline_80, self.h1, .8, 1)
		redLine(self.ptline_80, self.h2, .8, 1)
		redLine(self.softline_90, self.h1, .9, 1)
		redLine(self.ptline_90, self.h2, .9, 1)
		
		redLine(self.softline_10_n2, self.h3, .1, 0)
		redLine(self.ptline_10_n2, self.h4, .1, 0)
		redLine(self.softline_20_n2, self.h3, .2, 0)
		redLine(self.ptline_20_n2, self.h4, .2, 0)
		redLine(self.softline_30_n2, self.h3, .3, 0)
		redLine(self.ptline_30_n2, self.h4, .3, 0)
		redLine(self.softline_40_n2, self.h3, .4, 0)
		redLine(self.ptline_40_n2, self.h4, .4, 0)
		redLine(self.softline_50_n2, self.h3, .5, 0)
		redLine(self.ptline_50_n2, self.h4, .5, 0)
		redLine(self.softline_60_n2, self.h3, .6, 0)
		redLine(self.ptline_60_n2, self.h4, .6, 0)
		redLine(self.softline_70_n2, self.h3, .7, 0)
		redLine(self.ptline_70_n2, self.h4, .7, 0)
		redLine(self.softline_80_n2, self.h3, .8, 0)
		redLine(self.ptline_80_n2, self.h4, .8, 0)
		redLine(self.softline_90_n2, self.h3, .9, 0)
		redLine(self.ptline_90_n2, self.h4, .9, 0)

		self.softline_10.SetLineColor(kRed)
		self.ptline_10.SetLineColor(kRed)
		self.softline_20.SetLineColor(kRed)
		self.ptline_20.SetLineColor(kRed)
		self.softline_30.SetLineColor(kRed)
		self.ptline_30.SetLineColor(kRed)
		self.softline_40.SetLineColor(kRed)
		self.ptline_40.SetLineColor(kRed)
		self.softline_50.SetLineColor(kRed)
		self.ptline_50.SetLineColor(kRed)
		self.softline_60.SetLineColor(kRed)
		self.ptline_60.SetLineColor(kRed)
		self.softline_70.SetLineColor(kRed)
		self.ptline_70.SetLineColor(kRed)
		self.softline_80.SetLineColor(kRed)
		self.ptline_80.SetLineColor(kRed)
		self.softline_90.SetLineColor(kRed)
		self.ptline_90.SetLineColor(kRed)
		
		self.softline_10_n2.SetLineColor(kRed)
		self.ptline_10_n2.SetLineColor(kRed)
		self.softline_20_n2.SetLineColor(kRed)
		self.ptline_20_n2.SetLineColor(kRed)
		self.softline_30_n2.SetLineColor(kRed)
		self.ptline_30_n2.SetLineColor(kRed)
		self.softline_40_n2.SetLineColor(kRed)
		self.ptline_40_n2.SetLineColor(kRed)
		self.softline_50_n2.SetLineColor(kRed)
		self.ptline_50_n2.SetLineColor(kRed)
		self.softline_60_n2.SetLineColor(kRed)
		self.ptline_60_n2.SetLineColor(kRed)
		self.softline_70_n2.SetLineColor(kRed)
		self.ptline_70_n2.SetLineColor(kRed)
		self.softline_80_n2.SetLineColor(kRed)
		self.ptline_80_n2.SetLineColor(kRed)
		self.softline_90_n2.SetLineColor(kRed)
		self.ptline_90_n2.SetLineColor(kRed)
		
		
		self.h1.GetYaxis().SetRangeUser(-0.3, 0.3)
		self.h2.GetYaxis().SetRangeUser(-0.3, 0.3)
		
		self.h3.GetYaxis().SetRangeUser(0, 0.5)
		self.h4.GetYaxis().SetRangeUser(0, 0.5)
		
		self.h2.GetXaxis().SetRangeUser(100, 800)
		self.h4.GetXaxis().SetRangeUser(100, 800)
	
		self.h1.SetXTitle("Softdrop Mass")	
		self.h1.SetYTitle("N2DDT")	
		self.h2.SetXTitle("Jet pT")	
		self.h2.SetYTitle("N2DDT")	
		
		self.h3.SetXTitle("Softdrop Mass")	
		self.h3.SetYTitle("N2")	
		self.h4.SetXTitle("Jet pT")	
		self.h4.SetYTitle("N2")	
		
		
		LUMI = 5.9 #Temporary luminosity with 10% of 2018 data
        	cmsextra = "Preliminary"

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.h1.SetTitle("Softdrop Mass vs. N2DDT")
		self.h1.Draw("COLZ")
		self.softline_10.Draw("same hist")
		self.softline_20.Draw("same hist")
		self.softline_30.Draw("same hist")
		self.softline_40.Draw("same hist")
		self.softline_50.Draw("same hist")
		self.softline_60.Draw("same hist")
		self.softline_70.Draw("same hist")
		self.softline_80.Draw("same hist")
		self.softline_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c1.SaveAs("./plots/soft_n2ddt_redline_"+name+".png")
		c1.Close()
		

		c2 = TCanvas()
		c2.cd()
		self.h2.SetTitle("Jet pT vs. N2DDT")
		self.h2.Draw("COLZ")
		self.ptline_10.Draw("same hist")
		self.ptline_20.Draw("same hist")
		self.ptline_30.Draw("same hist")
		self.ptline_40.Draw("same hist")
		self.ptline_50.Draw("same hist")
		self.ptline_60.Draw("same hist")
		self.ptline_70.Draw("same hist")
		self.ptline_80.Draw("same hist")
		self.ptline_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c2.SaveAs("./plots/pt_n2ddt_redline_"+name+".png")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.h3.SetTitle("Softdrop Mass vs. N2")
		self.h3.Draw("COLZ")
		self.softline_10_n2.Draw("same hist")
		self.softline_20_n2.Draw("same hist")
		self.softline_30_n2.Draw("same hist")
		self.softline_40_n2.Draw("same hist")
		self.softline_50_n2.Draw("same hist")
		self.softline_60_n2.Draw("same hist")
		self.softline_70_n2.Draw("same hist")
		self.softline_80_n2.Draw("same hist")
		self.softline_90_n2.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c3.SaveAs("./plots/soft_n2_redline_"+name+".png")
		c3.Close()
		

		c4 = TCanvas()
		c4.cd()
		self.h4.SetTitle("Jet pT vs. N2")
		self.h4.Draw("COLZ")
		self.ptline_10_n2.Draw("same hist")
		self.ptline_20_n2.Draw("same hist")
		self.ptline_30_n2.Draw("same hist")
		self.ptline_40_n2.Draw("same hist")
		self.ptline_50_n2.Draw("same hist")
		self.ptline_60_n2.Draw("same hist")
		self.ptline_70_n2.Draw("same hist")
		self.ptline_80_n2.Draw("same hist")
		self.ptline_90_n2.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c4.SaveAs("./plots/pt_n2_redline_"+name+".png")
		c4.Close()

