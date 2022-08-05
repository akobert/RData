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
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, ifile5, ifile6, bfile1):
		gROOT.SetBatch(True)

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.soft10 = self.f.Get("pass_soft")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();

		self.soft25 = self.g.Get("pass_soft")
		
		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();

		self.soft150 = self.h.Get("pass_soft")

		self.k = TFile.Open(ifile4, "READ")
		self.k.ls();

		self.soft50 = self.k.Get("pass_soft")
		
		self.m = TFile.Open(ifile5, "READ")
		self.m.ls();

		self.soft75 = self.m.Get("pass_soft")
		
		self.n = TFile.Open(ifile6, "READ")
		self.n.ls();

		self.soft100 = self.n.Get("pass_soft")

		self.j = TFile.Open(bfile1, "READ")
		self.j.ls();

		self.GJsoft = self.j.Get("pass_soft")

		
		self.GJsoft.SetLineColor(kRed)

		S10 = self.soft10.Integral(2,3)
		S25 = self.soft25.Integral(5,7)
		S50 = self.soft50.Integral(10,12)
		S75 = self.soft75.Integral(15,17)
		S100 = self.soft100.Integral(20,22)
		S150 = self.soft150.Integral(29,35)

		B10 = self.GJsoft.Integral(2,3)
		B25 = self.GJsoft.Integral(5,7)
		B50 = self.GJsoft.Integral(10,12)
		B75 = self.GJsoft.Integral(15,17)
		B100 = self.GJsoft.Integral(20,22)
		B150 = self.GJsoft.Integral(29,35)

		RB10 = sqrt(self.GJsoft.Integral(2,3))
		RB25 = sqrt(self.GJsoft.Integral(5,7))
		RB50 = sqrt(self.GJsoft.Integral(10,12))
		RB75 = sqrt(self.GJsoft.Integral(15,17))
		RB100 = sqrt(self.GJsoft.Integral(20,22))
		RB150 = sqrt(self.GJsoft.Integral(29,35))

		SRB10 = S10/RB10
		SRB25 = S25/RB25
		SRB50 = S50/RB50
		SRB75 = S75/RB75
		SRB100 = S100/RB100
		SRB150 = S150/RB150

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.GJsoft.SetTitle("10 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft10.Draw("same hist")
		l1 = TLegend(.6, .75, .9, .9)
		l1.AddEntry(self.GJsoft, "Passing GJets")
                l1.AddEntry(self.soft10, "Passing 10 GeV Signal")
                l1.Draw()
		gPad.SetLogy()
		t1 = TLatex()
		t1.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB10))
                t1.DrawTextNDC(.4, .55, "S = "+str(S10))
                t1.DrawTextNDC(.4, .45, "B = "+str(B10))
		#TLine li1 = TLine(5,0,5,1)
                gPad.Update()
		li1 = TLine(5,-10,5,380000)
		li1.SetLineColor(kBlack)
		li1.Draw()
		li2 = TLine(15,-10,15,380000)
		li2.SetLineColor(kBlack)
		li2.Draw()
		c1.SaveAs(name+"_10GeV_SRB.png")
		c1.Close()

		c2 = TCanvas()
		c2.cd()
		self.GJsoft.SetTitle("25 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft25.Draw("same hist")
		l2 = TLegend(.6, .75, .9, .9)
		l2.AddEntry(self.GJsoft, "Passing GJets")
                l2.AddEntry(self.soft25, "Passing 25 GeV Signal")
                l2.Draw()
		gPad.SetLogy()
		t2 = TLatex()
		t2.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB25))
                t2.DrawTextNDC(.4, .55, "S = "+str(S25))
                t2.DrawTextNDC(.4, .45, "B = "+str(B25))
		li3 = TLine(20,-10,20,380000)
		li3.SetLineColor(kBlack)
		li3.Draw()
		li4 = TLine(35,-10,35,380000)
		li4.SetLineColor(kBlack)
		li4.Draw()
                gPad.Update()
		c2.SaveAs(name+"_25GeV_SRB.png")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.GJsoft.SetTitle("150 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft150.Draw("same hist")
		l3 = TLegend(.6, .75, .9, .9)
		l3.AddEntry(self.GJsoft, "Passing GJets")
                l3.AddEntry(self.soft150, "Passing 150 GeV Signal")
                l3.Draw()
		gPad.SetLogy()
		t3 = TLatex()
		t3.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB150))
                t3.DrawTextNDC(.4, .55, "S = "+str(S150))
                t3.DrawTextNDC(.4, .45, "B = "+str(B150))
		li5 = TLine(140,-10,140,65000)
		li5.SetLineColor(kBlack)
		li5.Draw()
		li6 = TLine(175,-10,175,65000)
		li6.SetLineColor(kBlack)
		li6.Draw()
                gPad.Update()
		c3.SaveAs(name+"_150GeV_SRB.png")
		c3.Close()

		c4 = TCanvas()
		c4.cd()
		self.GJsoft.SetTitle("50 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft50.Draw("same hist")
		l4 = TLegend(.6, .75, .9, .9)
		l4.AddEntry(self.GJsoft, "Passing GJets")
                l4.AddEntry(self.soft50, "Passing 50 GeV Signal")
                l4.Draw()
		gPad.SetLogy()
		t4 = TLatex()
		t4.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB50))
                t4.DrawTextNDC(.4, .55, "S = "+str(S50))
                t4.DrawTextNDC(.4, .45, "B = "+str(B50))
		li7 = TLine(45,-10,45,380000)
		li7.SetLineColor(kBlack)
		li7.Draw()
		li8 = TLine(60,-10,60,380000)
		li8.SetLineColor(kBlack)
		li8.Draw()
                gPad.Update()
		c4.SaveAs(name+"_50GeV_SRB.png")
		c4.Close()

		c5 = TCanvas()
		c5.cd()
		self.GJsoft.SetTitle("75 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft75.Draw("same hist")
		l5 = TLegend(.6, .75, .9, .9)
		l5.AddEntry(self.GJsoft, "Passing GJets")
                l5.AddEntry(self.soft75, "Passing 75 GeV Signal")
                l5.Draw()
		gPad.SetLogy()
		t5 = TLatex()
		t5.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB75))
                t5.DrawTextNDC(.4, .55, "S = "+str(S75))
                t5.DrawTextNDC(.4, .45, "B = "+str(B75))
		li7 = TLine(70,-10,70,380000)
		li7.SetLineColor(kBlack)
		li7.Draw()
		li8 = TLine(85,-10,85,380000)
		li8.SetLineColor(kBlack)
		li8.Draw()
                gPad.Update()
		c5.SaveAs(name+"_75GeV_SRB.png")
		c5.Close()

		c6 = TCanvas()
		c6.cd()
		self.GJsoft.SetTitle("100 GeV S/Root(B)")
		self.GJsoft.SetXTitle("Softdrop Mass")
		self.GJsoft.Draw("hist")
		self.soft100.Draw("same hist")
		l6 = TLegend(.6, .75, .9, .9)
		l6.AddEntry(self.GJsoft, "Passing GJets")
                l6.AddEntry(self.soft100, "Passing 100 GeV Signal")
                l6.Draw()
		gPad.SetLogy()
		t6 = TLatex()
		t6.DrawTextNDC(.4, .65, "S/sqrt(B) = "+str(SRB100))
                t6.DrawTextNDC(.4, .55, "S = "+str(S100))
                t6.DrawTextNDC(.4, .45, "B = "+str(B100))
		li7 = TLine(95,-10,95,380000)
		li7.SetLineColor(kBlack)
		li7.Draw()
		li8 = TLine(110,-10,110,380000)
		li8.SetLineColor(kBlack)
		li8.Draw()
                gPad.Update()
		c6.SaveAs(name+"_100GeV_SRB.png")
		c6.Close()
		
