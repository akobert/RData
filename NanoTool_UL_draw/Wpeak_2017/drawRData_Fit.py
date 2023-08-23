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
#                i.SetStats(0)
                t = i.GetMaximum()
                if t > maximum:
                        maximum = t
        for j in args:
                j.GetYaxis().SetRangeUser(1,maximum*1.35)#should be 1.35 (below as well)
                j.SetLineWidth(2)
        return maximum*1.35

def GoodPlotFormat(H, *args): # Handy little script for color/line/fill/point/etc...
#        try: H.SetStats(0)
#        except: print " ------------ [  No stats box found!  ]"
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

class drawRData_Fit:
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
		
		self.f2_Data = self.c.Get("fail_soft_thin")
		self.f2_1_Data = self.c.Get("fail_soft_uncorr_thin")
		
		comment1 = '''
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
'''		

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
		
		self.f2_TTBar = self.d.Get("fail_soft_thin")
		self.f2_1_TTBar = self.d.Get("fail_soft_uncorr_thin")
		
		comment2 = '''
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
'''		

		LUMI = 41.84 
        	cmsextra = "Preliminary"
		
		#Gaussian Fits
		#ROOT.gStyle.SetOptStat(111111)
		#gROOT.SetStyle("Plain")
		ROOT.gStyle.SetOptFit(111111)
	

		FitLimLow = 75
		FitLimHigh = 95
		Par0 = 4000 	#Amplitude
		Par1 = 5 	#Sigma
		Par2 = 80 	#Mean
		func = TF1("func", fitf, FitLimLow, FitLimHigh, 3)
		func.SetParameters(Par0, Par1, Par2)
		func.SetParNames("GaussAmp", "GaussSigma", "GaussMean")
		func.SetParLimits(1, 1, 20)
		func.SetParLimits(2, 70, 90)
		
		f2 = TCanvas()
		f2.cd()
#		f2.SetLogy()
		self.h2_Data.SetTitle("SingleMuon (Corrected) Softdrop Mass Fit")
		self.h2_Data.SetLineColor(1)
		self.h2_Data.Fit(func, "r")
		self.h2_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		f2.SaveAs("./plots/"+name+"_Data_corr_fit.png")
#		f2.SaveAs("./plots/"+name+"_Data_corr_fit.root")
		f2.Close()
		
		f2_1 = TCanvas()
		f2_1.cd()
#		f2_1.SetLogy()
		self.h2_1_Data.SetTitle("SingleMuon (Uncorrected) Softdrop Mass Fit")
		self.h2_1_Data.SetLineColor(1)
		self.h2_1_Data.Fit(func, "r")
		self.h2_1_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		f2_1.SaveAs("./plots/"+name+"_Data_uncorr_fit.png")
#		f2_1.SaveAs("./plots/"+name+"_Data_uncorr_fit.root")
		f2_1.Close()
		
		f2_tt = TCanvas()
		f2_tt.cd()
#		f2_tt.SetLogy()
		self.h2_TTBar.SetTitle("TTBar (Corrected) Softdrop Mass Fit")
		self.h2_TTBar.SetLineColor(1)
		self.h2_TTBar.Fit(func, "r")
		self.h2_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		f2_tt.SaveAs("./plots/"+name+"_TTBar_corr_fit.png")
#		f2_tt.SaveAs("./plots/"+name+"_TTBar_corr_fit.root")
		f2_tt.Close()
		
		f2_tt_1 = TCanvas()
		f2_tt_1.cd()
#		f2_tt_1.SetLogy()
		self.h2_1_TTBar.SetTitle("TTBar (Uncorrected) Softdrop Mass Fit")
		self.h2_1_TTBar.SetLineColor(1)
		self.h2_1_TTBar.Fit(func, "r")
		self.h2_1_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		f2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_fit.png")
#		f2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_fit.root")
		f2_tt_1.Close()
		
		pf2 = TCanvas()
		pf2.cd()
#		pf2.SetLogy()
		self.p2_Data.SetTitle("SingleMuon (Corrected) Passing Softdrop Mass Fit")
		self.p2_Data.SetLineColor(1)
		self.p2_Data.Fit(func, "r")
		self.p2_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		pf2.SaveAs("./plots/"+name+"_Data_corr_pass_fit.png")
