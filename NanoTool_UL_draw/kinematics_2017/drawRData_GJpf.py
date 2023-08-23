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
	cheapline.GetYaxis().SetTitle("Pass/Fail")
	cheapline.GetYaxis().SetTitleSize(0.1)
	cheapline.GetYaxis().SetNdivisions(6)
	cheapline.GetYaxis().SetLabelSize(0.145)
	cheapline.GetYaxis().SetTitleOffset(0.275)
	cheapline.GetYaxis().CenterTitle(True)
	cheapline.GetYaxis().SetRangeUser(0.,1.5)
	GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
	cheapline.GetXaxis().SetTitleSize(0.1925)
	cheapline.GetXaxis().SetLabelSize(0.16)
	cheapline.GetXaxis().SetTitleOffset(0.84)
	return cheapline
	

class drawRData:
	def __init__(self, name, ifile1):
		gROOT.SetBatch(True)

		
		
		self.i = TFile.Open(ifile1, "READ")
		self.i.ls();

		self.h1_GJ = self.i.Get("softdrop")

		self.p1_GJ = self.i.Get("pass_soft")
		self.p1_1_GJ = self.i.Get("pass_soft_thin")
		self.f1_GJ = self.i.Get("fail_soft")
		self.f1_1_GJ = self.i.Get("fail_soft_thin")
		
		
		GoodPlotFormat(self.h1_GJ, 'thickline', kBlack)
		
		
		GoodPlotFormat(self.p1_GJ, 'thickline', kBlue)
		GoodPlotFormat(self.p1_1_GJ, 'thickline', kBlue)
		
		GoodPlotFormat(self.f1_GJ, 'thickline', kRed)
		GoodPlotFormat(self.f1_1_GJ, 'thickline', kRed)
		
		
		self.h1_GJ.SetYTitle("Events")	
		self.p1_GJ.SetYTitle("Events")	
		self.p1_1_GJ.SetYTitle("Events")	
		self.f1_GJ.SetYTitle("Events")	
		self.f1_1_GJ.SetYTitle("Events")	


		self.h1_GJ.Scale(.1)	
		self.p1_GJ.Scale(.1)	
		self.p1_1_GJ.Scale(.1)	
		self.f1_GJ.Scale(.1)	
		self.f1_1_GJ.Scale(.1)	
		
	
		#Scale Failing for 10% DDT
		self.f1_GJ.Scale(1.0/9.0)	
		self.f1_1_GJ.Scale(1.0/9.0)	
	
		
		FindAndSetMax(self.p1_GJ, self.f1_GJ)
		FindAndSetMax(self.p1_1_GJ, self.f1_1_GJ)

		LUMI = 4.148 #Temporary luminosity with 10% of 2017 data
        	cmsextra = "Preliminary"

		ROOT.gStyle.SetOptStat(0)

		c1_p = TCanvas()
		c1_p.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
#		p12.SetLogy()
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.p1_GJ.SetTitle("Softdrop Mass")
		self.p1_GJ.Draw("hist")
		self.f1_GJ.Draw("same hist")
		l1_p = TLegend(.5, .6, .89, .89)
		l1_p.SetFillColor(0)
		l1_p.SetLineColor(0)
                l1_p.AddEntry(self.p1_GJ, "GJets Passing Softdrop Mass")
                l1_p.AddEntry(self.f1_GJ, "GJets Failing Softdrop Mass")
                l1_p.Draw()
#		gPad.SetLogy()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		p22.cd() #bottom
		cheap1_p = makeCheap(self.p1_GJ)
		cheap1_p.Draw("hist")
		pull1_p = makePull(self.p1_GJ, self.f1_GJ)
		pull1_p.Draw("esame")
		p22.RedrawAxis()
		c1_p.SaveAs("./plots/"+name+"_soft.png")
		c1_p.Close()
		
		c1_p_thin = TCanvas()
		c1_p_thin.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
#		p12.SetLogy()
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.p1_1_GJ.SetTitle("Softdrop Mass")
		self.p1_1_GJ.Draw("hist")
		self.f1_1_GJ.Draw("same hist")
		l1_1_p = TLegend(.5, .6, .89, .89)
		l1_1_p.SetFillColor(0)
		l1_1_p.SetLineColor(0)
                l1_1_p.AddEntry(self.p1_1_GJ, "GJets Passing Softdrop Mass")
                l1_1_p.AddEntry(self.f1_1_GJ, "GJets Failing Softdrop Mass")
                l1_1_p.Draw()
#		gPad.SetLogy()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		p22.cd() #bottom
		cheap1_p = makeCheap(self.p1_1_GJ)
		cheap1_p.Draw("hist")
		pull1_1_p = makePull(self.p1_1_GJ, self.f1_1_GJ)
		pull1_1_p.Draw("esame")
		p22.RedrawAxis()
		c1_p_thin.SaveAs("./plots/"+name+"_soft_thin.png")
		c1_p_thin.Close()

