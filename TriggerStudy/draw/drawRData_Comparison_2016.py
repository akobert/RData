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
        	
		LUMI = 36.31
        	cmsextra = "Preliminary"

		#background files
		
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.hist_175_cut = self.f.Get("photon_pt_175")
		self.notrig_cut = self.f.Get("photon_pt_notrig")

		
		self.hist_175_mva = self.f.Get("photon_pt_175_mva8")
		self.notrig_mva = self.f.Get("photon_pt_notrig_mva8")

		self.hist_175_mva2 = self.f.Get("photon_pt_175_mva85")
		self.notrig_mva2 = self.f.Get("photon_pt_notrig_mva85")

		self.hist_175_mva3 = self.f.Get("photon_pt_175_mva9")
		self.notrig_mva3 = self.f.Get("photon_pt_notrig_mva9")
		
		self.pt_eta_notrig = self.f.Get("photon_pt_eta_notrig")
		self.pt_eta_175 = self.f.Get("photon_pt_eta_175")

		ROOT.gInterpreter.Declare("Double_t widebins[31] = {0, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 215, 225, 235, 245, 255, 270, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")


		self.eff175_cut = TH1F("eff175_cut", "Photon Trigger Efficiency "+tag, 30, widebins)
		self.eff175_mva = TH1F("eff175_mva", "Photon Trigger Efficiency "+tag, 30, widebins)
                self.eff175_mva2 = TH1F("eff175_mva2", "Photon Trigger Efficiency "+tag, 30, widebins)
                self.eff175_mva3 = TH1F("eff175_mva3", "Photon Trigger Efficiency "+tag, 30, widebins)

                for i in range(1, self.eff175_cut.GetNbinsX()+1):

                        if self.hist_175_cut.GetBinContent(i) != 0 and self.notrig_cut.GetBinContent(i) != 0:
                                self.eff175_cut.SetBinContent(i, self.hist_175_cut.GetBinContent(i)/self.notrig_cut.GetBinContent(i))
				err_check = error(self.hist_175_cut.GetBinContent(i), self.notrig_cut.GetBinContent(i))
                                self.eff175_cut.SetBinError(i, error(self.hist_175_cut.GetBinContent(i), self.notrig_cut.GetBinContent(i)))
				print("175_cut bin: "+str(i)+" value: "+str(self.eff175_cut.GetBinContent(i)))
				print("175_cut bin: "+str(i)+" value error: "+str(self.eff175_cut.GetBinError(i)))
				print("175_cut bin: "+str(i)+" error check: "+str(err_check))
                        if self.hist_175_mva.GetBinContent(i) != 0 and self.notrig_mva.GetBinContent(i) != 0:
                                self.eff175_mva.SetBinContent(i, self.hist_175_mva.GetBinContent(i)/self.notrig_mva.GetBinContent(i))
                                self.eff175_mva.SetBinError(i, error(self.hist_175_mva.GetBinContent(i), self.notrig_mva.GetBinContent(i)))
				print("175_mva bin: "+str(i)+" value: "+str(self.eff175_mva.GetBinContent(i)))
                        if self.hist_175_mva2.GetBinContent(i) != 0 and self.notrig_mva2.GetBinContent(i) != 0:
                                self.eff175_mva2.SetBinContent(i, self.hist_175_mva2.GetBinContent(i)/self.notrig_mva2.GetBinContent(i))
                                self.eff175_mva2.SetBinError(i, error(self.hist_175_mva2.GetBinContent(i), self.notrig_mva2.GetBinContent(i)))
				print("175_mva2 bin: "+str(i)+" value: "+str(self.eff175_mva2.GetBinContent(i)))
                        if self.hist_175_mva3.GetBinContent(i) != 0 and self.notrig_mva3.GetBinContent(i) != 0:
                                self.eff175_mva3.SetBinContent(i, self.hist_175_mva3.GetBinContent(i)/self.notrig_mva3.GetBinContent(i))
                                self.eff175_mva3.SetBinError(i, error(self.hist_175_mva3.GetBinContent(i), self.notrig_mva3.GetBinContent(i)))
				print("175_mva3 bin: "+str(i)+" value: "+str(self.eff175_mva3.GetBinContent(i)))
		
	
		
		self.eff175_cut.SetLineColor(kBlue)
		self.eff175_mva.SetLineColor(kBlack)
		self.eff175_mva2.SetLineColor(kGreen)
		self.eff175_mva3.SetLineColor(kRed)
	
		#self.eff175_cut.SetAxisRange(0.9,1.1,"Y")
		self.eff175_cut.SetAxisRange(0.2,1.1,"Y")


		self.eff175_cut_graph = TGraphAsymmErrors(self.eff175_cut)
		self.eff175_mva_graph = TGraphAsymmErrors(self.eff175_mva)
		self.eff175_mva2_graph = TGraphAsymmErrors(self.eff175_mva2)
		self.eff175_mva3_graph = TGraphAsymmErrors(self.eff175_mva3)

		self.eff175_cut_graph.SetLineWidth(2)
		self.eff175_mva_graph.SetLineWidth(2)
		self.eff175_mva2_graph.SetLineWidth(2)
		self.eff175_mva3_graph.SetLineWidth(2)
		
		self.eff175_cut_graph.SetLineColor(kBlue)
		self.eff175_mva_graph.SetLineColor(kBlack)
		self.eff175_mva2_graph.SetLineColor(kGreen)
		self.eff175_mva3_graph.SetLineColor(kRed)
		
		#Fix upper bound of errors
                xval,yval = np.array(0.,dtype='double'), np.array(0.,dtype='double')
		for n in range(self.eff175_cut_graph.GetN()):
			self.eff175_cut_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_cut_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_cut_graph.GetErrorYhigh(n) > 1.: self.eff175_cut_graph.SetPointEYhigh(n,1.-yval)
			self.eff175_mva_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_mva_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_mva_graph.GetErrorYhigh(n) > 1.: self.eff175_mva_graph.SetPointEYhigh(n,1.-yval)
			self.eff175_mva2_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_mva2_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_mva2_graph.GetErrorYhigh(n) > 1.: self.eff175_mva2_graph.SetPointEYhigh(n,1.-yval)
			self.eff175_mva3_graph.GetPoint(n, xval, yval)
			if yval >= 1.: self.eff175_mva3_graph.SetPointEYhigh(n,0)
			elif yval+self.eff175_mva3_graph.GetErrorYhigh(n) > 1.: self.eff175_mva3_graph.SetPointEYhigh(n,1.-yval)
		
		self.eff175_cut_graph.GetYaxis().SetRangeUser(0.2,1.1)

		ROOT.gStyle.SetOptStat(0)

