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

class drawRData:
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4):
		gROOT.SetBatch(True)

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.base_h1 = self.f.Get("pass_soft")
		self.base_h2 = self.f.Get("pass_jet_pt")
		self.base_h3 = self.f.Get("fail_soft")
		self.base_h4 = self.f.Get("fail_jet_pt")
		self.base_h5 = self.f.Get("softdrop")
#		self.base_h6 = self.f.Get("jet_pt")
#		self.base_h7 = self.f.Get("thin_jet_pt")
#		self.base_h8 = self.f.Get("gen_pass_soft")
#		self.base_h9 = self.f.Get("gen_pass_jet_pt")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.corr_h1 = self.g.Get("pass_soft")
		self.corr_h2 = self.g.Get("pass_jet_pt")
		self.corr_h3 = self.g.Get("fail_soft")
		self.corr_h4 = self.g.Get("fail_jet_pt")
		self.corr_h5 = self.g.Get("softdrop")
#		self.corr_h6 = self.g.Get("jet_pt")
#		self.corr_h7 = self.g.Get("thin_jet_pt")
		
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.nano_h1 = self.h.Get("pass_soft")
		self.nano_h2 = self.h.Get("pass_jet_pt")
		self.nano_h3 = self.h.Get("fail_soft")
		self.nano_h4 = self.h.Get("fail_jet_pt")
		self.nano_h5 = self.h.Get("softdrop")
#		self.nano_h6 = self.h.Get("jet_pt")
#		self.nano_h7 = self.h.Get("thin_jet_pt")
		
		self.k = TFile.Open(ifile4, "READ")
		self.k.ls();

		self.nano_corr_h1 = self.k.Get("pass_soft")
		self.nano_corr_h2 = self.k.Get("pass_jet_pt")
		self.nano_corr_h3 = self.k.Get("fail_soft")
		self.nano_corr_h4 = self.k.Get("fail_jet_pt")
		self.nano_corr_h5 = self.k.Get("softdrop")
#		self.nano_corr_h6 = self.k.Get("jet_pt")
#		self.nano_corr_h7 = self.k.Get("thin_jet_pt")

		
		#self.comb1 = TH1F("comb1", "Background Softdrop Mass", 40, 0, 200)
		
		#self.comb1.Add(self.GJp1)
		#self.comb1.Add(self.QCDp1)
		#self.comb1.Add(self.TTp1)
	
		print(self.base_h1.Integral())	
		print(self.corr_h1.Integral())	
		print(self.nano_h1.Integral())	
		print(self.nano_corr_h1.Integral())	
		
		
		self.base_h1.SetLineColor(kBlack)
		self.base_h2.SetLineColor(kBlack)
		self.base_h3.SetLineColor(kBlack)
		self.base_h4.SetLineColor(kBlack)
		self.base_h5.SetLineColor(kBlack)
#		self.base_h6.SetLineColor(kBlack)
#		self.base_h7.SetLineColor(kBlack)


		#GenJet
#		self.base_h8.SetLineColor(kOrange)
#		self.base_h9.SetLineColor(kOrange)
		
		self.corr_h1.SetLineColor(kBlue)
		self.corr_h2.SetLineColor(kBlue)
		self.corr_h3.SetLineColor(kBlue)
		self.corr_h4.SetLineColor(kBlue)
		self.corr_h5.SetLineColor(kBlue)
#		self.corr_h6.SetLineColor(kBlue)
#		self.corr_h7.SetLineColor(kBlue)
		
		self.nano_h1.SetLineColor(kRed)
		self.nano_h2.SetLineColor(kRed)
		self.nano_h3.SetLineColor(kRed)
		self.nano_h4.SetLineColor(kRed)
		self.nano_h5.SetLineColor(kRed)
#		self.nano_h6.SetLineColor(kRed)
#		self.nano_h7.SetLineColor(kRed)
		
		self.nano_corr_h1.SetLineColor(kViolet)
		self.nano_corr_h2.SetLineColor(kViolet)
		self.nano_corr_h3.SetLineColor(kViolet)
		self.nano_corr_h4.SetLineColor(kViolet)
		self.nano_corr_h5.SetLineColor(kViolet)
#		self.nano_corr_h6.SetLineColor(kViolet)
#		self.nano_corr_h7.SetLineColor(kViolet)
		
		
		

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.nano_corr_h1.SetTitle(name+" Passing Softdrop Mass")
		self.nano_corr_h1.Draw("hist")
		self.base_h1.Draw("same hist")
#		self.base_h8.Draw("same hist")
		self.corr_h1.Draw("same hist")
		self.nano_h1.Draw("same hist")
		l1 = TLegend(.6, .75, .9, .9)
		l1.AddEntry(self.base_h1, "Uncorrected")
#		l1.AddEntry(self.base_h8, "AK8 GenJet")
                l1.AddEntry(self.corr_h1, "JMC")
                l1.AddEntry(self.nano_h1, "NanoAODTools")
                l1.AddEntry(self.nano_corr_h1, "NanoAODTools+JMC")
                l1.Draw()
