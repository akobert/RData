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
		H.SetFillColor(args[1])
		H.SetFillStyle(args[2])
	if args[0] == 'markers':
		H.SetLineColor(args[1])
		H.SetMarkerColor(args[1])
		H.SetMarkerStyle(args[2])
	H.GetXaxis().SetTitleSize(0.04)

	if args[0] == 'dashed':
		H.SetLineColor(args[1])
		H.SetLineWidth(1)
		H.SetLineStyle(7)
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
	#latex.DrawLatex(0.1265, 0.825, cmsText)
	latex.DrawLatex(0.12, 0.91, cmsText)
	pad.Update()

def error(num, den):
	z = den - num
	error = 0
	if den != 0:
		err_num = sqrt(num) if num != 0 else 1.6
		err_z = sqrt(z) if z >0 else 1.6
		error = sqrt((z*z*err_num*err_num) + (num*num*err_z*err_z))/(den*den)
	return error

def error2(A, B, errA, errB):
	error = 0
	if A != 0 and B != 0:
		C = A/B
		error = sqrt(pow(errA/A,2) + pow(errB/B,2)) * C
	return error

class drawRData:
	def __init__(self, name, ifile1, ifile2, tag):
		gROOT.SetBatch(True)
        	LUMI = 34.31
        	cmsextra = "Preliminary"

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.notrig_data = self.f.Get("photon_pt_notrig")
		self.T175_data = self.f.Get("photon_pt_175")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.notrig_mc = self.g.Get("photon_pt_notrig")
		self.T175_mc = self.g.Get("photon_pt_175")
		
		ROOT.gInterpreter.Declare("Double_t widebins[31] = {0, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 215, 225, 235, 245, 255, 270, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")


		self.eff175_mc = TH1F("eff175_mc", "Photon Trigger Efficiency "+tag, 30, widebins)



		for i in range(1, self.T175_mc.GetNbinsX()+1):
			if self.T175_mc.GetBinContent(i) != 0 and self.notrig_mc.GetBinContent(i) != 0:
				self.eff175_mc.SetBinContent(i, self.T175_mc.GetBinContent(i)/self.notrig_mc.GetBinContent(i))
				self.eff175_mc.SetBinError(i, error(self.T175_mc.GetBinContent(i), self.notrig_mc.GetBinContent(i)))
			
			
		
		self.eff175_mc.SetLineColor(kViolet)
	
		self.eff175_mc.SetAxisRange(0,1.2, "Y")	
		
		self.eff175_mc_graph = TGraphAsymmErrors(self.eff175_mc)

		self.eff175_mc_graph.SetLineWidth(2)
		
		self.eff175_mc_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.eff175_mc_graph.GetN()):
			self.eff175_mc_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_mc_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_mc_graph.GetErrorYhigh(n) > 1.: self.eff175_mc_graph.SetPointEYhigh(n,1.-yval)
		
		self.eff175_mc_graph.GetYaxis().SetRangeUser(0.2,1.1)


		self.eff175_data = TH1F("eff175_data", "Photon Trigger Efficiency "+tag, 30, widebins)

		for i in range(1, self.T175_data.GetNbinsX()+1):
			if self.T175_data.GetBinContent(i) != 0 and self.notrig_data.GetBinContent(i) != 0:
				self.eff175_data.SetBinContent(i, self.T175_data.GetBinContent(i)/self.notrig_data.GetBinContent(i))
				self.eff175_data.SetBinError(i, error(self.T175_data.GetBinContent(i), self.notrig_data.GetBinContent(i)))
			
		
		self.eff175_data.SetLineColor(kViolet)
	
		self.eff175_data.SetAxisRange(0,1.2, "Y")	
		
		self.eff175_data_graph = TGraphAsymmErrors(self.eff175_data)

		self.eff175_data_graph.SetLineWidth(2)
		
		self.eff175_data_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.eff175_data_graph.GetN()):
			self.eff175_data_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_data_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_data_graph.GetErrorYhigh(n) > 1.: self.eff175_data_graph.SetPointEYhigh(n,1.-yval)
		
		self.eff175_data_graph.GetYaxis().SetRangeUser(0.2,1.1)

		self.eff175_ratio_graph = TGraphAsymmErrors(self.eff175_data_graph.GetN())

		for n in range(self.eff175_data_graph.GetN()):
			if self.eff175_data_graph.GetY()[n] > 0 and self.eff175_mc_graph.GetY()[n] > 0:
				self.eff175_ratio_graph.SetPoint(n, self.eff175_data_graph.GetX()[n], self.eff175_data_graph.GetY()[n]/self.eff175_mc_graph.GetY()[n])
				self.eff175_ratio_graph.SetPointError(n, self.eff175_data_graph.GetErrorXlow(n), self.eff175_data_graph.GetErrorXhigh(n), error2(self.eff175_data_graph.GetY()[n], self.eff175_mc_graph.GetY()[n], self.eff175_data_graph.GetErrorYlow(n), self.eff175_mc_graph.GetErrorYlow(n)), error2(self.eff175_data_graph.GetY()[n], self.eff175_mc_graph.GetY()[n], self.eff175_data_graph.GetErrorYlow(n), self.eff175_mc_graph.GetErrorYlow(n)))


                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.eff175_ratio_graph.GetN()):
			self.eff175_ratio_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_ratio_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_ratio_graph.GetErrorYhigh(n) > 1.: self.eff175_ratio_graph.SetPointEYhigh(n,1.-yval)
		
		self.eff175_ratio_graph.GetYaxis().SetRangeUser(0.2,1.1)

		self.eff175_ratio_graph.SetLineColor(kViolet)

		self.eff175_ratio_graph.SetLineWidth(2)

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.eff175_ratio_graph.SetTitle("2016 Cut-Based Trigger Efficiency Data/MC Ratio "+tag)
		self.eff175_ratio_graph.GetXaxis().SetTitle("Photon pT")
		self.eff175_ratio_graph.Draw("AP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1 = TLegend(.6, .25, .9, .4)
		l1.AddEntry(self.eff175_ratio_graph, "Photon175 Trigger")
                l1.Draw()
		line1 = TLine(200, 0.2, 200, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		#c1.SaveAs("./"+name+".root")
		c1.Close()

