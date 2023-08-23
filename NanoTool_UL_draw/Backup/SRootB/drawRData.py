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
		
		B5 = self.b1_5.Integral(sig_low, sig_high)
		B10 = self.b1_10.Integral(sig_low, sig_high)
		B15 = self.b1_15.Integral(sig_low, sig_high)
		B20 = self.b1_20.Integral(sig_low, sig_high)
		B25 = self.b1_25.Integral(sig_low, sig_high)
		B30 = self.b1_30.Integral(sig_low, sig_high)
		B50 = self.b1_50.Integral(sig_low, sig_high)

		SRB5 = S5/sqrt(B5)
		SRB10 = S10/sqrt(B10)
		SRB15 = S15/sqrt(B15)
		SRB20 = S20/sqrt(B20)
		SRB25 = S25/sqrt(B25)
		SRB30 = S30/sqrt(B30)
		SRB50 = S50/sqrt(B50)


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
		c5.SaveAs("./plots/SRootB_"+name+"_5.png")
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
		c10.SaveAs("./plots/SRootB_"+name+"_10.png")
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
		c15.SaveAs("./plots/SRootB_"+name+"_15.png")
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
		c20.SaveAs("./plots/SRootB_"+name+"_20.png")
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
		c25.SaveAs("./plots/SRootB_"+name+"_25.png")
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
		c30.SaveAs("./plots/SRootB_"+name+"_30.png")
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
		c50.SaveAs("./plots/SRootB_"+name+"_50.png")
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

		c_srb.SaveAs("./plots/SRB_"+name+".png")
		c_srb.Close()
		
