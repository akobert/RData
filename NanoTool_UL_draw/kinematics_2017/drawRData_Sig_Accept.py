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
	def __init__(self, name, Mass, All, Pass, Fail, Total, tag):
		gROOT.SetBatch(True)
        	LUMI = 41.48
        	cmsextra = "Preliminary"

		
		self.tot_events = TGraphErrors(8) #Total Generated Events
		self.all_events = TGraphErrors(8) #Selection Criteria Passsed
		self.pass_events = TGraphErrors(8) #Passing N2DDT
		self.fail_events = TGraphErrors(8) #Failling N2DDT
		self.accept = TGraphErrors(8) #Passing Over Total
		self.ratio = TGraphErrors(8) #Passing Over All
		self.sel_ratio = TGraphErrors(8) #Selected Over All

		self.tot_events.SetLineWidth(2)
		self.all_events.SetLineWidth(2)
		self.pass_events.SetLineWidth(2)
		self.fail_events.SetLineWidth(2)
		self.accept.SetLineWidth(2)
		self.ratio.SetLineWidth(2)
		self.sel_ratio.SetLineWidth(2)
		
		self.tot_events.SetMarkerSize(3)
		self.all_events.SetMarkerSize(3)
		self.pass_events.SetMarkerSize(3)
		self.fail_events.SetMarkerSize(3)
		self.accept.SetMarkerSize(3)
		self.ratio.SetMarkerSize(3)
		self.sel_ratio.SetMarkerSize(3)

		self.tot_events.SetMarkerStyle(1)
		self.all_events.SetMarkerStyle(1)
		self.pass_events.SetMarkerStyle(1)
		self.fail_events.SetMarkerStyle(1)
		self.accept.SetMarkerStyle(1)
		self.ratio.SetMarkerStyle(1)
		self.sel_ratio.SetMarkerStyle(1)
		
		
	#	self.eff200_graph.SetLineColor(kRed)
	#	self.eff110_graph.SetLineColor(kBlue)
	#	self.effOR_graph.SetLineColor(kViolet)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.tot_events.GetN()):
			self.tot_events.SetPoint(n, Mass[n], Total[n])
			self.all_events.SetPoint(n, Mass[n], All[n])
			self.pass_events.SetPoint(n, Mass[n], Pass[n])
			self.fail_events.SetPoint(n, Mass[n], Fail[n])
			self.accept.SetPoint(n, Mass[n], Pass[n]/Total[n])
			self.ratio.SetPoint(n, Mass[n], Pass[n]/All[n])
			self.sel_ratio.SetPoint(n, Mass[n], All[n]/Total[n])
			
			self.tot_events.SetPointError(n, 2, sqrt(Total[n]))
			self.all_events.SetPointError(n, 2, sqrt(All[n]))
			self.pass_events.SetPointError(n, 2, sqrt(Pass[n]))
			self.fail_events.SetPointError(n, 2, sqrt(Fail[n]))
			self.accept.SetPointError(n, 2, error(Pass[n], Total[n]))
			self.ratio.SetPointError(n, 2, error(Pass[n], All[n]))
			self.sel_ratio.SetPointError(n, 2, error(All[n], Total[n]))
			

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.tot_events.SetTitle("Total Generated Events vs. Signal Mass "+tag)
		self.tot_events.GetXaxis().SetTitle("Signal Mass")
		self.tot_events.GetYaxis().SetTitle("Generated Events")
		self.tot_events.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c1.SaveAs("./"+name+"_Total_2017.png")
		c1.Close()

		c2 = TCanvas()
		c2.cd()
		self.all_events.SetTitle("Events Passing Selection Criteria vs. Signal Mass "+tag)
		self.all_events.GetXaxis().SetTitle("Signal Mass")
		self.all_events.GetYaxis().SetTitle("Events Passing Selection Criteria")
		self.all_events.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c2.SaveAs("./"+name+"_All_2017.png")
		c2.Close()

		c3 = TCanvas()
		c3.cd()
		self.pass_events.SetTitle("Events Passing N2DDT Cut vs. Signal Mass "+tag)
		self.pass_events.GetXaxis().SetTitle("Signal Mass")
		self.pass_events.GetYaxis().SetTitle("Events Passing N2DDT")
		self.pass_events.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c3.SaveAs("./"+name+"_Pass_2017.png")
		c3.Close()

		c4 = TCanvas()
		c4.cd()
		self.fail_events.SetTitle("Events Failing N2DDT Cut vs. Signal Mass "+tag)
		self.fail_events.GetXaxis().SetTitle("Signal Mass")
		self.fail_events.GetYaxis().SetTitle("Events Failing N2DDT")
		self.fail_events.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c4.SaveAs("./"+name+"_Fail_2017.png")
		c4.Close()
		
		c5 = TCanvas()
		c5.cd()
		self.accept.SetTitle("Events Passing N2DDT Cut / Total Events vs. Signal Mass "+tag)
		self.accept.GetXaxis().SetTitle("Signal Mass")
		self.accept.GetYaxis().SetTitle("Accepted Ratio")
		self.accept.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c5.SaveAs("./"+name+"_Accept_2017.png")
		c5.Close()

		c6 = TCanvas()
		c6.cd()
		self.ratio.SetTitle("Events Passing N2DDT Cut / Selected Events vs. Signal Mass "+tag)
		self.ratio.GetXaxis().SetTitle("Signal Mass")
		self.ratio.GetYaxis().SetTitle("Passing Ratio")
		self.ratio.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c6.SaveAs("./"+name+"_Pass_Ratio_2017.png")
		c6.Close()

		c7 = TCanvas()
		c7.cd()
		self.sel_ratio.SetTitle("Events Passing Selection Criteria / Total Events vs. Signal Mass "+tag)
		self.sel_ratio.GetXaxis().SetTitle("Signal Mass")
		self.sel_ratio.GetYaxis().SetTitle("Selection Ratio")
		self.sel_ratio.Draw("ALP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		c7.SaveAs("./"+name+"_Selected_Ratio_2017.png")
		c7.Close()



