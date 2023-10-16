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
        	LUMI = 59.82
        	cmsextra = "Preliminary"

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.notrig_data = self.f.Get("photon_pt_notrig")
		self.T110_data = self.f.Get("photon_pt_110")
		self.T200_data = self.f.Get("photon_pt_200")
		self.TOR_data = self.f.Get("photon_pt_OR")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.notrig_mc = self.g.Get("photon_pt_notrig")
		self.T110_mc = self.g.Get("photon_pt_110")
		self.T200_mc = self.g.Get("photon_pt_200")
		self.TOR_mc = self.g.Get("photon_pt_OR")
		
		ROOT.gInterpreter.Declare("Double_t widebins[35] = {0, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")

		self.eff110_mc = TH1F("eff110_mc", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.eff200_mc = TH1F("eff200_mc", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.effOR_mc = TH1F("effOR_mc", "Photon Trigger Efficiency "+tag, 34, widebins)



		for i in range(1, self.T110_mc.GetNbinsX()+1):
			if self.T110_mc.GetBinContent(i) != 0 and self.notrig_mc.GetBinContent(i) != 0:
				self.eff110_mc.SetBinContent(i, self.T110_mc.GetBinContent(i)/self.notrig_mc.GetBinContent(i))
				self.eff110_mc.SetBinError(i, error(self.T110_mc.GetBinContent(i), self.notrig_mc.GetBinContent(i)))
			
			if self.T200_mc.GetBinContent(i) != 0 and self.notrig_mc.GetBinContent(i) != 0:
				self.eff200_mc.SetBinContent(i, self.T200_mc.GetBinContent(i)/self.notrig_mc.GetBinContent(i))
				self.eff200_mc.SetBinError(i, error(self.T200_mc.GetBinContent(i), self.notrig_mc.GetBinContent(i)))
				
			if self.TOR_mc.GetBinContent(i) != 0 and self.notrig_mc.GetBinContent(i) != 0:
				self.effOR_mc.SetBinContent(i, self.TOR_mc.GetBinContent(i)/self.notrig_mc.GetBinContent(i))
				self.effOR_mc.SetBinError(i, error(self.TOR_mc.GetBinContent(i), self.notrig_mc.GetBinContent(i)))
			
		
		self.eff200_mc.SetLineColor(kRed)
		self.effOR_mc.SetLineColor(kViolet)
	
		self.eff110_mc.SetAxisRange(0,1.2, "Y")	
		self.eff200_mc.SetAxisRange(0,1.2, "Y")	
		self.effOR_mc.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mc_graph = TGraphAsymmErrors(self.eff200_mc)
		self.eff110_mc_graph = TGraphAsymmErrors(self.eff110_mc)
		self.effOR_mc_graph = TGraphAsymmErrors(self.effOR_mc)

		self.eff200_mc_graph.SetLineWidth(2)
		self.eff110_mc_graph.SetLineWidth(2)
		self.effOR_mc_graph.SetLineWidth(2)
		
		self.eff200_mc_graph.SetLineColor(kRed)
		self.eff110_mc_graph.SetLineColor(kBlue)
		self.effOR_mc_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mc_graph.GetN()):
			self.effOR_mc_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mc_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mc_graph.GetErrorYhigh(n) > 1.: self.effOR_mc_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mc_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mc_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mc_graph.GetErrorYhigh(n) > 1.: self.eff110_mc_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mc_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mc_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mc_graph.GetErrorYhigh(n) > 1.: self.eff200_mc_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mc_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mc_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mc_graph.GetYaxis().SetRangeUser(0.2,1.1)


		self.eff110_data = TH1F("eff110_data", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.eff200_data = TH1F("eff200_data", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.effOR_data = TH1F("effOR_data", "Photon Trigger Efficiency "+tag, 34, widebins)



		for i in range(1, self.T110_data.GetNbinsX()+1):
			if self.T110_data.GetBinContent(i) != 0 and self.notrig_data.GetBinContent(i) != 0:
				self.eff110_data.SetBinContent(i, self.T110_data.GetBinContent(i)/self.notrig_data.GetBinContent(i))
				self.eff110_data.SetBinError(i, error(self.T110_data.GetBinContent(i), self.notrig_data.GetBinContent(i)))
			
			if self.T200_data.GetBinContent(i) != 0 and self.notrig_data.GetBinContent(i) != 0:
				self.eff200_data.SetBinContent(i, self.T200_data.GetBinContent(i)/self.notrig_data.GetBinContent(i))
				self.eff200_data.SetBinError(i, error(self.T200_data.GetBinContent(i), self.notrig_data.GetBinContent(i)))
				
			if self.TOR_data.GetBinContent(i) != 0 and self.notrig_data.GetBinContent(i) != 0:
				self.effOR_data.SetBinContent(i, self.TOR_data.GetBinContent(i)/self.notrig_data.GetBinContent(i))
				self.effOR_data.SetBinError(i, error(self.TOR_data.GetBinContent(i), self.notrig_data.GetBinContent(i)))
			
		
		self.eff200_data.SetLineColor(kRed)
		self.effOR_data.SetLineColor(kViolet)
	
		self.eff110_data.SetAxisRange(0,1.2, "Y")	
		self.eff200_data.SetAxisRange(0,1.2, "Y")	
		self.effOR_data.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_data_graph = TGraphAsymmErrors(self.eff200_data)
		self.eff110_data_graph = TGraphAsymmErrors(self.eff110_data)
		self.effOR_data_graph = TGraphAsymmErrors(self.effOR_data)

		self.eff200_data_graph.SetLineWidth(2)
		self.eff110_data_graph.SetLineWidth(2)
		self.effOR_data_graph.SetLineWidth(2)
		
		self.eff200_data_graph.SetLineColor(kRed)
		self.eff110_data_graph.SetLineColor(kBlue)
		self.effOR_data_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_data_graph.GetN()):
			self.effOR_data_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_data_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_data_graph.GetErrorYhigh(n) > 1.: self.effOR_data_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_data_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_data_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_data_graph.GetErrorYhigh(n) > 1.: self.eff110_data_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_data_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_data_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_data_graph.GetErrorYhigh(n) > 1.: self.eff200_data_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_data_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_data_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_data_graph.GetYaxis().SetRangeUser(0.2,1.1)



		self.effOR_ratio_graph = TGraphAsymmErrors(self.effOR_data_graph.GetN())
		self.eff110_ratio_graph = TGraphAsymmErrors(self.eff110_data_graph.GetN())
		self.eff200_ratio_graph = TGraphAsymmErrors(self.eff200_data_graph.GetN())

		for n in range(self.effOR_data_graph.GetN()):
			if self.effOR_data_graph.GetY()[n] > 0 and self.effOR_mc_graph.GetY()[n] > 0:
				self.effOR_ratio_graph.SetPoint(n, self.effOR_data_graph.GetX()[n], self.effOR_data_graph.GetY()[n]/self.effOR_mc_graph.GetY()[n])
				print("OR Ratio Bin #"+str(n)+", X value="+str(self.effOR_data_graph.GetX()[n])+": "+str(self.effOR_data_graph.GetY()[n]/self.effOR_mc_graph.GetY()[n]))
				self.effOR_ratio_graph.SetPointError(n, self.effOR_data_graph.GetErrorXlow(n), self.effOR_data_graph.GetErrorXhigh(n), error2(self.effOR_data_graph.GetY()[n], self.effOR_mc_graph.GetY()[n], self.effOR_data_graph.GetErrorYlow(n), self.effOR_mc_graph.GetErrorYlow(n)), error2(self.effOR_data_graph.GetY()[n], self.effOR_mc_graph.GetY()[n], self.effOR_data_graph.GetErrorYlow(n), self.effOR_mc_graph.GetErrorYlow(n)))
			if self.eff110_data_graph.GetY()[n] > 0 and self.eff110_mc_graph.GetY()[n] > 0:
				self.eff110_ratio_graph.SetPoint(n, self.eff110_data_graph.GetX()[n], self.eff110_data_graph.GetY()[n]/self.eff110_mc_graph.GetY()[n])
				self.eff110_ratio_graph.SetPointError(n, self.eff110_data_graph.GetErrorXlow(n), self.eff110_data_graph.GetErrorXhigh(n), error2(self.eff110_data_graph.GetY()[n], self.eff110_mc_graph.GetY()[n], self.eff110_data_graph.GetErrorYlow(n), self.eff110_mc_graph.GetErrorYlow(n)), error2(self.eff110_data_graph.GetY()[n], self.eff110_mc_graph.GetY()[n], self.eff110_data_graph.GetErrorYlow(n), self.eff110_mc_graph.GetErrorYlow(n)))
			if self.eff200_data_graph.GetY()[n] > 0 and self.eff200_mc_graph.GetY()[n] > 0:
				self.eff200_ratio_graph.SetPoint(n, self.eff200_data_graph.GetX()[n], self.eff200_data_graph.GetY()[n]/self.eff200_mc_graph.GetY()[n])
				self.eff200_ratio_graph.SetPointError(n, self.eff200_data_graph.GetErrorXlow(n), self.eff200_data_graph.GetErrorXhigh(n), error2(self.eff200_data_graph.GetY()[n], self.eff200_mc_graph.GetY()[n], self.eff200_data_graph.GetErrorYlow(n), self.eff200_mc_graph.GetErrorYlow(n)), error2(self.eff200_data_graph.GetY()[n], self.eff200_mc_graph.GetY()[n], self.eff200_data_graph.GetErrorYlow(n), self.eff200_mc_graph.GetErrorYlow(n)))


                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_ratio_graph.GetN()):
			self.effOR_ratio_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_ratio_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_ratio_graph.GetErrorYhigh(n) > 1.: self.effOR_ratio_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_ratio_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_ratio_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_ratio_graph.GetErrorYhigh(n) > 1.: self.eff110_ratio_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_ratio_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_ratio_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_ratio_graph.GetErrorYhigh(n) > 1.: self.eff200_ratio_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_ratio_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_ratio_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_ratio_graph.GetYaxis().SetRangeUser(0.2,1.1)

		self.eff200_ratio_graph.SetLineColor(kRed)
		self.eff110_ratio_graph.SetLineColor(kBlue)
		self.effOR_ratio_graph.SetLineColor(kViolet)

		self.eff200_ratio_graph.SetLineWidth(2)
		self.eff110_ratio_graph.SetLineWidth(2)
		self.effOR_ratio_graph.SetLineWidth(2)

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.effOR_ratio_graph.SetTitle("Cut-Based Trigger Efficiency Data/MC Ratio "+tag)
		self.effOR_ratio_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_ratio_graph.Draw("AP")
#		self.eff110_ratio_graph.Draw("P")
#		self.eff200_ratio_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1 = TLegend(.6, .25, .9, .4)
#		l1.AddEntry(self.eff110_ratio_graph, "HLT_Photon110")
#		l1.AddEntry(self.eff200_ratio_graph, "HLT_Photon200")
		l1.AddEntry(self.effOR_ratio_graph, "ORed Triggers")
                l1.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		line2 = TLine(0, 1.0, 1100, 1.0)
		line2.SetLineColor(kBlue)
#		line2.SetLineWidth(2)
		line2.SetLineStyle(7)
		line2.Draw("same")
		line3 = TLine(0, 0.95, 1100, 0.95)
		line3.SetLineColor(kRed)
#		line3.SetLineWidth(2)
		line3.SetLineStyle(7)
		line3.Draw("same")
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		#c1.SaveAs("./"+name+".root")
		c1.Close()








#		c1 = TCanvas()
#		c1.cd()
		#self.eff110.SetXTitle("Photon pT")
#		self.eff110.Draw("histe")
#		self.eff200.Draw("same histe")
#		self.effOR.Draw("same histe")
#		l1 = TLegend(.6, .25, .9, .4)
#		l1.AddEntry(self.eff110, "Photon110")
 #               l1.AddEntry(self.eff200, "Photon200")
  #              l1.AddEntry(self.effOR, "OR")
   #             l1.Draw()
		#gPad.SetLogy()
#		c1.SaveAs("./"+name+".png")
#		c1.SaveAs("./"+name+".root")
#		c1.Close()

#		self.notrig.SetLineColor(kGreen)
#		self.T110.SetLineColor(kBlue)
#		self.T200.SetLineColor(kRed)
#		self.TOR.SetLineColor(kViolet)
#
#		c2 = TCanvas()
#		c2.cd()
#		self.notrig.SetTitle("Photon pT "+tag)
#		self.notrig.SetXTitle("Photon pT")
#		self.notrig.Draw("histe")
#		self.T110.Draw("same histe")
#		self.T200.Draw("same histe")
#		self.TOR.Draw("same histe")
#		l2 = TLegend(.6, .75, .9, .9)
#		l2.AddEntry(self.T110, "Photon110")
    #            l2.AddEntry(self.T200, "Photon200")
   #             l2.AddEntry(self.TOR, "OR")
  #              l2.AddEntry(self.notrig, "No Trigger")
 #               l2.Draw()
#		gPad.SetLogy()
#		c2.SaveAs("./photon_pt_"+name+".png")
#		c2.SaveAs("./photon_pt_"+name+".root")
#		c2.Close()
		
#		c3 = TCanvas()
#		c3.cd()
#		self.effOR_thin.SetTitle("Thin OR Trigger Photon pT Efficiency "+tag)
#		self.effOR_thin.SetXTitle("Photon pT")
	#	self.effOR_thin.Draw("histe")
#		self.effOR_thin.Draw("hist")
#		c3.SaveAs("./thin_"+name+".png")
#		c3.SaveAs("./thin_"+name+".root")
#		c3.Close()

