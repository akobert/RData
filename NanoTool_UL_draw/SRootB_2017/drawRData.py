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
	def __init__(self, name, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, bfile1, bfile2, bfile3, bfile4, bfile5, bfile6, bfile7, t, o, low, high):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/SRootB_2017/"+o,"RECREATE")

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.h1_5 = self.f.Get("pass_soft")
		self.h2_5 = self.f.Get("pass_jet_pt")
#		self.h3_5 = self.f.Get("jet_pt_soft_pass_wide4_wide")

		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.h1_10 = self.g.Get("pass_soft")
		self.h2_10 = self.g.Get("pass_jet_pt")
#		self.h3_10 = self.g.Get("jet_pt_soft_pass_wide4_wide")
		
		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.h1_15 = self.h.Get("pass_soft")
		self.h2_15 = self.h.Get("pass_jet_pt")
#		self.h3_15 = self.h.Get("jet_pt_soft_pass_wide4_wide")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.h1_20 = self.i.Get("pass_soft")
		self.h2_20 = self.i.Get("pass_jet_pt")
#		self.h3_20 = self.i.Get("jet_pt_soft_pass_wide4_wide")
		
		self.j = TFile.Open(sfile5, "READ")
		self.j.ls();

		self.h1_25 = self.j.Get("pass_soft")
		self.h2_25 = self.j.Get("pass_jet_pt")
#		self.h3_25 = self.j.Get("jet_pt_soft_pass_wide4_wide")
		
		self.k = TFile.Open(sfile6, "READ")
		self.k.ls();

		self.h1_30 = self.k.Get("pass_soft")
		self.h2_30 = self.k.Get("pass_jet_pt")
#		self.h3_30 = self.k.Get("jet_pt_soft_pass_wide4_wide")
		
		self.l = TFile.Open(sfile7, "READ")
		self.l.ls();

		self.h1_50 = self.l.Get("pass_soft")
		self.h2_50 = self.l.Get("pass_jet_pt")
#		self.h3_50 = self.l.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bf = TFile.Open(bfile1, "READ")
		self.bf.ls();

		self.b1_5 = self.bf.Get("pass_soft")
		self.b2_5 = self.bf.Get("pass_jet_pt")
#		self.b3_5 = self.bf.Get("jet_pt_soft_pass_wide4_wide")

		self.bg = TFile.Open(bfile2, "READ")
		self.bg.ls();

		self.b1_10 = self.bg.Get("pass_soft")
		self.b2_10 = self.bg.Get("pass_jet_pt")
#		self.b3_10 = self.bg.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bh = TFile.Open(bfile3, "READ")
		self.bh.ls();

		self.b1_15 = self.bh.Get("pass_soft")
		self.b2_15 = self.bh.Get("pass_jet_pt")
#		self.b3_15 = self.bh.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bi = TFile.Open(bfile4, "READ")
		self.bi.ls();

		self.b1_20 = self.bi.Get("pass_soft")
		self.b2_20 = self.bi.Get("pass_jet_pt")
#		self.b3_20 = self.bi.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bj = TFile.Open(bfile5, "READ")
		self.bj.ls();

		self.b1_25 = self.bj.Get("pass_soft")
		self.b2_25 = self.bj.Get("pass_jet_pt")
#		self.b3_25 = self.bj.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bk = TFile.Open(bfile6, "READ")
		self.bk.ls();

		self.b1_30 = self.bk.Get("pass_soft")
		self.b2_30 = self.bk.Get("pass_jet_pt")
#		self.b3_30 = self.bk.Get("jet_pt_soft_pass_wide4_wide")
		
		self.bl = TFile.Open(bfile7, "READ")
		self.bl.ls();

		self.b1_50 = self.bl.Get("pass_soft")
		self.b2_50 = self.bl.Get("pass_jet_pt")
#		self.b3_50 = self.bl.Get("jet_pt_soft_pass_wide4_wide")
		
		sig_low = self.b1_20.GetXaxis().FindBin(low)
		sig_high = self.b1_20.GetXaxis().FindBin(high)

	
		self.b1_5.SetLineColor(kRed)
		self.b2_5.SetLineColor(kRed)
		self.b1_10.SetLineColor(kRed)
		self.b2_10.SetLineColor(kRed)
		self.b1_15.SetLineColor(kRed)
		self.b2_15.SetLineColor(kRed)
		self.b1_20.SetLineColor(kRed)
		self.b2_20.SetLineColor(kRed)
		self.b1_25.SetLineColor(kRed)
		self.b2_25.SetLineColor(kRed)
		self.b1_30.SetLineColor(kRed)
		self.b2_30.SetLineColor(kRed)
		self.b1_50.SetLineColor(kRed)
		self.b2_50.SetLineColor(kRed)
	