#		gPad.SetLogy()
		c1.SaveAs("./plots/Correction_"+name+"_pass_soft.png")
		c1.SaveAs("./plots/Correction_"+name+"_pass_soft.root")
		c1.Close()
		
		c2 = TCanvas()
		c2.cd()
		self.nano_corr_h2.SetTitle(name+" Jet pT")
		self.nano_corr_h2.Draw("hist")
		self.base_h2.Draw("same hist")
#		self.base_h9.Draw("same hist")
		self.corr_h2.Draw("same hist")
		self.nano_h2.Draw("same hist")
		l2 = TLegend(.6, .75, .9, .9)
		l2.AddEntry(self.base_h2, "Uncorrected")
#		l2.AddEntry(self.base_h9, "AK8 GenJet")
                l2.AddEntry(self.corr_h2, "JMC")
                l2.AddEntry(self.nano_h2, "NanoAODTools")
                l2.AddEntry(self.nano_corr_h2, "NanoAODTools+JMC")
                l2.Draw()
#		gPad.SetLogy()
		c2.SaveAs("./plots/Correction_"+name+"_pass_jet_pt.png")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.nano_corr_h3.SetTitle(name+" Failing Softdrop Mass")
		self.nano_corr_h3.Draw("hist")
		self.base_h3.Draw("same hist")
		self.corr_h3.Draw("same hist")
		self.nano_h3.Draw("same hist")
		l3 = TLegend(.6, .75, .9, .9)
		l3.AddEntry(self.base_h3, "Uncorrected")
                l3.AddEntry(self.corr_h3, "JMC")
                l3.AddEntry(self.nano_h3, "NanoAODTools")
                l3.AddEntry(self.nano_corr_h3, "NanoAODTools+JMC")
                l3.Draw()
#		gPad.SetLogy()
		c3.SaveAs("./plots/Correction_"+name+"_fail_soft.png")
		c3.Close()

		c4 = TCanvas()
		c4.cd()
		self.nano_corr_h4.SetTitle(name+" Failing Jet pT")
		self.nano_corr_h4.Draw("hist")
		self.base_h4.Draw("same hist")
		self.corr_h4.Draw("same hist")
		self.nano_h4.Draw("same hist")
		l4 = TLegend(.6, .75, .9, .9)
		l4.AddEntry(self.base_h4, "Uncorrected")
                l4.AddEntry(self.corr_h4, "JMC")
                l4.AddEntry(self.nano_h4, "NanoAODTools")
                l4.AddEntry(self.nano_corr_h4, "NanoAODTools+JMC")
                l4.Draw()
#		gPad.SetLogy()
		c4.SaveAs("./plots/Correction_"+name+"_fail_jet_pt.png")
		c4.Close()

		c5 = TCanvas()
		c5.cd()
		self.nano_corr_h5.SetTitle(name+" Total Softdrop Mass")
		self.nano_corr_h5.Draw("hist")
		self.base_h5.Draw("same hist")
		self.corr_h5.Draw("same hist")
		self.nano_h5.Draw("same hist")
		l5 = TLegend(.6, .75, .9, .9)
		l5.AddEntry(self.base_h5, "Uncorrected")
                l5.AddEntry(self.corr_h5, "JMC")
                l5.AddEntry(self.nano_h5, "NanoAODTools")
                l5.AddEntry(self.nano_corr_h5, "NanoAODTools+JMC")
                l5.Draw()
#		gPad.SetLogy()
		c5.SaveAs("./plots/Correction_"+name+"_tot_soft.png")
		c5.Close()

#		c6 = TCanvas()
#		c6.cd()
#		self.nano_corr_h6.SetTitle(name+" Total Jet pT")
#		self.nano_corr_h6.Draw("hist")
#		self.base_h6.Draw("same hist")
#		self.corr_h6.Draw("same hist")
#		self.nano_h6.Draw("same hist")
#		l6 = TLegend(.6, .75, .9, .9)
#		l6.AddEntry(self.base_h6, "Uncorrected")
 #               l6.AddEntry(self.corr_h6, "JMC")
  #              l6.AddEntry(self.nano_h6, "NanoAODTools")
   #             l6.AddEntry(self.nano_corr_h6, "NanoAODTools+JMC")
    #            l6.Draw()
#		gPad.SetLogy()
#		c6.SaveAs("./plots/Correction_"+name+"_tot_jet_pt.png")
#		c6.Close()

#		c7 = TCanvas()
#		c7.cd()
#		self.nano_corr_h7.SetTitle(name+" Total Thin Jet pT")
#		self.nano_corr_h7.Draw("hist")
#		self.base_h7.Draw("same hist")
#		self.corr_h7.Draw("same hist")
#		self.nano_h7.Draw("same hist")
#		l7 = TLegend(.6, .75, .9, .9)
#		l7.AddEntry(self.base_h7, "Uncorrected")
 #               l7.AddEntry(self.corr_h7, "JMC")
  #              l7.AddEntry(self.nano_h7, "NanoAODTools")
   #             l7.AddEntry(self.nano_corr_h7, "NanoAODTools+JMC")
    #            l7.Draw()
#		gPad.SetLogy()
#		c7.SaveAs("./plots/Correction_"+name+"_tot_thin_jet_pt.png")
#		c7.Close()

