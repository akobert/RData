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
class drawRData:
	def __init__(self, name, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, bfile1, bfile2, bfile3, bfile4, bfile5, bfile6, bfile7, sfile_btag1, sfile_btag2, sfile_btag3, sfile_btag4, sfile_btag5, sfile_btag6, sfile_btag7, bfile_btag1, bfile_btag2, bfile_btag3, bfile_btag4, bfile_btag5, bfile_btag6, bfile_btag7, t, o, low, high):
		gROOT.SetBatch(True)

#		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/SRootB/"+o,"RECREATE")

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.h1_5 = self.f.Get("pass_soft")
		self.h2_5 = self.f.Get("pass_jet_pt")

		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.h1_10 = self.g.Get("pass_soft")
		self.h2_10 = self.g.Get("pass_jet_pt")
		
		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.h1_15 = self.h.Get("pass_soft")
		self.h2_15 = self.h.Get("pass_jet_pt")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.h1_20 = self.i.Get("pass_soft")
		self.h2_20 = self.i.Get("pass_jet_pt")
		
		self.j = TFile.Open(sfile5, "READ")
		self.j.ls();

		self.h1_25 = self.j.Get("pass_soft")
		self.h2_25 = self.j.Get("pass_jet_pt")
		
		self.k = TFile.Open(sfile6, "READ")
		self.k.ls();

		self.h1_30 = self.k.Get("pass_soft")
		self.h2_30 = self.k.Get("pass_jet_pt")
		
		self.l = TFile.Open(sfile7, "READ")
		self.l.ls();

		self.h1_50 = self.l.Get("pass_soft")
		self.h2_50 = self.l.Get("pass_jet_pt")
		
		self.bf = TFile.Open(bfile1, "READ")
		self.bf.ls();

		self.b1_5 = self.bf.Get("pass_soft")
		self.b2_5 = self.bf.Get("pass_jet_pt")

		self.bg = TFile.Open(bfile2, "READ")
		self.bg.ls();

		self.b1_10 = self.bg.Get("pass_soft")
		self.b2_10 = self.bg.Get("pass_jet_pt")
		
		self.bh = TFile.Open(bfile3, "READ")
		self.bh.ls();

		self.b1_15 = self.bh.Get("pass_soft")
		self.b2_15 = self.bh.Get("pass_jet_pt")
		
		self.bi = TFile.Open(bfile4, "READ")
		self.bi.ls();

		self.b1_20 = self.bi.Get("pass_soft")
		self.b2_20 = self.bi.Get("pass_jet_pt")
		
		self.bj = TFile.Open(bfile5, "READ")
		self.bj.ls();

		self.b1_25 = self.bj.Get("pass_soft")
		self.b2_25 = self.bj.Get("pass_jet_pt")
		
		self.bk = TFile.Open(bfile6, "READ")
		self.bk.ls();

		self.b1_30 = self.bk.Get("pass_soft")
		self.b2_30 = self.bk.Get("pass_jet_pt")
		
		self.bl = TFile.Open(bfile7, "READ")
		self.bl.ls();

		self.b1_50 = self.bl.Get("pass_soft")
		self.b2_50 = self.bl.Get("pass_jet_pt")


		self.f_btag = TFile.Open(sfile_btag1, "READ")
		self.f_btag.ls();

		self.h1_btag_5 = self.f_btag.Get("pass_soft")
		self.h2_btag_5 = self.f_btag.Get("pass_jet_pt")

		self.g_btag = TFile.Open(sfile_btag2, "READ")
		self.g_btag.ls();

		self.h1_btag_10 = self.g_btag.Get("pass_soft")
		self.h2_btag_10 = self.g_btag.Get("pass_jet_pt")
		
		self.h_btag = TFile.Open(sfile_btag3, "READ")
		self.h_btag.ls();

		self.h1_btag_15 = self.h_btag.Get("pass_soft")
		self.h2_btag_15 = self.h_btag.Get("pass_jet_pt")
		
		self.i_btag = TFile.Open(sfile_btag4, "READ")
		self.i_btag.ls();

		self.h1_btag_20 = self.i_btag.Get("pass_soft")
		self.h2_btag_20 = self.i_btag.Get("pass_jet_pt")
		
		self.j_btag = TFile.Open(sfile_btag5, "READ")
		self.j_btag.ls();

		self.h1_btag_25 = self.j_btag.Get("pass_soft")
		self.h2_btag_25 = self.j_btag.Get("pass_jet_pt")
		
		self.k_btag = TFile.Open(sfile_btag6, "READ")
		self.k_btag.ls();

		self.h1_btag_30 = self.k_btag.Get("pass_soft")
		self.h2_btag_30 = self.k_btag.Get("pass_jet_pt")
		
		self.l_btag = TFile.Open(sfile_btag7, "READ")
		self.l_btag.ls();

		self.h1_btag_50 = self.l_btag.Get("pass_soft")
		self.h2_btag_50 = self.l_btag.Get("pass_jet_pt")
		
		self.bf_btag = TFile.Open(bfile_btag1, "READ")
		self.bf_btag.ls();

		self.b1_btag_5 = self.bf_btag.Get("pass_soft")
		self.b2_btag_5 = self.bf_btag.Get("pass_jet_pt")

		self.bg_btag = TFile.Open(bfile_btag2, "READ")
		self.bg_btag.ls();

		self.b1_btag_10 = self.bg_btag.Get("pass_soft")
		self.b2_btag_10 = self.bg_btag.Get("pass_jet_pt")
		
		self.bh_btag = TFile.Open(bfile_btag3, "READ")
		self.bh_btag.ls();

		self.b1_btag_15 = self.bh_btag.Get("pass_soft")
		self.b2_btag_15 = self.bh_btag.Get("pass_jet_pt")
		
		self.bi_btag = TFile.Open(bfile_btag4, "READ")
		self.bi_btag.ls();

		self.b1_btag_20 = self.bi_btag.Get("pass_soft")
		self.b2_btag_20 = self.bi_btag.Get("pass_jet_pt")
		
		self.bj_btag = TFile.Open(bfile_btag5, "READ")
		self.bj_btag.ls();

		self.b1_btag_25 = self.bj_btag.Get("pass_soft")
		self.b2_btag_25 = self.bj_btag.Get("pass_jet_pt")
		
		self.bk_btag = TFile.Open(bfile_btag6, "READ")
		self.bk_btag.ls();

		self.b1_btag_30 = self.bk_btag.Get("pass_soft")
		self.b2_btag_30 = self.bk_btag.Get("pass_jet_pt")
		
		self.bl_btag = TFile.Open(bfile_btag7, "READ")
		self.bl_btag.ls();

		self.b1_btag_50 = self.bl_btag.Get("pass_soft")
		self.b2_btag_50 = self.bl_btag.Get("pass_jet_pt")
		
		sig_low = self.b1_20.GetXaxis().FindBin(low)
		sig_high = self.b1_20.GetXaxis().FindBin(high)

	

		S5 = self.h1_5.Integral(sig_low, sig_high)
		S10 = self.h1_10.Integral(sig_low, sig_high)
		S15 = self.h1_15.Integral(sig_low, sig_high)
		S20 = self.h1_20.Integral(sig_low, sig_high)
		S25 = self.h1_25.Integral(sig_low, sig_high)
		S30 = self.h1_30.Integral(sig_low, sig_high)
		S50 = self.h1_50.Integral(sig_low, sig_high)
		
		S5_btag = self.h1_btag_5.Integral(sig_low, sig_high)
		S10_btag = self.h1_btag_10.Integral(sig_low, sig_high)
		S15_btag = self.h1_btag_15.Integral(sig_low, sig_high)
		S20_btag = self.h1_btag_20.Integral(sig_low, sig_high)
		S25_btag = self.h1_btag_25.Integral(sig_low, sig_high)
		S30_btag = self.h1_btag_30.Integral(sig_low, sig_high)
		S50_btag = self.h1_btag_50.Integral(sig_low, sig_high)
		
		B5 = self.b1_5.Integral(sig_low, sig_high)
		B10 = self.b1_10.Integral(sig_low, sig_high)
		B15 = self.b1_15.Integral(sig_low, sig_high)
		B20 = self.b1_20.Integral(sig_low, sig_high)
		B25 = self.b1_25.Integral(sig_low, sig_high)
		B30 = self.b1_30.Integral(sig_low, sig_high)
		B50 = self.b1_50.Integral(sig_low, sig_high)
		
		B5_btag = self.b1_btag_5.Integral(sig_low, sig_high)
		B10_btag = self.b1_btag_10.Integral(sig_low, sig_high)
		B15_btag = self.b1_btag_15.Integral(sig_low, sig_high)
		B20_btag = self.b1_btag_20.Integral(sig_low, sig_high)
		B25_btag = self.b1_btag_25.Integral(sig_low, sig_high)
		B30_btag = self.b1_btag_30.Integral(sig_low, sig_high)
		B50_btag = self.b1_btag_50.Integral(sig_low, sig_high)

		SRB5 = S5/sqrt(B5)
		SRB10 = S10/sqrt(B10)
		SRB15 = S15/sqrt(B15)
		SRB20 = S20/sqrt(B20)
		SRB25 = S25/sqrt(B25)
		SRB30 = S30/sqrt(B30)
		SRB50 = S50/sqrt(B50)
		
		SRB5_btag = S5_btag/sqrt(B5_btag)
		SRB10_btag = S10_btag/sqrt(B10_btag)
		SRB15_btag = S15_btag/sqrt(B15_btag)
		SRB20_btag = S20_btag/sqrt(B20_btag)
		SRB25_btag = S25_btag/sqrt(B25_btag)
		SRB30_btag = S30_btag/sqrt(B30_btag)
		SRB50_btag = S50_btag/sqrt(B50_btag)


		ROOT.gStyle.SetOptStat(0)



		self.SRB = TGraph(7)
		self.SRB.SetPoint(1,5,SRB5)
		self.SRB.SetPoint(2,10,SRB10)
		self.SRB.SetPoint(3,15,SRB15)
		self.SRB.SetPoint(4,20,SRB20)
		self.SRB.SetPoint(5,25,SRB25)
		self.SRB.SetPoint(6,30,SRB30)
		self.SRB.SetPoint(7,50,SRB50)
		self.SRB.SetTitle("S/Root(B) For "+name+" Sample;DDT%;S/Root(B)")
		
		self.SRB.SetLineColor(kBlue)

		self.SRB_btag = TGraph(7)
		self.SRB_btag.SetPoint(1,5,SRB5_btag)
		self.SRB_btag.SetPoint(2,10,SRB10_btag)
		self.SRB_btag.SetPoint(3,15,SRB15_btag)
		self.SRB_btag.SetPoint(4,20,SRB20_btag)
		self.SRB_btag.SetPoint(5,25,SRB25_btag)
		self.SRB_btag.SetPoint(6,30,SRB30_btag)
		self.SRB_btag.SetPoint(7,50,SRB50_btag)
		self.SRB_btag.SetTitle("S/Root(B) For "+name+" Sample;DDT%;S/Root(B)")
		
		self.SRB_btag.SetLineColor(kRed)

		c_srb = TCanvas()
		c_srb.cd()
		self.SRB.Draw("AL*")
		self.SRB_btag.Draw("AL* same")

                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.SRB, "S/Root(B) No B-Veto")
                l1.AddEntry(self.SRB_btag, "S/Root(B) B-Veto")
                l1.Draw()

		c_srb.SaveAs("./plots/SRB_"+name+"_all_.png")
		c_srb.Close()
		