#		self.h3_5_highpt = self.h3_5.ProjectionY("sdm_5ddt_highpt", 6, 15)
#		self.h3_10_highpt = self.h3_10.ProjectionY("sdm_10ddt_highpt", 6, 15)
#		self.h3_15_highpt = self.h3_15.ProjectionY("sdm_15ddt_highpt", 6, 15)
#		self.h3_20_highpt = self.h3_20.ProjectionY("sdm_20ddt_highpt", 6, 15)
#		self.h3_25_highpt = self.h3_25.ProjectionY("sdm_25ddt_highpt", 6, 15)
#		self.h3_30_highpt = self.h3_30.ProjectionY("sdm_30ddt_highpt", 6, 15)
#		self.h3_50_highpt = self.h3_50.ProjectionY("sdm_50ddt_highpt", 6, 15)
		
#		self.b3_5_highpt = self.b3_5.ProjectionY("sdm_back_5ddt_highpt", 6, 15)
#		self.b3_10_highpt = self.b3_10.ProjectionY("sdm_back_10ddt_highpt", 6, 15)
#		self.b3_15_highpt = self.b3_15.ProjectionY("sdm_back_15ddt_highpt", 6, 15)
#		self.b3_20_highpt = self.b3_20.ProjectionY("sdm_back_20ddt_highpt", 6, 15)
#		self.b3_25_highpt = self.b3_25.ProjectionY("sdm_back_25ddt_highpt", 6, 15)
#		self.b3_30_highpt = self.b3_30.ProjectionY("sdm_back_30ddt_highpt", 6, 15)
#		self.b3_50_highpt = self.b3_50.ProjectionY("sdm_back_50ddt_highpt", 6, 15)
			
		
		FindAndSetMax(self.b1_5, self.h1_5)
		FindAndSetMax(self.b1_10, self.h1_10)
		FindAndSetMax(self.b1_15, self.h1_15)
		FindAndSetMax(self.b1_20, self.h1_20)
		FindAndSetMax(self.b1_25, self.h1_25)
		FindAndSetMax(self.b1_30, self.h1_30)
		FindAndSetMax(self.b1_50, self.h1_50)

		S5 = self.h1_5.Integral(sig_low, sig_high)
		S10 = self.h1_10.Integral(sig_low, sig_high)
		S15 = self.h1_15.Integral(sig_low, sig_high)
		S20 = self.h1_20.Integral(sig_low, sig_high)
		S25 = self.h1_25.Integral(sig_low, sig_high)
		S30 = self.h1_30.Integral(sig_low, sig_high)
		S50 = self.h1_50.Integral(sig_low, sig_high)
		
#		S5_high = self.h3_5_highpt.Integral(sig_low, sig_high)
#		S10_high = self.h3_10_highpt.Integral(sig_low, sig_high)
#		S15_high = self.h3_15_highpt.Integral(sig_low, sig_high)
#		S20_high = self.h3_20_highpt.Integral(sig_low, sig_high)
#		S25_high = self.h3_25_highpt.Integral(sig_low, sig_high)
#		S30_high = self.h3_30_highpt.Integral(sig_low, sig_high)
#		S50_high = self.h3_50_highpt.Integral(sig_low, sig_high)
		
		B5 = self.b1_5.Integral(sig_low, sig_high)
		B10 = self.b1_10.Integral(sig_low, sig_high)
		B15 = self.b1_15.Integral(sig_low, sig_high)
		B20 = self.b1_20.Integral(sig_low, sig_high)
		B25 = self.b1_25.Integral(sig_low, sig_high)
		B30 = self.b1_30.Integral(sig_low, sig_high)
		B50 = self.b1_50.Integral(sig_low, sig_high)
		
