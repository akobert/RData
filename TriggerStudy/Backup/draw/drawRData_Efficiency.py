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
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, ifile7, ifile8, tag):
		gROOT.SetBatch(True)

		#background files
		
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.GJ_mva = self.f.Get("h5_mvaID")
		self.GJ_all = self.f.Get("photon_pt_allPho")
		self.GJ_mva8 = self.f.Get("photon_pt_MVA8")
		self.GJ_mva85 = self.f.Get("photon_pt_MVA85")
		self.GJ_mva9 = self.f.Get("photon_pt_MVA9")
		self.GJ_bit = self.f.Get("photon_pt_bitmap")
		
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.Data_mva = self.g.Get("h5_mvaID")
		self.Data_all = self.g.Get("photon_pt_allPho")
		self.Data_mva8 = self.g.Get("photon_pt_MVA8")
		self.Data_mva85 = self.g.Get("photon_pt_MVA85")
		self.Data_mva9 = self.g.Get("photon_pt_MVA9")
		self.Data_bit = self.g.Get("photon_pt_bitmap")
			
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.Sig25_mva = self.h.Get("h5_mvaID")
		self.Sig25_all = self.h.Get("photon_pt_allPho")
		self.Sig25_mva8 = self.h.Get("photon_pt_MVA8")
		self.Sig25_mva85 = self.h.Get("photon_pt_MVA85")
		self.Sig25_mva9 = self.h.Get("photon_pt_MVA9")
		self.Sig25_bit = self.h.Get("photon_pt_bitmap")
		
		self.i = TFile.Open(ifile4, "READ")
		self.i.ls();

		self.Sig10_mva = self.i.Get("h5_mvaID")
		self.Sig10_all = self.i.Get("photon_pt_allPho")
		self.Sig10_mva8 = self.i.Get("photon_pt_MVA8")
		self.Sig10_mva85 = self.i.Get("photon_pt_MVA85")
		self.Sig10_mva9 = self.i.Get("photon_pt_MVA9")
		self.Sig10_bit = self.i.Get("photon_pt_bitmap")
		
		self.k2 = TFile.Open(ifile5, "READ")
		self.k2.ls();

		self.Sig50_mva = self.k2.Get("h5_mvaID")
		self.Sig50_all = self.k2.Get("photon_pt_allPho")
		self.Sig50_mva8 = self.k2.Get("photon_pt_MVA8")
		self.Sig50_mva85 = self.k2.Get("photon_pt_MVA85")
		self.Sig50_mva9 = self.k2.Get("photon_pt_MVA9")
		self.Sig50_bit = self.k2.Get("photon_pt_bitmap")
		
		self.k = TFile.Open(ifile6, "READ")
		self.k.ls();

		self.Sig75_mva = self.k.Get("h5_mvaID")
		self.Sig75_all = self.k.Get("photon_pt_allPho")
		self.Sig75_mva8 = self.k.Get("photon_pt_MVA8")
		self.Sig75_mva85 = self.k.Get("photon_pt_MVA85")
		self.Sig75_mva9 = self.k.Get("photon_pt_MVA9")
		self.Sig75_bit = self.k.Get("photon_pt_bitmap")
		
		self.l = TFile.Open(ifile7, "READ")
		self.l.ls();

		self.Sig100_mva = self.l.Get("h5_mvaID")
		self.Sig100_all = self.l.Get("photon_pt_allPho")
		self.Sig100_mva8 = self.l.Get("photon_pt_MVA8")
		self.Sig100_mva85 = self.l.Get("photon_pt_MVA85")
		self.Sig100_mva9 = self.l.Get("photon_pt_MVA9")
		self.Sig100_bit = self.l.Get("photon_pt_bitmap")
		
		self.m = TFile.Open(ifile8, "READ")
		self.m.ls();

		self.Sig150_mva = self.m.Get("h5_mvaID")
		self.Sig150_all = self.m.Get("photon_pt_allPho")
		self.Sig150_mva8 = self.m.Get("photon_pt_MVA8")
		self.Sig150_mva85 = self.m.Get("photon_pt_MVA85")
		self.Sig150_mva9 = self.m.Get("photon_pt_MVA9")
		self.Sig150_bit = self.m.Get("photon_pt_bitmap")
			
		#Normalize Histograms
		self.GJ_mva.Scale(1/self.GJ_mva.Integral())
		self.Data_mva.Scale(1/self.Data_mva.Integral())
		self.Sig25_mva.Scale(1/self.Sig25_mva.Integral())
		
		self.GJ_mva.SetLineColor(kOrange)
		self.Data_mva.SetLineColor(kBlack)
		self.Sig25_mva.SetLineColor(kCyan)
	
		self.Data_mva.SetAxisRange(0,.2,"Y")

		ROOT.gInterpreter.Declare("Double_t widebins[35] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")

		self.GJ_mva8.Divide(self.GJ_all)
		self.GJ_mva85.Divide(self.GJ_all)
		self.GJ_mva9.Divide(self.GJ_all)
		self.GJ_bit.Divide(self.GJ_all)
		
		self.Sig10_mva8.Divide(self.Sig10_all)
		self.Sig10_mva85.Divide(self.Sig10_all)
		self.Sig10_mva9.Divide(self.Sig10_all)
		self.Sig10_bit.Divide(self.Sig10_all)
		
		self.Sig25_mva8.Divide(self.Sig25_all)
		self.Sig25_mva85.Divide(self.Sig25_all)
		self.Sig25_mva9.Divide(self.Sig25_all)
		self.Sig25_bit.Divide(self.Sig25_all)
		
		self.Sig50_mva8.Divide(self.Sig50_all)
		self.Sig50_mva85.Divide(self.Sig50_all)
		self.Sig50_mva9.Divide(self.Sig50_all)
		self.Sig50_bit.Divide(self.Sig50_all)
		
		self.Sig75_mva8.Divide(self.Sig75_all)
		self.Sig75_mva85.Divide(self.Sig75_all)
		self.Sig75_mva9.Divide(self.Sig75_all)
		self.Sig75_bit.Divide(self.Sig75_all)
		
		self.Sig100_mva8.Divide(self.Sig100_all)
		self.Sig100_mva85.Divide(self.Sig100_all)
		self.Sig100_mva9.Divide(self.Sig100_all)
		self.Sig100_bit.Divide(self.Sig100_all)
		
		self.Sig150_mva8.Divide(self.Sig150_all)
		self.Sig150_mva85.Divide(self.Sig150_all)
		self.Sig150_mva9.Divide(self.Sig150_all)
		self.Sig150_bit.Divide(self.Sig150_all)
		
		self.GJ_mva8.SetAxisRange(0,1.0,"Y")
		self.GJ_mva85.SetAxisRange(0,1.0,"Y")
		self.GJ_mva9.SetAxisRange(0,1.0,"Y")
		self.GJ_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig10_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig10_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig10_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig10_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig25_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig25_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig25_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig25_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig50_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig50_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig50_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig50_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig75_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig75_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig75_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig75_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig100_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig100_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig100_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig100_bit.SetAxisRange(0,1.0,"Y")
		
		self.Sig150_mva8.SetAxisRange(0,1.0,"Y")
		self.Sig150_mva85.SetAxisRange(0,1.0,"Y")
		self.Sig150_mva9.SetAxisRange(0,1.0,"Y")
		self.Sig150_bit.SetAxisRange(0,1.0,"Y")
		
		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.Data_mva.SetTitle("Normalized MVA Scores")
		self.Data_mva.SetXTitle("MVA Score")
		self.Data_mva.Draw("hist")
		self.GJ_mva.Draw("same hist")
		self.Sig25_mva.Draw("same hist")
		l1 = TLegend(.4, .75, .7, .9)
		l1.AddEntry(self.GJ_mva, "GJets")
                l1.AddEntry(self.Data_mva, "Data")
                l1.AddEntry(self.Sig25_mva, "25 GeV Signal")
                l1.Draw()
		#gPad.SetLogy()
		c1.SaveAs("./"+name+".png")
		c1.SaveAs("./"+name+".root")
		c1.Close()

		self.GJ_bit.SetLineColor(kBlue)
		self.GJ_mva8.SetLineColor(kBlack)
		self.GJ_mva85.SetLineColor(kGreen)
		self.GJ_mva9.SetLineColor(kRed)
		self.Sig10_bit.SetLineColor(kBlue)
		self.Sig10_mva8.SetLineColor(kBlack)
		self.Sig10_mva85.SetLineColor(kGreen)
		self.Sig10_mva9.SetLineColor(kRed)
		self.Sig25_bit.SetLineColor(kBlue)
		self.Sig25_mva8.SetLineColor(kBlack)
		self.Sig25_mva85.SetLineColor(kGreen)
		self.Sig25_mva9.SetLineColor(kRed)
		self.Sig50_bit.SetLineColor(kBlue)
		self.Sig50_mva8.SetLineColor(kBlack)
		self.Sig50_mva85.SetLineColor(kGreen)
		self.Sig50_mva9.SetLineColor(kRed)
		self.Sig75_bit.SetLineColor(kBlue)
		self.Sig75_mva8.SetLineColor(kBlack)
		self.Sig75_mva85.SetLineColor(kGreen)
		self.Sig75_mva9.SetLineColor(kRed)
		self.Sig100_bit.SetLineColor(kBlue)
		self.Sig100_mva8.SetLineColor(kBlack)
		self.Sig100_mva85.SetLineColor(kGreen)
		self.Sig100_mva9.SetLineColor(kRed)
		self.Sig150_bit.SetLineColor(kBlue)
		self.Sig150_mva8.SetLineColor(kBlack)
		self.Sig150_mva85.SetLineColor(kGreen)
		self.Sig150_mva9.SetLineColor(kRed)

		c2 = TCanvas()
		c2.cd()
		self.GJ_bit.SetXTitle("Photon pT")
		self.GJ_bit.SetTitle("GJets Cut Efficiency")
		self.GJ_bit.Draw("hist")
		self.GJ_mva8.Draw("same hist")
		self.GJ_mva85.Draw("same hist")
		self.GJ_mva9.Draw("same hist")
		l2 = TLegend(.6, .75, .9, .9)
		l2.AddEntry(self.GJ_bit, "CutBased")
		l2.AddEntry(self.GJ_mva8, "MVA > 0.8")
		l2.AddEntry(self.GJ_mva85, "MVA > 0.85")
		l2.AddEntry(self.GJ_mva9, "MVA > 0.9")
		l2.Draw()
		c2.SaveAs("./GJ_Eff.png")
		c2.SaveAs("./GJ_Eff.root")
		c2.Close()

                c3 = TCanvas()
                c3.cd()
                self.Sig10_bit.SetXTitle("Photon pT")
                self.Sig10_bit.SetTitle("Sig10 Cut Efficiency")
                self.Sig10_bit.Draw("hist")
                self.Sig10_mva8.Draw("same hist")
                self.Sig10_mva85.Draw("same hist")
                self.Sig10_mva9.Draw("same hist")
                l3 = TLegend(.6, .75, .9, .9)
                l3.AddEntry(self.Sig10_bit, "CutBased")
                l3.AddEntry(self.Sig10_mva8, "MVA > 0.8")
                l3.AddEntry(self.Sig10_mva85, "MVA > 0.85")
                l3.AddEntry(self.Sig10_mva9, "MVA > 0.9")
                l3.Draw()
                c3.SaveAs("./Sig10_Eff.png")
                c3.SaveAs("./Sig10_Eff.root")
                c3.Close()

		c4 = TCanvas()
		c4.cd()
		self.Sig25_bit.SetXTitle("Photon pT")
		self.Sig25_bit.SetTitle("Sig25 Cut Efficiency")
		self.Sig25_bit.Draw("hist")
		self.Sig25_mva8.Draw("same hist")
		self.Sig25_mva85.Draw("same hist")
		self.Sig25_mva9.Draw("same hist")
		l4 = TLegend(.6, .75, .9, .9)
		l4.AddEntry(self.Sig25_bit, "CutBased")
		l4.AddEntry(self.Sig25_mva8, "MVA > 0.8")
		l4.AddEntry(self.Sig25_mva85, "MVA > 0.85")
		l4.AddEntry(self.Sig25_mva9, "MVA > 0.9")
		l4.Draw()
		c4.SaveAs("./Sig25_Eff.png")
		c4.SaveAs("./Sig25_Eff.root")
		c4.Close()
		
		c5 = TCanvas()
		c5.cd()
		self.Sig50_bit.SetXTitle("Photon pT")
		self.Sig50_bit.SetTitle("Sig50 Cut Efficiency")
		self.Sig50_bit.Draw("hist")
		self.Sig50_mva8.Draw("same hist")
		self.Sig50_mva85.Draw("same hist")
		self.Sig50_mva9.Draw("same hist")
		l5 = TLegend(.6, .75, .9, .9)
		l5.AddEntry(self.Sig50_bit, "CutBased")
		l5.AddEntry(self.Sig50_mva8, "MVA > 0.8")
		l5.AddEntry(self.Sig50_mva85, "MVA > 0.85")
		l5.AddEntry(self.Sig50_mva9, "MVA > 0.9")
		l5.Draw()
		c5.SaveAs("./Sig50_Eff.png")
		c5.SaveAs("./Sig50_Eff.root")
		c5.Close()
		
		c6 = TCanvas()
		c6.cd()
		self.Sig75_bit.SetXTitle("Photon pT")
		self.Sig75_bit.SetTitle("Sig75 Cut Efficiency")
		self.Sig75_bit.Draw("hist")
		self.Sig75_mva8.Draw("same hist")
		self.Sig75_mva85.Draw("same hist")
		self.Sig75_mva9.Draw("same hist")
		l6 = TLegend(.6, .75, .9, .9)
		l6.AddEntry(self.Sig75_bit, "CutBased")
		l6.AddEntry(self.Sig75_mva8, "MVA > 0.8")
		l6.AddEntry(self.Sig75_mva85, "MVA > 0.85")
		l6.AddEntry(self.Sig75_mva9, "MVA > 0.9")
		l6.Draw()
		c6.SaveAs("./Sig75_Eff.png")
		c6.SaveAs("./Sig75_Eff.root")
		c6.Close()
		
		c7 = TCanvas()
		c7.cd()
		self.Sig100_bit.SetXTitle("Photon pT")
		self.Sig100_bit.SetTitle("Sig100 Cut Efficiency")
		self.Sig100_bit.Draw("hist")
		self.Sig100_mva8.Draw("same hist")
		self.Sig100_mva85.Draw("same hist")
		self.Sig100_mva9.Draw("same hist")
		l7 = TLegend(.6, .75, .9, .9)
		l7.AddEntry(self.Sig100_bit, "CutBased")
		l7.AddEntry(self.Sig100_mva8, "MVA > 0.8")
		l7.AddEntry(self.Sig100_mva85, "MVA > 0.85")
		l7.AddEntry(self.Sig100_mva9, "MVA > 0.9")
		l7.Draw()
		c7.SaveAs("./Sig100_Eff.png")
		c7.SaveAs("./Sig100_Eff.root")
		c7.Close()
		
		c8 = TCanvas()
		c8.cd()
		self.Sig150_bit.SetXTitle("Photon pT")
		self.Sig150_bit.SetTitle("Sig150 Cut Efficiency")
		self.Sig150_bit.Draw("hist")
		self.Sig150_mva8.Draw("same hist")
		self.Sig150_mva85.Draw("same hist")
		self.Sig150_mva9.Draw("same hist")
		l8 = TLegend(.6, .75, .9, .9)
		l8.AddEntry(self.Sig150_bit, "CutBased")
		l8.AddEntry(self.Sig150_mva8, "MVA > 0.8")
		l8.AddEntry(self.Sig150_mva85, "MVA > 0.85")
		l8.AddEntry(self.Sig150_mva9, "MVA > 0.9")
		l8.Draw()
		c8.SaveAs("./Sig150_Eff.png")
		c8.SaveAs("./Sig150_Eff.root")
		c8.Close()
		
