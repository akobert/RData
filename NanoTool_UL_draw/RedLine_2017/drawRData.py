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


def redLine(line, hist, p):
        for i in range(1, hist.GetNbinsX()+1):
                tot = 0
                for j in range(1, hist.GetNbinsY()+1):
                        tot += hist.GetBinContent(i, j)
                if tot != 0:
                        part = 0
                        for k in range(1, hist.GetNbinsY()+1):
                                part += hist.GetBinContent(i, k)
                                if (part/tot) > p:
                                        line.SetBinContent(i, (k*.01)-0.5) #.02 is n2ddt bin width

#					print((k*.01)-0.5)
                                        break
                else:
                        line.SetBinContent(i, -0.5)	


class drawRData:
	def __init__(self, name, ifile1, ifile2, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/RedLine/"+o,"RECREATE")
		
		self.i = TFile.Open(ifile1, "READ")
		self.i.ls();

		self.h1_GJ = self.i.Get("soft_n2ddt")
		self.h2_GJ = self.i.Get("pt_n2ddt")
		
		self.k = TFile.Open(ifile2, "READ")
		self.k.ls();

		self.h1_Data = self.k.Get("soft_n2ddt")
		self.h2_Data = self.k.Get("pt_n2ddt")


		self.softline_GJ_10 = TH1F("softline_GJ_10", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_10 = TH1F("ptline_GJ_10", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_20 = TH1F("softline_GJ_20", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_20 = TH1F("ptline_GJ_20", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_30 = TH1F("softline_GJ_30", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_30 = TH1F("ptline_GJ_30", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_40 = TH1F("softline_GJ_40", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_40 = TH1F("ptline_GJ_40", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_50 = TH1F("softline_GJ_50", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_50 = TH1F("ptline_GJ_50", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_60 = TH1F("softline_GJ_60", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_60 = TH1F("ptline_GJ_60", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_70 = TH1F("softline_GJ_70", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_70 = TH1F("ptline_GJ_70", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_80 = TH1F("softline_GJ_80", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_80 = TH1F("ptline_GJ_80", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		self.softline_GJ_90 = TH1F("softline_GJ_90", "", self.h1_GJ.GetNbinsX(), 0, 200)
		self.ptline_GJ_90 = TH1F("ptline_GJ_90", "", self.h2_GJ.GetNbinsX(), 0, 2000)
		
		self.softline_Data_10 = TH1F("softline_Data_10", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_10 = TH1F("ptline_Data_10", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_20 = TH1F("softline_Data_20", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_20 = TH1F("ptline_Data_20", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_30 = TH1F("softline_Data_30", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_30 = TH1F("ptline_Data_30", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_40 = TH1F("softline_Data_40", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_40 = TH1F("ptline_Data_40", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_50 = TH1F("softline_Data_50", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_50 = TH1F("ptline_Data_50", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_60 = TH1F("softline_Data_60", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_60 = TH1F("ptline_Data_60", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_70 = TH1F("softline_Data_70", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_70 = TH1F("ptline_Data_70", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_80 = TH1F("softline_Data_80", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_80 = TH1F("ptline_Data_80", "", self.h2_Data.GetNbinsX(), 0, 2000)
		self.softline_Data_90 = TH1F("softline_Data_90", "", self.h1_Data.GetNbinsX(), 0, 200)
		self.ptline_Data_90 = TH1F("ptline_Data_90", "", self.h2_Data.GetNbinsX(), 0, 2000)

		redLine(self.softline_GJ_10, self.h1_GJ, .1)
		redLine(self.ptline_GJ_10, self.h2_GJ, .1)
		redLine(self.softline_GJ_20, self.h1_GJ, .2)
		redLine(self.ptline_GJ_20, self.h2_GJ, .2)
		redLine(self.softline_GJ_30, self.h1_GJ, .3)
		redLine(self.ptline_GJ_30, self.h2_GJ, .3)
		redLine(self.softline_GJ_40, self.h1_GJ, .4)
		redLine(self.ptline_GJ_40, self.h2_GJ, .4)
		redLine(self.softline_GJ_50, self.h1_GJ, .5)
		redLine(self.ptline_GJ_50, self.h2_GJ, .5)
		redLine(self.softline_GJ_60, self.h1_GJ, .6)
		redLine(self.ptline_GJ_60, self.h2_GJ, .6)
		redLine(self.softline_GJ_70, self.h1_GJ, .7)
		redLine(self.ptline_GJ_70, self.h2_GJ, .7)
		redLine(self.softline_GJ_80, self.h1_GJ, .8)
		redLine(self.ptline_GJ_80, self.h2_GJ, .8)
		redLine(self.softline_GJ_90, self.h1_GJ, .9)
		redLine(self.ptline_GJ_90, self.h2_GJ, .9)
		
		redLine(self.softline_Data_10, self.h1_Data, .1)
		redLine(self.ptline_Data_10, self.h2_Data, .1)
		redLine(self.softline_Data_20, self.h1_Data, .2)
		redLine(self.ptline_Data_20, self.h2_Data, .2)
		redLine(self.softline_Data_30, self.h1_Data, .3)
		redLine(self.ptline_Data_30, self.h2_Data, .3)
		redLine(self.softline_Data_40, self.h1_Data, .4)
		redLine(self.ptline_Data_40, self.h2_Data, .4)
		redLine(self.softline_Data_50, self.h1_Data, .5)
		redLine(self.ptline_Data_50, self.h2_Data, .5)
		redLine(self.softline_Data_60, self.h1_Data, .6)
		redLine(self.ptline_Data_60, self.h2_Data, .6)
		redLine(self.softline_Data_70, self.h1_Data, .7)
		redLine(self.ptline_Data_70, self.h2_Data, .7)
		redLine(self.softline_Data_80, self.h1_Data, .8)
		redLine(self.ptline_Data_80, self.h2_Data, .8)
		redLine(self.softline_Data_90, self.h1_Data, .9)
		redLine(self.ptline_Data_90, self.h2_Data, .9)

		self.softline_GJ_10.SetLineColor(kRed)
		self.ptline_GJ_10.SetLineColor(kRed)
		self.softline_GJ_20.SetLineColor(kRed)
		self.ptline_GJ_20.SetLineColor(kRed)
		self.softline_GJ_30.SetLineColor(kRed)
		self.ptline_GJ_30.SetLineColor(kRed)
		self.softline_GJ_40.SetLineColor(kRed)
		self.ptline_GJ_40.SetLineColor(kRed)
		self.softline_GJ_50.SetLineColor(kRed)
		self.ptline_GJ_50.SetLineColor(kRed)
		self.softline_GJ_60.SetLineColor(kRed)
		self.ptline_GJ_60.SetLineColor(kRed)
		self.softline_GJ_70.SetLineColor(kRed)
		self.ptline_GJ_70.SetLineColor(kRed)
		self.softline_GJ_80.SetLineColor(kRed)
		self.ptline_GJ_80.SetLineColor(kRed)
		self.softline_GJ_90.SetLineColor(kRed)
		self.ptline_GJ_90.SetLineColor(kRed)
		
		self.softline_Data_10.SetLineColor(kRed)
		self.ptline_Data_10.SetLineColor(kRed)
		self.softline_Data_20.SetLineColor(kRed)
		self.ptline_Data_20.SetLineColor(kRed)
		self.softline_Data_30.SetLineColor(kRed)
		self.ptline_Data_30.SetLineColor(kRed)
		self.softline_Data_40.SetLineColor(kRed)
		self.ptline_Data_40.SetLineColor(kRed)
		self.softline_Data_50.SetLineColor(kRed)
		self.ptline_Data_50.SetLineColor(kRed)
		self.softline_Data_60.SetLineColor(kRed)
		self.ptline_Data_60.SetLineColor(kRed)
		self.softline_Data_70.SetLineColor(kRed)
		self.ptline_Data_70.SetLineColor(kRed)
		self.softline_Data_80.SetLineColor(kRed)
		self.ptline_Data_80.SetLineColor(kRed)
		self.softline_Data_90.SetLineColor(kRed)
		self.ptline_Data_90.SetLineColor(kRed)
		
		self.h1_GJ.GetYaxis().SetRangeUser(-0.3, 0.3)
		self.h2_GJ.GetYaxis().SetRangeUser(-0.3, 0.3)
		self.h1_Data.GetYaxis().SetRangeUser(-0.3, 0.3)
		self.h2_Data.GetYaxis().SetRangeUser(-0.3, 0.3)
		
		self.h2_GJ.GetXaxis().SetRangeUser(100, 800)
		self.h2_Data.GetXaxis().SetRangeUser(100, 800)
	
		self.h1_GJ.SetXTitle("Softdrop Mass")	
		self.h1_GJ.SetYTitle("N2DDT")	
		self.h2_GJ.SetXTitle("Jet pT")	
		self.h2_GJ.SetYTitle("N2DDT")	
		
		self.h1_Data.SetXTitle("Softdrop Mass")	
		self.h1_Data.SetYTitle("N2DDT")	
		self.h2_Data.SetXTitle("Jet pT")	
		self.h2_Data.SetYTitle("N2DDT")	
		
		LUMI = 5.9 #Temporary luminosity with 10% of 2018 data
        	cmsextra = "Preliminary"

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.h1_GJ.SetTitle("Softdrop Mass vs. N2DDT")
		self.h1_GJ.Draw("COLZ")
		self.softline_GJ_10.Draw("same hist")
		self.softline_GJ_20.Draw("same hist")
		self.softline_GJ_30.Draw("same hist")
		self.softline_GJ_40.Draw("same hist")
		self.softline_GJ_50.Draw("same hist")
		self.softline_GJ_60.Draw("same hist")
		self.softline_GJ_70.Draw("same hist")
		self.softline_GJ_80.Draw("same hist")
		self.softline_GJ_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c1.SaveAs("./plots/soft_n2ddt_redline_GJ.png")
		c1.Close()
		

		c2 = TCanvas()
		c2.cd()
		self.h2_GJ.SetTitle("Jet pT vs. N2DDT")
		self.h2_GJ.Draw("COLZ")
		self.ptline_GJ_10.Draw("same hist")
		self.ptline_GJ_20.Draw("same hist")
		self.ptline_GJ_30.Draw("same hist")
		self.ptline_GJ_40.Draw("same hist")
		self.ptline_GJ_50.Draw("same hist")
		self.ptline_GJ_60.Draw("same hist")
		self.ptline_GJ_70.Draw("same hist")
		self.ptline_GJ_80.Draw("same hist")
		self.ptline_GJ_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c2.SaveAs("./plots/pt_n2ddt_redline_GJ.png")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.h1_Data.SetTitle("Softdrop Mass vs. N2DDT")
		self.h1_Data.Draw("COLZ")
		self.softline_Data_10.Draw("same hist")
		self.softline_Data_20.Draw("same hist")
		self.softline_Data_30.Draw("same hist")
		self.softline_Data_40.Draw("same hist")
		self.softline_Data_50.Draw("same hist")
		self.softline_Data_60.Draw("same hist")
		self.softline_Data_70.Draw("same hist")
		self.softline_Data_80.Draw("same hist")
		self.softline_Data_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c3.SaveAs("./plots/soft_n2ddt_redline_Data.png")
		c3.Close()
		

		c4 = TCanvas()
		c4.cd()
		self.h2_Data.SetTitle("Jet pT vs. N2DDT")
		self.h2_Data.Draw("COLZ")
		self.ptline_Data_10.Draw("same hist")
		self.ptline_Data_20.Draw("same hist")
		self.ptline_Data_30.Draw("same hist")
		self.ptline_Data_40.Draw("same hist")
		self.ptline_Data_50.Draw("same hist")
		self.ptline_Data_60.Draw("same hist")
		self.ptline_Data_70.Draw("same hist")
		self.ptline_Data_80.Draw("same hist")
		self.ptline_Data_90.Draw("same hist")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c4.SaveAs("./plots/pt_n2ddt_redline_Data.png")
		c4.Close()


