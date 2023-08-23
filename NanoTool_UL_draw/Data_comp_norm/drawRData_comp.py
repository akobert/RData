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

def norm(H):
	factor = H.Integral()
	H.Scale(1.0/factor)
	return

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
	cheapline.GetYaxis().SetTitle("2017/2018")
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
	def __init__(self, name, ifile1, ifile2):
		gROOT.SetBatch(True)

		self.i = TFile.Open(ifile1, "READ")
		self.i.ls();

		self.h1_2017 = self.i.Get("softdrop")
		self.h2_2017 = self.i.Get("thin_softdrop")
		self.h3_2017 = self.i.Get("jet_pt")
		self.h4_2017 = self.i.Get("thin_jet_pt")
		self.h5_2017 = self.i.Get("nPV")
		self.h6_2017 = self.i.Get("nPV_good")
		self.h7_2017 = self.i.Get("HT")
		self.h8_2017 = self.i.Get("HT_AK8")
		
		GoodPlotFormat(self.h1_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h2_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h3_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h4_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h5_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h6_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h7_2017, 'thickline', kBlue)
		GoodPlotFormat(self.h8_2017, 'thickline', kBlue)
		
		self.h1_2017.SetYTitle("Events")	
		self.h2_2017.SetYTitle("Events")	
		self.h3_2017.SetYTitle("Events")	
		self.h4_2017.SetYTitle("Events")	
		self.h5_2017.SetYTitle("Events")	
		self.h6_2017.SetYTitle("Events")	
		self.h7_2017.SetYTitle("Events")	
		self.h8_2017.SetYTitle("Events")	
		
		norm(self.h1_2017)
		norm(self.h2_2017)
		norm(self.h3_2017)
		norm(self.h4_2017)
		norm(self.h5_2017)
		norm(self.h6_2017)
		norm(self.h7_2017)
		norm(self.h8_2017)

		self.j = TFile.Open(ifile2, "READ")
		self.j.ls();

		self.h1_2018 = self.j.Get("softdrop")
		self.h2_2018 = self.j.Get("thin_softdrop")
		self.h3_2018 = self.j.Get("jet_pt")
		self.h4_2018 = self.j.Get("thin_jet_pt")
		self.h5_2018 = self.j.Get("nPV")
		self.h6_2018 = self.j.Get("nPV_good")
		self.h7_2018 = self.j.Get("HT")
		self.h8_2018 = self.j.Get("HT_AK8")
		
		GoodPlotFormat(self.h1_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h2_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h3_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h4_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h5_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h6_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h7_2018, 'thickline', kGreen)
		GoodPlotFormat(self.h8_2018, 'thickline', kGreen)
		
		norm(self.h1_2018)
		norm(self.h2_2018)
		norm(self.h3_2018)
		norm(self.h4_2018)
		norm(self.h5_2018)
		norm(self.h6_2018)
		norm(self.h7_2018)
		norm(self.h8_2018)
		
		FindAndSetMax(self.h1_2017, self.h1_2018)
		FindAndSetMax(self.h2_2017, self.h2_2018)
		FindAndSetMax(self.h3_2017, self.h3_2018)
		FindAndSetMax(self.h4_2017, self.h4_2018)
		FindAndSetMax(self.h5_2017, self.h5_2018)
		FindAndSetMax(self.h6_2017, self.h6_2018)
		FindAndSetMax(self.h7_2017, self.h7_2018)
		FindAndSetMax(self.h8_2017, self.h8_2018)


		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h1_2017.SetTitle("Softdrop Mass")
		self.h1_2017.Draw("hist")
		self.h1_2018.Draw("same hist")
		l1 = TLegend(.5, .6, .89, .89)
		l1.SetFillColor(0)
		l1.SetLineColor(0)
                l1.AddEntry(self.h1_2017, "2017 Data")
                l1.AddEntry(self.h1_2018, "2018 Data")
                l1.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap1 = makeCheap(self.h1_2017)
		cheap1.Draw("hist")
		pull1 = makePull(self.h1_2017, self.h1_2018)
		pull1.Draw("esame")
		p22.RedrawAxis()
		c1.SaveAs("./plots/"+name+"_soft_norm.png")
		c1.Close()
		
		c2 = TCanvas()
		c2.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h2_2017.SetTitle("Thin Softdrop Mass")
		self.h2_2017.Draw("hist")
		self.h2_2018.Draw("same hist")
		l2 = TLegend(.5, .6, .89, .89)
		l2.SetFillColor(0)
		l2.SetLineColor(0)
                l2.AddEntry(self.h2_2017, "2017 Data")
                l2.AddEntry(self.h2_2018, "2018 Data")
                l2.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap2 = makeCheap(self.h2_2017)
		cheap2.Draw("hist")
		pull2 = makePull(self.h2_2017, self.h2_2018)
		pull2.Draw("esame")
		p22.RedrawAxis()
		c2.SaveAs("./plots/"+name+"_thin_soft_norm.png")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h3_2017.SetTitle("Jet pT")
		self.h3_2017.Draw("hist")
		self.h3_2018.Draw("same hist")
		l3 = TLegend(.5, .6, .89, .89)
		l3.SetFillColor(0)
		l3.SetLineColor(0)
                l3.AddEntry(self.h3_2017, "2017 Data")
                l3.AddEntry(self.h3_2018, "2018 Data")
                l3.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap3 = makeCheap(self.h3_2017)
		cheap3.Draw("hist")
		pull3 = makePull(self.h3_2017, self.h3_2018)
		pull3.Draw("esame")
		p22.RedrawAxis()
		c3.SaveAs("./plots/"+name+"_jet_pt_norm.png")
		c3.Close()
	
		c4 = TCanvas()
		c4.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h4_2017.SetTitle("Thin Jet pT")
		self.h4_2017.Draw("hist")
		self.h4_2018.Draw("same hist")
		l4 = TLegend(.5, .6, .89, .89)
		l4.SetFillColor(0)
		l4.SetLineColor(0)
                l4.AddEntry(self.h4_2017, "2017 Data")
                l4.AddEntry(self.h4_2018, "2018 Data")
                l4.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap4 = makeCheap(self.h4_2017)
		cheap4.Draw("hist")
		pull4 = makePull(self.h4_2017, self.h4_2018)
		pull4.Draw("esame")
		p22.RedrawAxis()
		c4.SaveAs("./plots/"+name+"_thin_jet_pt_norm.png")
		c4.Close()
		
		c5 = TCanvas()
		c5.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h5_2017.SetTitle("Number of Primary Vertices")
		self.h5_2017.Draw("hist")
		self.h5_2018.Draw("same hist")
		l5 = TLegend(.5, .6, .89, .89)
		l5.SetFillColor(0)
		l5.SetLineColor(0)
                l5.AddEntry(self.h5_2017, "2017 Data")
                l5.AddEntry(self.h5_2018, "2018 Data")
                l5.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap5 = makeCheap(self.h5_2017)
		cheap5.Draw("hist")
		pull5 = makePull(self.h5_2017, self.h5_2018)
		pull5.Draw("esame")
		p22.RedrawAxis()
		c5.SaveAs("./plots/"+name+"_nPV_norm.png")
		c5.Close()
		
		c6 = TCanvas()
		c6.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h6_2017.SetTitle("Number of (Good) Primary Vertices")
		self.h6_2017.Draw("hist")
		self.h6_2018.Draw("same hist")
		l6 = TLegend(.5, .6, .89, .89)
		l6.SetFillColor(0)
		l6.SetLineColor(0)
                l6.AddEntry(self.h6_2017, "2017 Data")
                l6.AddEntry(self.h6_2018, "2018 Data")
                l6.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap6 = makeCheap(self.h6_2017)
		cheap6.Draw("hist")
		pull6 = makePull(self.h6_2017, self.h6_2018)
		pull6.Draw("esame")
		p22.RedrawAxis()
		c6.SaveAs("./plots/"+name+"_nPV_good_norm.png")
		c6.Close()
		
		c7 = TCanvas()
		c7.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h7_2017.SetTitle("AK4 HT")
		self.h7_2017.Draw("hist")
		self.h7_2018.Draw("same hist")
		l7 = TLegend(.5, .6, .89, .89)
		l7.SetFillColor(0)
		l7.SetLineColor(0)
                l7.AddEntry(self.h7_2017, "2017 Data")
                l7.AddEntry(self.h7_2018, "2018 Data")
                l7.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap7 = makeCheap(self.h7_2017)
		cheap7.Draw("hist")
		pull7 = makePull(self.h7_2017, self.h7_2018)
		pull7.Draw("esame")
		p22.RedrawAxis()
		c7.SaveAs("./plots/"+name+"_HT_AK4_norm.png")
		c7.Close()
		
		c8 = TCanvas()
		c8.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h8_2017.SetTitle("AK8 HT")
		self.h8_2017.Draw("hist")
		self.h8_2018.Draw("same hist")
		l8 = TLegend(.5, .6, .89, .89)
		l8.SetFillColor(0)
		l8.SetLineColor(0)
                l8.AddEntry(self.h8_2017, "2017 Data")
                l8.AddEntry(self.h8_2018, "2018 Data")
                l8.Draw()