#		pf2.SaveAs("./plots/"+name+"_Data_corr_fit.root")
		pf2.Close()
		
		pf2_1 = TCanvas()
		pf2_1.cd()
#		pf2_1.SetLogy()
		self.p2_1_Data.SetTitle("SingleMuon (Uncorrected) Passing Softdrop Mass Fit")
		self.p2_1_Data.SetLineColor(1)
		self.p2_1_Data.Fit(func, "r")
		self.p2_1_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		pf2_1.SaveAs("./plots/"+name+"_Data_uncorr_pass_fit.png")
#		pf2_1.SaveAs("./plots/"+name+"_Data_uncorr_fit.root")
		pf2_1.Close()
		
		pf2_tt = TCanvas()
		pf2_tt.cd()
#		pf2_tt.SetLogy()
		self.p2_TTBar.SetTitle("TTBar (Corrected) Passing Softdrop Mass Fit")
		self.p2_TTBar.SetLineColor(1)
		self.p2_TTBar.Fit(func, "r")
		self.p2_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		pf2_tt.SaveAs("./plots/"+name+"_TTBar_corr_pass_fit.png")
#		pf2_tt.SaveAs("./plots/"+name+"_TTBar_corr_fit.root")
		pf2_tt.Close()
		
		pf2_tt_1 = TCanvas()
		pf2_tt_1.cd()
#		pf2_tt_1.SetLogy()
		self.p2_1_TTBar.SetTitle("TTBar (Uncorrected) Passing Softdrop Mass Fit")
		self.p2_1_TTBar.SetLineColor(1)
		self.p2_1_TTBar.Fit(func, "r")
		self.p2_1_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		pf2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_pass_fit.png")
#		pf2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_fit.root")
		pf2_tt_1.Close()

		ff2 = TCanvas()
		ff2.cd()
#		ff2.SetLogy()
		self.f2_Data.SetTitle("SingleMuon (Corrected) Failing Softdrop Mass Fit")
		self.f2_Data.SetLineColor(1)
		self.f2_Data.Fit(func, "r")
		self.f2_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		ff2.SaveAs("./plots/"+name+"_Data_corr_fail_fit.png")
#		ff2.SaveAs("./plots/"+name+"_Data_corr_fit.root")
		ff2.Close()
		
		ff2_1 = TCanvas()
		ff2_1.cd()
#		ff2_1.SetLogy()
		self.f2_1_Data.SetTitle("SingleMuon (Uncorrected) Failing Softdrop Mass Fit")
		self.f2_1_Data.SetLineColor(1)
		self.f2_1_Data.Fit(func, "r")
		self.f2_1_Data.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		ff2_1.SaveAs("./plots/"+name+"_Data_uncorr_fail_fit.png")
#		ff2_1.SaveAs("./plots/"+name+"_Data_uncorr_fit.root")
		ff2_1.Close()
		
		ff2_tt = TCanvas()
		ff2_tt.cd()
#		ff2_tt.SetLogy()
		self.f2_TTBar.SetTitle("TTBar (Corrected) Failing Softdrop Mass Fit")
		self.f2_TTBar.SetLineColor(1)
		self.f2_TTBar.Fit(func, "r")
		self.f2_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		ff2_tt.SaveAs("./plots/"+name+"_TTBar_corr_fail_fit.png")
#		ff2_tt.SaveAs("./plots/"+name+"_TTBar_corr_fit.root")
		ff2_tt.Close()
		
		ff2_tt_1 = TCanvas()
		ff2_tt_1.cd()
#		ff2_tt_1.SetLogy()
		self.f2_1_TTBar.SetTitle("TTBar (Uncorrected) Failing Softdrop Mass Fit")
		self.f2_1_TTBar.SetLineColor(1)
		self.f2_1_TTBar.Fit(func, "r")
		self.f2_1_TTBar.Draw("samehiste")
#		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#wmass = TLine(80.379,0,80.379,gPad.GetUymax())
		#wmass.SetLineColor(kViolet)
		#wmass.SetLineWidth(2)
		#wmass.Draw("same")
		ff2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_fail_fit.png")
#		ff2_tt_1.SaveAs("./plots/"+name+"_TTBar_uncorr_fit.root")
		ff2_tt_1.Close()