#		B5_high = self.b3_5_highpt.Integral(sig_low, sig_high)
#		B10_high = self.b3_10_highpt.Integral(sig_low, sig_high)
#		B15_high = self.b3_15_highpt.Integral(sig_low, sig_high)
#		B20_high = self.b3_20_highpt.Integral(sig_low, sig_high)
#		B25_high = self.b3_25_highpt.Integral(sig_low, sig_high)
#		B30_high = self.b3_30_highpt.Integral(sig_low, sig_high)
#		B50_high = self.b3_50_highpt.Integral(sig_low, sig_high)

		SRB5 = S5/sqrt(B5)
		SRB10 = S10/sqrt(B10)
		SRB15 = S15/sqrt(B15)
		SRB20 = S20/sqrt(B20)
		SRB25 = S25/sqrt(B25)
		SRB30 = S30/sqrt(B30)
		SRB50 = S50/sqrt(B50)
		
#		SRB5_high = S5_high/sqrt(B5_high)
#		SRB10_high = S10_high/sqrt(B10_high)
#		SRB15_high = S15_high/sqrt(B15_high)
#		SRB20_high = S20_high/sqrt(B20_high)
#		SRB25_high = S25_high/sqrt(B25_high)
#		SRB30_high = S30_high/sqrt(B30_high)
#		SRB50_high = S50_high/sqrt(B50_high)


		print("S5: "+str(S5)+" B5: "+str(B5))
		print("S10: "+str(S10)+" B10: "+str(B10))
		print("S15: "+str(S15)+" B15: "+str(B15))
		print("S20: "+str(S20)+" B20: "+str(B20))
		print("S25: "+str(S25)+" B25: "+str(B25))
		print("S30: "+str(S30)+" B30: "+str(B30))
		print("S50: "+str(S50)+" B50: "+str(B50))
		