#		gPad.SetLogy()
		p22.cd() #bottom
		cheap8 = makeCheap(self.h8_2017)
		cheap8.Draw("hist")
		pull8 = makePull(self.h8_2017, self.h8_2018)
		pull8.Draw("esame")
		p22.RedrawAxis()
		c8.SaveAs("./plots/"+name+"_HT_AK8_norm.png")
		c8.Close()
		
		
		
		c1_logy = TCanvas()
		c1_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h1_2017.SetTitle("Softdrop Mass")
		self.h1_2017.Draw("hist")
		self.h1_2018.Draw("same hist")
		l1 = TLegend(.5, .6, .89, .89)
		l1.SetFillColor(0)
		l1.SetLineColor(0)
                l1.AddEntry(self.h1_2017, "2017 Data")
                l1.AddEntry(self.h1_2018, "2018 Data")
                l1.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap1 = makeCheap(self.h1_2017)
		cheap1.Draw("hist")
		pull1 = makePull(self.h1_2017, self.h1_2018)
		pull1.Draw("esame")
		p22.RedrawAxis()
		c1_logy.SaveAs("./plots/"+name+"_soft_logy_norm.png")
		c1_logy.Close()
		
		c2_logy = TCanvas()
		c2_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h2_2017.SetTitle("Thin Softdrop Mass")
		self.h2_2017.Draw("hist")
		self.h2_2018.Draw("same hist")
		l2 = TLegend(.5, .6, .89, .89)
		l2.SetFillColor(0)
		l2.SetLineColor(0)
                l2.AddEntry(self.h2_2017, "2017 Data")
                l2.AddEntry(self.h2_2018, "2018 Data")
                l2.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap2 = makeCheap(self.h2_2017)
		cheap2.Draw("hist")
		pull2 = makePull(self.h2_2017, self.h2_2018)
		pull2.Draw("esame")
		p22.RedrawAxis()
		c2_logy.SaveAs("./plots/"+name+"_thin_soft_logy_norm.png")
		c2_logy.Close()
		
		c3_logy = TCanvas()
		c3_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h3_2017.SetTitle("Jet pT")
		self.h3_2017.Draw("hist")
		self.h3_2018.Draw("same hist")
		l3 = TLegend(.5, .6, .89, .89)
		l3.SetFillColor(0)
		l3.SetLineColor(0)
                l3.AddEntry(self.h3_2017, "2017 Data")
                l3.AddEntry(self.h3_2018, "2018 Data")
                l3.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap3 = makeCheap(self.h3_2017)
		cheap3.Draw("hist")
		pull3 = makePull(self.h3_2017, self.h3_2018)
		pull3.Draw("esame")
		p22.RedrawAxis()
		c3_logy.SaveAs("./plots/"+name+"_jet_pt_logy_norm.png")
		c3_logy.Close()
	
		c4_logy = TCanvas()
		c4_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h4_2017.SetTitle("Thin Jet pT")
		self.h4_2017.Draw("hist")
		self.h4_2018.Draw("same hist")
		l4 = TLegend(.5, .6, .89, .89)
		l4.SetFillColor(0)
		l4.SetLineColor(0)
                l4.AddEntry(self.h4_2017, "2017 Data")
                l4.AddEntry(self.h4_2018, "2018 Data")
                l4.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap4 = makeCheap(self.h4_2017)
		cheap4.Draw("hist")
		pull4 = makePull(self.h4_2017, self.h4_2018)
		pull4.Draw("esame")
		p22.RedrawAxis()
		c4_logy.SaveAs("./plots/"+name+"_thin_jet_pt_logy_norm.png")
		c4_logy.Close()
		
		c5_logy = TCanvas()
		c5_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h5_2017.SetTitle("Number of Primary Vertices")
		self.h5_2017.Draw("hist")
		self.h5_2018.Draw("same hist")
		l5 = TLegend(.5, .6, .89, .89)
		l5.SetFillColor(0)
		l5.SetLineColor(0)
                l5.AddEntry(self.h5_2017, "2017 Data")
                l5.AddEntry(self.h5_2018, "2018 Data")
                l5.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap5 = makeCheap(self.h5_2017)
		cheap5.Draw("hist")
		pull5 = makePull(self.h5_2017, self.h5_2018)
		pull5.Draw("esame")
		p22.RedrawAxis()
		c5_logy.SaveAs("./plots/"+name+"_nPV_logy_norm.png")
		c5_logy.Close()
		
		c6_logy = TCanvas()
		c6_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h6_2017.SetTitle("Number of (Good) Primary Vertices")
		self.h6_2017.Draw("hist")
		self.h6_2018.Draw("same hist")
		l6 = TLegend(.5, .6, .89, .89)
		l6.SetFillColor(0)
		l6.SetLineColor(0)
                l6.AddEntry(self.h6_2017, "2017 Data")
                l6.AddEntry(self.h6_2018, "2018 Data")
                l6.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap6 = makeCheap(self.h6_2017)
		cheap6.Draw("hist")
		pull6 = makePull(self.h6_2017, self.h6_2018)
		pull6.Draw("esame")
		p22.RedrawAxis()
		c6_logy.SaveAs("./plots/"+name+"_nPV_good_logy_norm.png")
		c6_logy.Close()
		
		c7_logy = TCanvas()
		c7_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h7_2017.SetTitle("AK4 HT")
		self.h7_2017.Draw("hist")
		self.h7_2018.Draw("same hist")
		l7 = TLegend(.5, .6, .89, .89)
		l7.SetFillColor(0)
		l7.SetLineColor(0)
                l7.AddEntry(self.h7_2017, "2017 Data")
                l7.AddEntry(self.h7_2018, "2018 Data")
                l7.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap7 = makeCheap(self.h7_2017)
		cheap7.Draw("hist")
		pull7 = makePull(self.h7_2017, self.h7_2018)
		pull7.Draw("esame")
		p22.RedrawAxis()
		c7_logy.SaveAs("./plots/"+name+"_HT_AK4_logy_norm.png")
		c7_logy.Close()
		
		c8_logy = TCanvas()
		c8_logy.cd()
		p12 = TPad("pad1", "tall", 0,0.175,1,1)
		p22 = TPad("pad2", "short", 0,0.0,1.0,0.23)
		p12.Draw()
		p22.Draw()
		p12.cd() #top
		self.h8_2017.SetTitle("AK8 HT")
		self.h8_2017.Draw("hist")
		self.h8_2018.Draw("same hist")
		l8 = TLegend(.5, .6, .89, .89)
		l8.SetFillColor(0)
		l8.SetLineColor(0)
                l8.AddEntry(self.h8_2017, "2017 Data")
                l8.AddEntry(self.h8_2018, "2018 Data")
                l8.Draw()
		gPad.SetLogy()
		p22.cd() #bottom
		cheap8 = makeCheap(self.h8_2017)
		cheap8.Draw("hist")
		pull8 = makePull(self.h8_2017, self.h8_2018)
		pull8.Draw("esame")
		p22.RedrawAxis()
		c8_logy.SaveAs("./plots/"+name+"_HT_AK8_logy_norm.png")
		c8_logy.Close()
	