#		c1 = TCanvas()
#		c1.cd()
#		self.eff175_cut.SetTitle("175 Trigger Efficiency "+tag)
#		self.eff175_cut.SetXTitle("Photon pT")
#		self.eff175_cut.Draw("histe")
#		self.eff175_mva.Draw("same histe")
#		self.eff175_mva2.Draw("same histe")
#		self.eff175_mva3.Draw("same histe")
#		l1 = TLegend(.6, .25, .9, .4)
#		l1.AddEntry(self.eff175_cut, "Cut Based")
 #               l1.AddEntry(self.eff175_mva, "MVA > .8")
  #              l1.AddEntry(self.eff175_mva2, "MVA > .85")
   #             l1.AddEntry(self.eff175_mva3, "MVA > .9")
    #            l1.Draw()
		#gPad.SetLogy()
#		c1.SaveAs("./"+name+".png")
#		c1.SaveAs("./"+name+".root")
#		c1.Close()
		
		c1 = TCanvas()
		c1.cd()
		self.eff175_cut_graph.SetTitle("HLT_Photon175 Trigger Efficiency "+tag)
		self.eff175_cut_graph.GetXaxis().SetTitle("Photon pT")
		self.eff175_cut_graph.Draw("AP")
		self.eff175_mva_graph.Draw("P")
		self.eff175_mva2_graph.Draw("P")
		self.eff175_mva3_graph.Draw("P")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		l1 = TLegend(.6, .25, .9, .4)
		l1.AddEntry(self.eff175_cut_graph, "Cut Based")
		l1.AddEntry(self.eff175_mva_graph, "MVA > .8")
		l1.AddEntry(self.eff175_mva2_graph, "MVA > .85")
		l1.AddEntry(self.eff175_mva3_graph, "MVA > .9")
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
		
		c1 = TCanvas()
		c1.cd()
		self.eff175_cut_graph.SetTitle("CutBased HLT_Photon175 Trigger Efficiency "+tag)
		self.eff175_cut_graph.GetXaxis().SetTitle("Photon pT")
		self.eff175_cut_graph.Draw("AP")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		#gPad.SetLogy()
		line1 = TLine(200, 0.2, 200, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		c1.SaveAs("./"+name+"_cut.png")
#		c1.SaveAs("./"+name+".root")
		c1.Close()
		
		for i in range(1, self.pt_eta_175.GetNbinsX()+1):
			for j in range(1, self.pt_eta_175.GetNbinsY()+1):
				if self.pt_eta_175.GetBinContent(i,j) > 0 and self.pt_eta_notrig.GetBinContent(i,j) > 0:
					self.pt_eta_175.SetBinContent(i, j, self.pt_eta_175.GetBinContent(i,j)/self.pt_eta_notrig.GetBinContent(i,j))
				else:
					self.pt_eta_175.SetBinContent(i, j, 0)
		
		
		c3 = TCanvas()
		c3.cd()
		self.pt_eta_175.SetTitle("CutBased Photon175 Efficiency Photon Eta vs. Photon pT "+tag)
		self.pt_eta_175.SetXTitle("Photon Eta")
		self.pt_eta_175.SetYTitle("Photon pT")
		self.pt_eta_175.Draw("COLZ")
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
		line1 = TLine(200, 0.2, 200, 1.1)
		line1.SetLineColor(kBlack)
#		line1.SetLineWidth(2)
		line1.SetLineStyle(7)
		line1.Draw("same")
		#gPad.SetLogy()
		c3.SaveAs("./"+name+"_pt_eta_175.png")
		c3.Close()
		