#		print("S5_high: "+str(S5_high)+" B5_high: "+str(B5_high))
#		print("S10_high: "+str(S10_high)+" B10_high: "+str(B10_high))
#		print("S15_high: "+str(S15_high)+" B15_high: "+str(B15_high))
#		print("S20_high: "+str(S20_high)+" B20_high: "+str(B20_high))
#		print("S25_high: "+str(S25_high)+" B25_high: "+str(B25_high))
#		print("S30_high: "+str(S30_high)+" B30_high: "+str(B30_high))
#		print("S50_high: "+str(S50_high)+" B50_high: "+str(B50_high))

		ROOT.gStyle.SetOptStat(0)


		c5 = TCanvas()
		c5.cd()
                gPad.SetLogy()
		self.b1_5.SetTitle(name+" S/Root(B) 5% DDT")
		self.b1_5.Draw("hist")
		self.h1_5.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_5.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_5.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_5, name+" Signal")
                l1.AddEntry(self.b1_5, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB5))
                t1.DrawTextNDC(.4, .55, "S = "+str(S5))
                t1.DrawTextNDC(.4, .45, "B = "+str(B5))
                gPad.Update()
		c5.SaveAs("./plots/SRootB_2017_"+name+"_5.png")
		c5.Close()

		c10 = TCanvas()
		c10.cd()
                gPad.SetLogy()
		self.b1_10.SetTitle(name+" S/Root(B) 10% DDT")
		self.b1_10.Draw("hist")
		self.h1_10.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_10.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_10.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_10, name+" Signal")
                l1.AddEntry(self.b1_10, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB10))
                t1.DrawTextNDC(.4, .55, "S = "+str(S10))
                t1.DrawTextNDC(.4, .45, "B = "+str(B10))
                gPad.Update()
		c10.SaveAs("./plots/SRootB_2017_"+name+"_10.png")
		c10.Close()


		c15 = TCanvas()
		c15.cd()
                gPad.SetLogy()
		self.b1_15.SetTitle(name+" S/Root(B) 15% DDT")
		self.b1_15.Draw("hist")
		self.h1_15.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_15.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_15.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_15, name+" Signal")
                l1.AddEntry(self.b1_15, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB15))
                t1.DrawTextNDC(.4, .55, "S = "+str(S15))
                t1.DrawTextNDC(.4, .45, "B = "+str(B15))
                gPad.Update()
		c15.SaveAs("./plots/SRootB_2017_"+name+"_15.png")
		c15.Close()

		c20 = TCanvas()
		c20.cd()
                gPad.SetLogy()
		self.b1_20.SetTitle(name+" S/Root(B) 20% DDT")
		self.b1_20.Draw("hist")
		self.h1_20.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_20.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_20.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_20, name+" Signal")
                l1.AddEntry(self.b1_20, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB20))
                t1.DrawTextNDC(.4, .55, "S = "+str(S20))
                t1.DrawTextNDC(.4, .45, "B = "+str(B20))
                gPad.Update()
		c20.SaveAs("./plots/SRootB_2017_"+name+"_20.png")
		c20.Close()
		
		c25 = TCanvas()
		c25.cd()
                gPad.SetLogy()
		self.b1_25.SetTitle(name+" S/Root(B) 25% DDT")
		self.b1_25.Draw("hist")
		self.h1_25.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_25.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_25.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_25, name+" Signal")
                l1.AddEntry(self.b1_25, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB25))
                t1.DrawTextNDC(.4, .55, "S = "+str(S25))
                t1.DrawTextNDC(.4, .45, "B = "+str(B25))
                gPad.Update()
		c25.SaveAs("./plots/SRootB_2017_"+name+"_25.png")
		c25.Close()
		
		c30 = TCanvas()
		c30.cd()
                gPad.SetLogy()
		self.b1_30.SetTitle(name+" S/Root(B) 30% DDT")
		self.b1_30.Draw("hist")
		self.h1_30.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_30.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_30.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_30, name+" Signal")
                l1.AddEntry(self.b1_30, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB30))
                t1.DrawTextNDC(.4, .55, "S = "+str(S30))
                t1.DrawTextNDC(.4, .45, "B = "+str(B30))
                gPad.Update()
		c30.SaveAs("./plots/SRootB_2017_"+name+"_30.png")
		c30.Close()
		
		c50 = TCanvas()
		c50.cd()
                gPad.SetLogy()
		self.b1_50.SetTitle(name+" S/Root(B) 50% DDT")
		self.b1_50.Draw("hist")
		self.h1_50.Draw("same hist")
		lin1 = TLine(low, 1, low, self.h1_50.GetMaximum())
		lin2 = TLine(high, 1, high, self.h1_50.GetMaximum())
		lin1.SetLineColor(kViolet)
		lin2.SetLineColor(kViolet)
		lin1.SetLineWidth(2)
		lin2.SetLineWidth(2)
		lin1.Draw()
		lin2.Draw()
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h1_50, name+" Signal")
                l1.AddEntry(self.b1_50, "GJets")
                l1.Draw()
                t1 = TLatex()
                t1.DrawTextNDC(.4, .65, "S/Root(B) = "+str(SRB50))
                t1.DrawTextNDC(.4, .55, "S = "+str(S50))
                t1.DrawTextNDC(.4, .45, "B = "+str(B50))
                gPad.Update()
		c50.SaveAs("./plots/SRootB_2017_"+name+"_50.png")
		c50.Close()


		self.SRB = TGraph(7)
		self.SRB.SetPoint(1,5,SRB5)
		self.SRB.SetPoint(2,10,SRB10)
		self.SRB.SetPoint(3,15,SRB15)
		self.SRB.SetPoint(4,20,SRB20)
		self.SRB.SetPoint(5,25,SRB25)
		self.SRB.SetPoint(6,30,SRB30)
		self.SRB.SetPoint(7,50,SRB50)
		self.SRB.SetTitle("S/Root(B) For "+name+" Sample;DDT%;S/Root(B)")

		c_srb = TCanvas()
		c_srb.cd()
		self.SRB.Draw("AL*")
		ofile.WriteObject(self.SRB, "SRB_all_"+str(t))
		c_srb.SaveAs("./plots/SRB_2017_"+name+".png")
		c_srb.Close()
		
#		self.SRB_high = TGraph(7)
#		self.SRB_high.SetPoint(1,5,SRB5_high)
#		self.SRB_high.SetPoint(2,10,SRB10_high)
#		self.SRB_high.SetPoint(3,15,SRB15_high)
#		self.SRB_high.SetPoint(4,20,SRB20_high)
#		self.SRB_high.SetPoint(5,25,SRB25_high)
#		self.SRB_high.SetPoint(6,30,SRB30_high)
#		self.SRB_high.SetPoint(7,50,SRB50_high)
#		self.SRB_high.SetTitle("Jet pT > 200: S/Root(B) For "+name+" Sample;DDT%;S/Root(B)")

#		c_srb_high = TCanvas()
#		c_srb_high.cd()
#		self.SRB_high.Draw("AL*")
#		ofile.WriteObject(self.SRB_high, "SRB_high_"+str(t))
#		c_srb_high.SaveAs("./plots/SRB_high_2017_"+name+".png")
#		c_srb_high.Close()
		
		ofile.Write()
