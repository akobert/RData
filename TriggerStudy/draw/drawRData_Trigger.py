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
#	r = num.GetBinContent(n)/den.GetBinContent(n)

#	return r*sqrt(pow(num.GetBinError(n)/num.GetBinContent(n),2) + pow(den.GetBinError(n)/den.GetBinContent(n),2))
	
	z = den - num
	error = 0
	if den != 0:
		err_num = sqrt(num) if num != 0 else 1.6
		err_z = sqrt(z) if z !=0 else 1.6
		error = sqrt((z*z*err_num*err_num) + (num*num*err_z*err_z))/(den*den)
	return error
	

class drawRData:
	def __init__(self, name, ifile1, tag):
		gROOT.SetBatch(True)
        	LUMI = 59.82
        	cmsextra = "Preliminary"

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.notrig = self.f.Get("photon_pt_notrig")
		self.T110 = self.f.Get("photon_pt_110")
		self.T200 = self.f.Get("photon_pt_200")
		self.TOR = self.f.Get("photon_pt_OR")
		
		self.notrig_mva90 = self.f.Get("photon_pt_notrig_mva90")
		self.T110_mva90 = self.f.Get("photon_pt_110_mva90")
		self.T200_mva90 = self.f.Get("photon_pt_200_mva90")
		self.TOR_mva90 = self.f.Get("photon_pt_OR_mva90")
		
		self.notrig_mva80 = self.f.Get("photon_pt_notrig_mva80")
		self.T110_mva80 = self.f.Get("photon_pt_110_mva80")
		self.T200_mva80 = self.f.Get("photon_pt_200_mva80")
		self.TOR_mva80 = self.f.Get("photon_pt_OR_mva80")
		
		self.notrig_mva8 = self.f.Get("photon_pt_notrig_mva8")
		self.T110_mva8 = self.f.Get("photon_pt_110_mva8")
		self.T200_mva8 = self.f.Get("photon_pt_200_mva8")
		self.TOR_mva8 = self.f.Get("photon_pt_OR_mva8")
		
		self.notrig_mva85 = self.f.Get("photon_pt_notrig_mva85")
		self.T110_mva85 = self.f.Get("photon_pt_110_mva85")
		self.T200_mva85 = self.f.Get("photon_pt_200_mva85")
		self.TOR_mva85 = self.f.Get("photon_pt_OR_mva85")
		
		self.notrig_mva9 = self.f.Get("photon_pt_notrig_mva9")
		self.T110_mva9 = self.f.Get("photon_pt_110_mva9")
		self.T200_mva9 = self.f.Get("photon_pt_200_mva9")
		self.TOR_mva9 = self.f.Get("photon_pt_OR_mva9")
		
		ROOT.gInterpreter.Declare("Double_t widebins[35] = {0, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")

		self.eff110 = TH1F("eff110", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.eff200 = TH1F("eff200", "Photon Trigger Efficiency "+tag, 34, widebins)
		self.effOR = TH1F("effOR", "Photon Trigger Efficiency "+tag, 34, widebins)
		
		self.eff110_mva90 = TH1F("eff110_mva90", "Photon Trigger Efficiency (MVA WP90) "+tag, 34, widebins)
		self.eff200_mva90 = TH1F("eff200_mva90", "Photon Trigger Efficiency (MVA WP90) "+tag, 34, widebins)
		self.effOR_mva90 = TH1F("effOR_mva90", "Photon Trigger Efficiency (MVA WP90) "+tag, 34, widebins)
		
		self.eff110_mva80 = TH1F("eff110_mva80", "Photon Trigger Efficiency (MVA WP80) "+tag, 34, widebins)
		self.eff200_mva80 = TH1F("eff200_mva80", "Photon Trigger Efficiency (MVA WP80) "+tag, 34, widebins)
		self.effOR_mva80 = TH1F("effOR_mva80", "Photon Trigger Efficiency (MVA WP80) "+tag, 34, widebins)
		
		self.eff110_mva8 = TH1F("eff110_mva8", "Photon Trigger Efficiency (MVA>0.8) "+tag, 34, widebins)
		self.eff200_mva8 = TH1F("eff200_mva8", "Photon Trigger Efficiency (MVA>0.8) "+tag, 34, widebins)
		self.effOR_mva8 = TH1F("effOR_mva8", "Photon Trigger Efficiency (MVA>0.8) "+tag, 34, widebins)
		
		self.eff110_mva85 = TH1F("eff110_mva85", "Photon Trigger Efficiency (MVA>0.85) "+tag, 34, widebins)
		self.eff200_mva85 = TH1F("eff200_mva85", "Photon Trigger Efficiency (MVA>0.85) "+tag, 34, widebins)
		self.effOR_mva85 = TH1F("effOR_mva85", "Photon Trigger Efficiency (MVA>0.85) "+tag, 34, widebins)
		
		self.eff110_mva9 = TH1F("eff110_mva9", "Photon Trigger Efficiency (MVA>0.9) "+tag, 34, widebins)
		self.eff200_mva9 = TH1F("eff200_mva9", "Photon Trigger Efficiency (MVA>0.9) "+tag, 34, widebins)
		self.effOR_mva9 = TH1F("effOR_mva9", "Photon Trigger Efficiency (MVA>0.9) "+tag, 34, widebins)

#		self.effOR_thin = TH1F("effOR_thin", "Thin Photon Trigger Efficiency "+tag, 500, 0, 500)


		for i in range(1, self.T110.GetNbinsX()+1):
			if self.T110.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.eff110.SetBinContent(i, self.T110.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.eff110.SetBinError(i, error(self.T110.GetBinContent(i), self.notrig.GetBinContent(i)))
			
			if self.T200.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.eff200.SetBinContent(i, self.T200.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.eff200.SetBinError(i, error(self.T200.GetBinContent(i), self.notrig.GetBinContent(i)))
				
			if self.TOR.GetBinContent(i) != 0 and self.notrig.GetBinContent(i) != 0:
				self.effOR.SetBinContent(i, self.TOR.GetBinContent(i)/self.notrig.GetBinContent(i))
				self.effOR.SetBinError(i, error(self.TOR.GetBinContent(i), self.notrig.GetBinContent(i)))
			
		for i in range(1, self.T110_mva90.GetNbinsX()+1):
			if self.T110_mva90.GetBinContent(i) != 0 and self.notrig_mva90.GetBinContent(i) != 0:
				self.eff110_mva90.SetBinContent(i, self.T110_mva90.GetBinContent(i)/self.notrig_mva90.GetBinContent(i))
				self.eff110_mva90.SetBinError(i, error(self.T110_mva90.GetBinContent(i), self.notrig_mva90.GetBinContent(i)))
			
			if self.T200_mva90.GetBinContent(i) != 0 and self.notrig_mva90.GetBinContent(i) != 0:
				self.eff200_mva90.SetBinContent(i, self.T200_mva90.GetBinContent(i)/self.notrig_mva90.GetBinContent(i))
				self.eff200_mva90.SetBinError(i, error(self.T200_mva90.GetBinContent(i), self.notrig_mva90.GetBinContent(i)))
				
			if self.TOR_mva90.GetBinContent(i) != 0 and self.notrig_mva90.GetBinContent(i) != 0:
				self.effOR_mva90.SetBinContent(i, self.TOR_mva90.GetBinContent(i)/self.notrig_mva90.GetBinContent(i))
				self.effOR_mva90.SetBinError(i, error(self.TOR_mva90.GetBinContent(i), self.notrig_mva90.GetBinContent(i)))

		for i in range(1, self.T110_mva80.GetNbinsX()+1):
			if self.T110_mva80.GetBinContent(i) != 0 and self.notrig_mva80.GetBinContent(i) != 0:
				self.eff110_mva80.SetBinContent(i, self.T110_mva80.GetBinContent(i)/self.notrig_mva80.GetBinContent(i))
				self.eff110_mva80.SetBinError(i, error(self.T110_mva80.GetBinContent(i), self.notrig_mva80.GetBinContent(i)))
			
			if self.T200_mva80.GetBinContent(i) != 0 and self.notrig_mva80.GetBinContent(i) != 0:
				self.eff200_mva80.SetBinContent(i, self.T200_mva80.GetBinContent(i)/self.notrig_mva80.GetBinContent(i))
				self.eff200_mva80.SetBinError(i, error(self.T200_mva80.GetBinContent(i), self.notrig_mva80.GetBinContent(i)))
				
			if self.TOR_mva80.GetBinContent(i) != 0 and self.notrig_mva80.GetBinContent(i) != 0:
				self.effOR_mva80.SetBinContent(i, self.TOR_mva80.GetBinContent(i)/self.notrig_mva80.GetBinContent(i))
				self.effOR_mva80.SetBinError(i, error(self.TOR_mva80.GetBinContent(i), self.notrig_mva80.GetBinContent(i)))

		for i in range(1, self.T110_mva8.GetNbinsX()+1):
			if self.T110_mva8.GetBinContent(i) != 0 and self.notrig_mva8.GetBinContent(i) != 0:
				self.eff110_mva8.SetBinContent(i, self.T110_mva8.GetBinContent(i)/self.notrig_mva8.GetBinContent(i))
				self.eff110_mva8.SetBinError(i, error(self.T110_mva8.GetBinContent(i), self.notrig_mva8.GetBinContent(i)))
			
			if self.T200_mva8.GetBinContent(i) != 0 and self.notrig_mva8.GetBinContent(i) != 0:
				self.eff200_mva8.SetBinContent(i, self.T200_mva8.GetBinContent(i)/self.notrig_mva8.GetBinContent(i))
				self.eff200_mva8.SetBinError(i, error(self.T200_mva8.GetBinContent(i), self.notrig_mva8.GetBinContent(i)))
				
			if self.TOR_mva8.GetBinContent(i) != 0 and self.notrig_mva8.GetBinContent(i) != 0:
				self.effOR_mva8.SetBinContent(i, self.TOR_mva8.GetBinContent(i)/self.notrig_mva8.GetBinContent(i))
				self.effOR_mva8.SetBinError(i, error(self.TOR_mva8.GetBinContent(i), self.notrig_mva8.GetBinContent(i)))

		for i in range(1, self.T110_mva85.GetNbinsX()+1):
			if self.T110_mva85.GetBinContent(i) != 0 and self.notrig_mva85.GetBinContent(i) != 0:
				self.eff110_mva85.SetBinContent(i, self.T110_mva85.GetBinContent(i)/self.notrig_mva85.GetBinContent(i))
				self.eff110_mva85.SetBinError(i, error(self.T110_mva85.GetBinContent(i), self.notrig_mva85.GetBinContent(i)))
			
			if self.T200_mva85.GetBinContent(i) != 0 and self.notrig_mva85.GetBinContent(i) != 0:
				self.eff200_mva85.SetBinContent(i, self.T200_mva85.GetBinContent(i)/self.notrig_mva85.GetBinContent(i))
				self.eff200_mva85.SetBinError(i, error(self.T200_mva85.GetBinContent(i), self.notrig_mva85.GetBinContent(i)))
				
			if self.TOR_mva85.GetBinContent(i) != 0 and self.notrig_mva85.GetBinContent(i) != 0:
				self.effOR_mva85.SetBinContent(i, self.TOR_mva85.GetBinContent(i)/self.notrig_mva85.GetBinContent(i))
				self.effOR_mva85.SetBinError(i, error(self.TOR_mva85.GetBinContent(i), self.notrig_mva85.GetBinContent(i)))

		for i in range(1, self.T110_mva9.GetNbinsX()+1):
			if self.T110_mva9.GetBinContent(i) != 0 and self.notrig_mva9.GetBinContent(i) != 0:
				self.eff110_mva9.SetBinContent(i, self.T110_mva9.GetBinContent(i)/self.notrig_mva9.GetBinContent(i))
				self.eff110_mva9.SetBinError(i, error(self.T110_mva9.GetBinContent(i), self.notrig_mva9.GetBinContent(i)))
			
			if self.T200_mva9.GetBinContent(i) != 0 and self.notrig_mva9.GetBinContent(i) != 0:
				self.eff200_mva9.SetBinContent(i, self.T200_mva9.GetBinContent(i)/self.notrig_mva9.GetBinContent(i))
				self.eff200_mva9.SetBinError(i, error(self.T200_mva9.GetBinContent(i), self.notrig_mva9.GetBinContent(i)))
				
			if self.TOR_mva9.GetBinContent(i) != 0 and self.notrig_mva9.GetBinContent(i) != 0:
				self.effOR_mva9.SetBinContent(i, self.TOR_mva9.GetBinContent(i)/self.notrig_mva9.GetBinContent(i))
				self.effOR_mva9.SetBinError(i, error(self.TOR_mva9.GetBinContent(i), self.notrig_mva9.GetBinContent(i)))




#		for i in range(1, self.TOR_thin.GetNbinsX()+1):
#			if self.TOR_thin.GetBinContent(i) != 0 and self.notrig_thin.GetBinContent(i) != 0:
#				self.effOR_thin.SetBinContent(i, self.TOR_thin.GetBinContent(i)/self.notrig_thin.GetBinContent(i))
#				self.effOR_thin.SetBinError(i, error(self.TOR_thin.GetBinContent(i), self.notrig_thin.GetBinContent(i)))
				#print(self.effOR_thin.GetBinContent(i))			
			
		
		
		self.eff200.SetLineColor(kRed)
		self.effOR.SetLineColor(kViolet)
	
		self.eff110.SetAxisRange(0,1.2, "Y")	
		self.eff200.SetAxisRange(0,1.2, "Y")	
		self.effOR.SetAxisRange(0,1.2, "Y")	
#		self.effOR_thin.SetAxisRange(0.9,1.1, "Y")	
		
		self.eff200_graph = TGraphAsymmErrors(self.eff200)
		self.eff110_graph = TGraphAsymmErrors(self.eff110)
		self.effOR_graph = TGraphAsymmErrors(self.effOR)

		self.eff200_graph.SetLineWidth(2)
		self.eff110_graph.SetLineWidth(2)
		self.effOR_graph.SetLineWidth(2)
		
		self.eff200_graph.SetLineColor(kRed)
		self.eff110_graph.SetLineColor(kBlue)
		self.effOR_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_graph.GetN()):
			self.effOR_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_graph.GetErrorYhigh(n) > 1.: self.effOR_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_graph.GetErrorYhigh(n) > 1.: self.eff110_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_graph.GetErrorYhigh(n) > 1.: self.eff200_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.effOR_graph.SetTitle("Cut-Based Trigger Efficiency "+tag)
		self.effOR_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_graph.Draw("AP")
		self.eff110_graph.Draw("P")
		self.eff200_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1 = TLegend(.6, .25, .9, .4)
		l1.AddEntry(self.eff110_graph, "HLT_Photon110")
		l1.AddEntry(self.eff200_graph, "HLT_Photon200")
		l1.AddEntry(self.effOR_graph, "ORed Triggers")
                l1.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		#c1.SaveAs("./"+name+".root")
		c1.Close()



		self.eff200_mva90.SetLineColor(kRed)
		self.effOR_mva90.SetLineColor(kViolet)
	
		self.eff110_mva90.SetAxisRange(0,1.2, "Y")	
		self.eff200_mva90.SetAxisRange(0,1.2, "Y")	
		self.effOR_mva90.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mva90_graph = TGraphAsymmErrors(self.eff200_mva90)
		self.eff110_mva90_graph = TGraphAsymmErrors(self.eff110_mva90)
		self.effOR_mva90_graph = TGraphAsymmErrors(self.effOR_mva90)

		self.eff200_mva90_graph.SetLineWidth(2)
		self.eff110_mva90_graph.SetLineWidth(2)
		self.effOR_mva90_graph.SetLineWidth(2)
		
		self.eff200_mva90_graph.SetLineColor(kRed)
		self.eff110_mva90_graph.SetLineColor(kBlue)
		self.effOR_mva90_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mva90_graph.GetN()):
			self.effOR_mva90_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mva90_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mva90_graph.GetErrorYhigh(n) > 1.: self.effOR_mva90_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mva90_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mva90_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mva90_graph.GetErrorYhigh(n) > 1.: self.eff110_mva90_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mva90_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mva90_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mva90_graph.GetErrorYhigh(n) > 1.: self.eff200_mva90_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mva90_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mva90_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mva90_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1_mva90 = TCanvas()
		c1_mva90.cd()
		self.effOR_mva90_graph.SetTitle("Cut-Based Trigger Efficiency (WP90) "+tag)
		self.effOR_mva90_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_mva90_graph.Draw("AP")
		self.eff110_mva90_graph.Draw("P")
		self.eff200_mva90_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1_mva90 = TLegend(.6, .25, .9, .4)
		l1_mva90.AddEntry(self.eff110_mva90_graph, "HLT_Photon110")
		l1_mva90.AddEntry(self.eff200_mva90_graph, "HLT_Photon200")
		l1_mva90.AddEntry(self.effOR_mva90_graph, "ORed Triggers")
                l1_mva90.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1_mva90.SaveAs("./"+name+"_wp90.png")
		#c1_mva90.SaveAs("./"+name+"_wp90.root")
		c1_mva90.Close()


		self.eff200_mva80.SetLineColor(kRed)
		self.effOR_mva80.SetLineColor(kViolet)
	
		self.eff110_mva80.SetAxisRange(0,1.2, "Y")	
		self.eff200_mva80.SetAxisRange(0,1.2, "Y")	
		self.effOR_mva80.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mva80_graph = TGraphAsymmErrors(self.eff200_mva80)
		self.eff110_mva80_graph = TGraphAsymmErrors(self.eff110_mva80)
		self.effOR_mva80_graph = TGraphAsymmErrors(self.effOR_mva80)

		self.eff200_mva80_graph.SetLineWidth(2)
		self.eff110_mva80_graph.SetLineWidth(2)
		self.effOR_mva80_graph.SetLineWidth(2)
		
		self.eff200_mva80_graph.SetLineColor(kRed)
		self.eff110_mva80_graph.SetLineColor(kBlue)
		self.effOR_mva80_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mva80_graph.GetN()):
			self.effOR_mva80_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mva80_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mva80_graph.GetErrorYhigh(n) > 1.: self.effOR_mva80_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mva80_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mva80_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mva80_graph.GetErrorYhigh(n) > 1.: self.eff110_mva80_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mva80_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mva80_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mva80_graph.GetErrorYhigh(n) > 1.: self.eff200_mva80_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mva80_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mva80_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mva80_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1_mva80 = TCanvas()
		c1_mva80.cd()
		self.effOR_mva80_graph.SetTitle("Cut-Based Trigger Efficiency (WP80) "+tag)
		self.effOR_mva80_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_mva80_graph.Draw("AP")
		self.eff110_mva80_graph.Draw("P")
		self.eff200_mva80_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1_mva80 = TLegend(.6, .25, .9, .4)
		l1_mva80.AddEntry(self.eff110_mva80_graph, "HLT_Photon110")
		l1_mva80.AddEntry(self.eff200_mva80_graph, "HLT_Photon200")
		l1_mva80.AddEntry(self.effOR_mva80_graph, "ORed Triggers")
                l1_mva80.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1_mva80.SaveAs("./"+name+"_wp80.png")
		#c1_mva80.SaveAs("./"+name+"_wp80.root")
		c1_mva80.Close()

		self.eff200_mva8.SetLineColor(kRed)
		self.effOR_mva8.SetLineColor(kViolet)
	
		self.eff110_mva8.SetAxisRange(0,1.2, "Y")	
		self.eff200_mva8.SetAxisRange(0,1.2, "Y")	
		self.effOR_mva8.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mva8_graph = TGraphAsymmErrors(self.eff200_mva8)
		self.eff110_mva8_graph = TGraphAsymmErrors(self.eff110_mva8)
		self.effOR_mva8_graph = TGraphAsymmErrors(self.effOR_mva8)

		self.eff200_mva8_graph.SetLineWidth(2)
		self.eff110_mva8_graph.SetLineWidth(2)
		self.effOR_mva8_graph.SetLineWidth(2)
		
		self.eff200_mva8_graph.SetLineColor(kRed)
		self.eff110_mva8_graph.SetLineColor(kBlue)
		self.effOR_mva8_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mva8_graph.GetN()):
			self.effOR_mva8_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mva8_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mva8_graph.GetErrorYhigh(n) > 1.: self.effOR_mva8_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mva8_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mva8_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mva8_graph.GetErrorYhigh(n) > 1.: self.eff110_mva8_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mva8_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mva8_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mva8_graph.GetErrorYhigh(n) > 1.: self.eff200_mva8_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mva8_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mva8_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mva8_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1_mva8 = TCanvas()
		c1_mva8.cd()
		self.effOR_mva8_graph.SetTitle("Cut-Based Trigger Efficiency (MVA>0.8) "+tag)
		self.effOR_mva8_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_mva8_graph.Draw("AP")
		self.eff110_mva8_graph.Draw("P")
		self.eff200_mva8_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1_mva8 = TLegend(.6, .25, .9, .4)
		l1_mva8.AddEntry(self.eff110_mva8_graph, "HLT_Photon110")
		l1_mva8.AddEntry(self.eff200_mva8_graph, "HLT_Photon200")
		l1_mva8.AddEntry(self.effOR_mva8_graph, "ORed Triggers")
                l1_mva8.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1_mva8.SaveAs("./"+name+"_mva8.png")
		#c1_mva8.SaveAs("./"+name+"_mva8.root")
		c1_mva8.Close()



		self.eff200_mva85.SetLineColor(kRed)
		self.effOR_mva85.SetLineColor(kViolet)
	
		self.eff110_mva85.SetAxisRange(0,1.2, "Y")	
		self.eff200_mva85.SetAxisRange(0,1.2, "Y")	
		self.effOR_mva85.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mva85_graph = TGraphAsymmErrors(self.eff200_mva85)
		self.eff110_mva85_graph = TGraphAsymmErrors(self.eff110_mva85)
		self.effOR_mva85_graph = TGraphAsymmErrors(self.effOR_mva85)

		self.eff200_mva85_graph.SetLineWidth(2)
		self.eff110_mva85_graph.SetLineWidth(2)
		self.effOR_mva85_graph.SetLineWidth(2)
		
		self.eff200_mva85_graph.SetLineColor(kRed)
		self.eff110_mva85_graph.SetLineColor(kBlue)
		self.effOR_mva85_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mva85_graph.GetN()):
			self.effOR_mva85_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mva85_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mva85_graph.GetErrorYhigh(n) > 1.: self.effOR_mva85_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mva85_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mva85_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mva85_graph.GetErrorYhigh(n) > 1.: self.eff110_mva85_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mva85_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mva85_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mva85_graph.GetErrorYhigh(n) > 1.: self.eff200_mva85_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mva85_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mva85_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mva85_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1_mva85 = TCanvas()
		c1_mva85.cd()
		self.effOR_mva85_graph.SetTitle("Cut-Based Trigger Efficiency (MVA>0.85) "+tag)
		self.effOR_mva85_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_mva85_graph.Draw("AP")
		self.eff110_mva85_graph.Draw("P")
		self.eff200_mva85_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1_mva85 = TLegend(.6, .25, .9, .4)
		l1_mva85.AddEntry(self.eff110_mva85_graph, "HLT_Photon110")
		l1_mva85.AddEntry(self.eff200_mva85_graph, "HLT_Photon200")
		l1_mva85.AddEntry(self.effOR_mva85_graph, "ORed Triggers")
                l1_mva85.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1_mva85.SaveAs("./"+name+"_mva85.png")
		#c1_mva85.SaveAs("./"+name+"_mva85.root")
		c1_mva85.Close()



		self.eff200_mva9.SetLineColor(kRed)
		self.effOR_mva9.SetLineColor(kViolet)
	
		self.eff110_mva9.SetAxisRange(0,1.2, "Y")	
		self.eff200_mva9.SetAxisRange(0,1.2, "Y")	
		self.effOR_mva9.SetAxisRange(0,1.2, "Y")	
		
		self.eff200_mva9_graph = TGraphAsymmErrors(self.eff200_mva9)
		self.eff110_mva9_graph = TGraphAsymmErrors(self.eff110_mva9)
		self.effOR_mva9_graph = TGraphAsymmErrors(self.effOR_mva9)

		self.eff200_mva9_graph.SetLineWidth(2)
		self.eff110_mva9_graph.SetLineWidth(2)
		self.effOR_mva9_graph.SetLineWidth(2)
		
		self.eff200_mva9_graph.SetLineColor(kRed)
		self.eff110_mva9_graph.SetLineColor(kBlue)
		self.effOR_mva9_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.effOR_mva9_graph.GetN()):
			self.effOR_mva9_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.effOR_mva9_graph.SetPointEYhigh(n,0)
			elif yval+self.effOR_mva9_graph.GetErrorYhigh(n) > 1.: self.effOR_mva9_graph.SetPointEYhigh(n,1.-yval)
			self.eff110_mva9_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff110_mva9_graph.SetPointEYhigh(n,0)
			elif yval+self.eff110_mva9_graph.GetErrorYhigh(n) > 1.: self.eff110_mva9_graph.SetPointEYhigh(n,1.-yval)
			self.eff200_mva9_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff200_mva9_graph.SetPointEYhigh(n,0)
			elif yval+self.eff200_mva9_graph.GetErrorYhigh(n) > 1.: self.eff200_mva9_graph.SetPointEYhigh(n,1.-yval)
		
		self.effOR_mva9_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff200_mva9_graph.GetYaxis().SetRangeUser(0.2,1.1)
		self.eff110_mva9_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

		c1_mva9 = TCanvas()
		c1_mva9.cd()
		self.effOR_mva9_graph.SetTitle("Cut-Based Trigger Efficiency (MVA>0.9) "+tag)
		self.effOR_mva9_graph.GetXaxis().SetTitle("Photon pT")
		self.effOR_mva9_graph.Draw("AP")
		self.eff110_mva9_graph.Draw("P")
		self.eff200_mva9_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1_mva9 = TLegend(.6, .25, .9, .4)
		l1_mva9.AddEntry(self.eff110_mva9_graph, "HLT_Photon110")
		l1_mva9.AddEntry(self.eff200_mva9_graph, "HLT_Photon200")
		l1_mva9.AddEntry(self.effOR_mva9_graph, "ORed Triggers")
                l1_mva9.Draw()
		line1 = TLine(120, 0.2, 120, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c1_mva9.SaveAs("./"+name+"_mva9.png")
		#c1_mva9.SaveAs("./"+name+"_mva9.root")
		c1_mva9.Close()

