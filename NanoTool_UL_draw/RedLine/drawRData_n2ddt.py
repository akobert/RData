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

def normalize(hist):
	tot = hist.Integral()
	hist.Scale(1.0/tot)	
	return

class drawRData:
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, ifile9, ifile10, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/RedLine/"+o,"RECREATE")
		
		self.i = TFile.Open(ifile1, "READ")
		self.i.ls();
		self.h1 = self.i.Get("n2ddt")
		self.j = TFile.Open(ifile2, "READ")
		self.j.ls();
		self.h2 = self.j.Get("n2ddt")
		self.k = TFile.Open(ifile3, "READ")
		self.k.ls();
		self.h3 = self.k.Get("n2ddt")
		self.l = TFile.Open(ifile4, "READ")
		self.l.ls();
		self.h4 = self.l.Get("n2ddt")
		self.m = TFile.Open(ifile5, "READ")
		self.m.ls();
		self.h5 = self.m.Get("n2ddt")
		self.n = TFile.Open(ifile6, "READ")
		self.n.ls();
		self.h6 = self.n.Get("n2ddt")
		self.p = TFile.Open(ifile7, "READ")
		self.p.ls();
		self.h7 = self.p.Get("n2ddt")
		self.q = TFile.Open(ifile8, "READ")
		self.q.ls();
		self.h8 = self.q.Get("n2ddt")
		self.r = TFile.Open(ifile9, "READ")
		self.r.ls();
		self.h9 = self.r.Get("n2ddt")
		self.s = TFile.Open(ifile10, "READ")
		self.s.ls();
		self.h10 = self.s.Get("n2ddt")

		normalize(self.h1)
		normalize(self.h2)
		normalize(self.h3)
		normalize(self.h4)
		normalize(self.h5)
		normalize(self.h6)
		normalize(self.h7)
		normalize(self.h8)
		normalize(self.h9)
		normalize(self.h10)

		self.h1.SetLineColor(kBlue)
		self.h2.SetLineColor(kBlack)
		self.h3.SetLineColor(kRed)
		self.h4.SetLineColor(kGreen)
		self.h5.SetLineColor(kYellow)
		self.h6.SetLineColor(kOrange)
		self.h7.SetLineColor(kGray)
		self.h8.SetLineColor(kCyan)
		self.h9.SetLineColor(kViolet)
		self.h10.SetLineColor(kPink)
		
	
		
		LUMI = 5.9 #Temporary luminosity with 10% of 2018 data
        	cmsextra = "Preliminary"

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.h1.SetTitle("N2DDT")
		self.h1.Draw("hist")
		self.h2.Draw("same hist")
		self.h3.Draw("same hist")
		self.h4.Draw("same hist")
		self.h5.Draw("same hist")
		self.h6.Draw("same hist")
		self.h7.Draw("same hist")
		self.h8.Draw("same hist")
		self.h9.Draw("same hist")
		self.h10.Draw("same hist")
		l1 = TLegend(.68, .53, .89, .89)
		l1.SetFillColor(0)
                l1.SetLineColor(0)
		l1.AddEntry(self.h1, "GJets")
		l1.AddEntry(self.h2, "Data")
		l1.AddEntry(self.h3, "M10")
		l1.AddEntry(self.h4, "M20")
		l1.AddEntry(self.h5, "M25")
		l1.AddEntry(self.h6, "M50")
		l1.AddEntry(self.h7, "M75")
		l1.AddEntry(self.h8, "M100")
		l1.AddEntry(self.h9, "M125")
		l1.AddEntry(self.h10, "M150")
		l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		c1.SaveAs("./plots/n2ddt_all.png")
		c1.Close()
		
