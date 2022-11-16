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
                j.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
                j.SetLineWidth(2)
        return maximum*1.35
class drawRData:
	def __init__(self, name, ifile1, ifile2, t, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/"+o,"RECREATE")

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.base_h1 = self.f.Get("pass_soft")
		self.base_h2 = self.f.Get("pass_jet_pt")
		self.base_h3 = self.f.Get("fail_soft")
		self.base_h4 = self.f.Get("fail_jet_pt")

#		self.base_h5 = self.f.Get("ak4_btag")
#                self.base_h5.GetXaxis().SetRangeUser(0,1)
#		self.base_h6 = self.f.Get("METPT")
#		self.base_h7 = self.f.Get("PuppiMETPT")
		
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.corr_h1 = self.g.Get("pass_soft")
		self.corr_h2 = self.g.Get("pass_jet_pt")
		self.corr_h3 = self.g.Get("fail_soft")
		self.corr_h4 = self.g.Get("fail_jet_pt")
		
		self.corr_h5 = self.g.Get("ak4_btag")
                self.corr_h5.GetXaxis().SetRangeUser(0,1)
		self.corr_h6 = self.g.Get("METPT")
		self.corr_h7 = self.g.Get("PuppiMETPT")
	
		self.corr_h8 = self.g.Get("ak4_btag_met")
                self.corr_h8.GetXaxis().SetRangeUser(0,1)
		
		
		self.base_h1.SetLineColor(kBlue)
		self.base_h2.SetLineColor(kBlue)
		self.base_h3.SetLineColor(kBlue)
		self.base_h4.SetLineColor(kBlue)

	
	
		self.corr_h1.SetLineColor(kRed)
		self.corr_h2.SetLineColor(kRed)
		self.corr_h3.SetLineColor(kRed)
		self.corr_h4.SetLineColor(kRed)
		
		
		FindAndSetMax(self.base_h1, self.corr_h1)
		FindAndSetMax(self.base_h2, self.corr_h2)
		FindAndSetMax(self.base_h3, self.corr_h3)
		FindAndSetMax(self.base_h4, self.corr_h4)

		#FindAndSetMax(self.corr_h5)		
		#FindAndSetMax(self.corr_h6)		
		#FindAndSetMax(self.corr_h7)		

		c5 = TCanvas()
		c5.cd()
		self.corr_h5.SetTitle(name+" AK4 BTag Score")
		self.corr_h5.Draw("hist")
		c5.SaveAs("./plots/"+name+"_ak4_btag.png")
		c5.Close()

		c6 = TCanvas()
		c6.cd()
		self.corr_h6.SetTitle(name+" MET pT")
		self.corr_h6.Draw("hist")
		c6.SaveAs("./plots/"+name+"_MET_pt.png")
		c6.Close()
		
		c7 = TCanvas()
		c7.cd()
		self.corr_h7.SetTitle(name+" Puppi MET pT")
		self.corr_h7.Draw("hist")
		c7.SaveAs("./plots/"+name+"_PUPPI_MET_pt.png")
		c7.Close()
		
		c8 = TCanvas()
		c8.cd()
		self.corr_h8.SetTitle(name+" AK4 BTag Score (PUPPI MET < 75 GeV)")
		self.corr_h8.Draw("hist")
		c8.SaveAs("./plots/"+name+"_ak4_btag_met.png")
		c8.Close()

#		ROOT.gStyle.SetOptStat(0)

#		c1 = TCanvas()
#		c1.cd()
#		self.corr_h1.SetTitle(name+" Passing Softdrop Mass")
#		self.corr_h1.Draw("hist")
#		self.base_h1.Draw("same hist")
#		lin1.Draw()
#		l1 = TLegend(.6, .75, .9, .9)
#		l1.AddEntry(self.base_h1, "JEC")
 #               l1.AddEntry(self.corr_h1, "JEC and JMC")
  #              l1.Draw()
#		gPad.SetLogy()
#		c1.SaveAs("./plots/Correction_"+name+"_pass_soft.png")
#		c1.Close()
		
#		c2 = TCanvas()
#		c2.cd()
#		self.corr_h2.SetTitle(name+" Passing Jet pT")
#		self.corr_h2.Draw("hist")
#		self.base_h2.Draw("same hist")
#		l2 = TLegend(.6, .75, .9, .9)
#		l2.AddEntry(self.base_h2, "JEC")
 #               l2.AddEntry(self.corr_h2, "JEC and JMC")
  #              l2.Draw()
##		gPad.SetLogy()
#		c2.SaveAs("./plots/Correction_"+name+"_pass_jet_pt.png")
#		c2.Close()
		
#		c3 = TCanvas()
#		c3.cd()
#		self.corr_h3.SetTitle(name+" Failing Softdrop Mass")
#		self.corr_h3.Draw("hist")
#		self.base_h3.Draw("same hist")
#		l3 = TLegend(.6, .75, .9, .9)
#		l3.AddEntry(self.base_h3, "JEC")
 #               l3.AddEntry(self.corr_h3, "JEC and JMC")
  #              l3.Draw()
##		gPad.SetLogy()
#		c3.SaveAs("./plots/Correction_"+name+"_fail_soft.png")
#		c3.Close()
#
#		c4 = TCanvas()
#		c4.cd()
#		self.corr_h4.SetTitle(name+" Failing Jet pT")
#		self.corr_h4.Draw("hist")
#		self.base_h4.Draw("same hist")
#		l4 = TLegend(.6, .75, .9, .9)
#		l4.AddEntry(self.base_h4, "JEC")
 ##               l4.AddEntry(self.corr_h4, "JEC and JMC")
  #              l4.Draw()
#		gPad.SetLogy()
#		c4.SaveAs("./plots/Correction_"+name+"_fail_jet_pt.png")
#		c4.Close()


#		widebins = np.array([0,120,130,145,160,180,200,250,300,400,500,700,900,1200,1500,2000])

#		a1_base = self.f.Get("jet_pt_soft_pass_wide4_thin")
#		a2_base = self.f.Get("jet_pt_soft_fail_wide4_thin")
		
#		a1_corr = self.g.Get("jet_pt_soft_pass_wide4_thin")
#		a2_corr = self.g.Get("jet_pt_soft_fail_wide4_thin")
#		for i in range(2, 16):
#			o1_base = a1_base.ProjectionY("base_pass_"+str(i), i, i)
#			o2_base = a2_base.ProjectionY("base_fail_"+str(i), i, i)
#			
#			o1_corr = a1_corr.ProjectionY("corr_pass_"+str(i), i, i)
#			o2_corr = a2_corr.ProjectionY("corr_fail_"+str(i), i, i)
#			
#			o1_base.SetTitle(name+" JEC Passing Softdrop Mass "+str(widebins[i-1])+"-"+str(widebins[i])+" GeV pT bin")
#			o1_base.SetXTitle("Softdrop Mass")
#			o2_base.SetTitle(name+" JEC Failing Softdrop Mass "+str(widebins[i-1])+"-"+str(widebins[i])+" GeV pT bin")
#			o2_base.SetXTitle("Softdrop Mass")
#			
#			o1_corr.SetTitle(name+" JEC+JMC Passing Softdrop Mass "+str(widebins[i-1])+"-"+str(widebins[i])+" GeV pT bin")
#			o1_corr.SetXTitle("Softdrop Mass")
#			o2_corr.SetTitle(name+" JEC+JMC Failing Softdrop Mass "+str(widebins[i-1])+"-"+str(widebins[i])+" GeV pT bin")
#			o2_corr.SetXTitle("Softdrop Mass")
#			
##			ofile.WriteObject(o1_base, "base_pass_"+str(i-1))
#			ofile.WriteObject(o2_base, "base_fail_"+str(i-1))
#			ofile.WriteObject(o1_corr, "corr_pass_"+str(i-1))
#			ofile.WriteObject(o2_corr, "corr_fail_"+str(i-1))
#


