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

def SigAdd(hist, sig, low, high):
	for i in range(low, high+1):
		hist.SetBinContent(i, sig.GetBinContent(i))

	return

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
        latex.DrawLatex(0.1265, 1-t+lumiTextOffset*t, cmsText)
        pad.Update()

class drawRData:
	def __init__(self, name, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, sfile8, sfile9, sfile10, sfile11, sfile12, o):
		gROOT.SetBatch(True)

		ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_draw/trigSF_check/"+o,"RECREATE")

		LUMI = 59.82
		cmsextra = "Preliminary"

		#Signal files
		self.f = TFile.Open(sfile1, "READ")
		self.f.ls();

		self.h10 = self.f.Get("thin_softdrop")
		
		self.p10 = self.f.Get("pass_soft_thin")
		
		self.f10 = self.f.Get("fail_soft_thin")
		
		self.g = TFile.Open(sfile2, "READ")
		self.g.ls();

		self.h10_trigSF = self.g.Get("thin_softdrop")
		
		self.p10_trigSF = self.g.Get("pass_soft_thin")
		
		self.f10_trigSF = self.g.Get("fail_soft_thin")

		self.h = TFile.Open(sfile3, "READ")
		self.h.ls();

		self.h25 = self.h.Get("thin_softdrop")
		
		self.p25 = self.h.Get("pass_soft_thin")
		
		self.f25 = self.h.Get("fail_soft_thin")
		
		self.i = TFile.Open(sfile4, "READ")
		self.i.ls();

		self.h25_trigSF = self.i.Get("thin_softdrop")
		
		self.p25_trigSF = self.i.Get("pass_soft_thin")
		
		self.f25_trigSF = self.i.Get("fail_soft_thin")
		
		self.j = TFile.Open(sfile5, "READ")
		self.j.ls();

		self.h50 = self.j.Get("thin_softdrop")
		
		self.p50 = self.j.Get("pass_soft_thin")
		
		self.f50 = self.j.Get("fail_soft_thin")
		
		self.k = TFile.Open(sfile6, "READ")
		self.k.ls();

		self.h50_trigSF = self.k.Get("thin_softdrop")
		
		self.p50_trigSF = self.k.Get("pass_soft_thin")
		
		self.f50_trigSF = self.k.Get("fail_soft_thin")
		
		self.l = TFile.Open(sfile7, "READ")
		self.l.ls();

		self.h75 = self.l.Get("thin_softdrop")
		
		self.p75 = self.l.Get("pass_soft_thin")
		
		self.f75 = self.l.Get("fail_soft_thin")
		
		self.m = TFile.Open(sfile8, "READ")
		self.m.ls();

		self.h75_trigSF = self.m.Get("thin_softdrop")
		
		self.p75_trigSF = self.m.Get("pass_soft_thin")
		
		self.f75_trigSF = self.m.Get("fail_soft_thin")

		self.n = TFile.Open(sfile9, "READ")
		self.n.ls();

		self.hWG = self.n.Get("thin_softdrop")
		
		self.pWG = self.n.Get("pass_soft_thin")
		
		self.fWG = self.n.Get("fail_soft_thin")

		self.o = TFile.Open(sfile10, "READ")
		self.o.ls();

		self.hWG_trigSF = self.o.Get("thin_softdrop")
		
		self.pWG_trigSF = self.o.Get("pass_soft_thin")
		
		self.fWG_trigSF = self.o.Get("fail_soft_thin")
	
		self.p = TFile.Open(sfile11, "READ")
		self.p.ls();

		self.hZG = self.p.Get("thin_softdrop")
		
		self.pZG = self.p.Get("pass_soft_thin")
		
		self.fZG = self.p.Get("fail_soft_thin")
		
		self.q = TFile.Open(sfile12, "READ")
		self.q.ls();

		self.hZG_trigSF = self.q.Get("thin_softdrop")
		
		self.pZG_trigSF = self.q.Get("pass_soft_thin")
		
		self.fZG_trigSF = self.q.Get("fail_soft_thin")


		self.h10_trigSF.SetLineColor(kRed)
		self.h25_trigSF.SetLineColor(kRed)
		self.h50_trigSF.SetLineColor(kRed)
		self.h75_trigSF.SetLineColor(kRed)
		self.hWG_trigSF.SetLineColor(kRed)
		self.hZG_trigSF.SetLineColor(kRed)
		
		self.p10_trigSF.SetLineColor(kRed)
		self.p25_trigSF.SetLineColor(kRed)
		self.p50_trigSF.SetLineColor(kRed)
		self.p75_trigSF.SetLineColor(kRed)
		self.pWG_trigSF.SetLineColor(kRed)
		self.pZG_trigSF.SetLineColor(kRed)
		
		self.f10_trigSF.SetLineColor(kRed)
		self.f25_trigSF.SetLineColor(kRed)
		self.f50_trigSF.SetLineColor(kRed)
		self.f75_trigSF.SetLineColor(kRed)
		self.fWG_trigSF.SetLineColor(kRed)
		self.fZG_trigSF.SetLineColor(kRed)
	
		FindAndSetMax(self.h10, self.h10_trigSF)
		FindAndSetMax(self.h25, self.h25_trigSF)
		FindAndSetMax(self.h50, self.h50_trigSF)
		FindAndSetMax(self.h75, self.h75_trigSF)
		FindAndSetMax(self.hWG, self.hWG_trigSF)
		FindAndSetMax(self.hZG, self.hZG_trigSF)
		
		FindAndSetMax(self.p10, self.p10_trigSF)
		FindAndSetMax(self.p25, self.p25_trigSF)
		FindAndSetMax(self.p50, self.p50_trigSF)
		FindAndSetMax(self.p75, self.p75_trigSF)
		FindAndSetMax(self.pWG, self.pWG_trigSF)
		FindAndSetMax(self.pZG, self.pZG_trigSF)

		FindAndSetMax(self.f10, self.f10_trigSF)
		FindAndSetMax(self.f25, self.f25_trigSF)
		FindAndSetMax(self.f50, self.f50_trigSF)
		FindAndSetMax(self.f75, self.f75_trigSF)
		FindAndSetMax(self.fWG, self.fWG_trigSF)
		FindAndSetMax(self.fZG, self.fZG_trigSF)

		ROOT.gStyle.SetOptStat(0)

		c10 = TCanvas()
		c10.cd()
#                gPad.SetLogy()
		self.h10.SetTitle(name+" 10 GeV")
		self.h10.Draw("hist")
		self.h10_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h10, "Corrections Applied")
                l1.AddEntry(self.h10_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c10.SaveAs("./plots/trigSF_comp_10GeV_2018.png")

		ofile.WriteObject(c10, "10GeV")
		c10.Close()
		

		c25 = TCanvas()
		c25.cd()
#                gPad.SetLogy()
		self.h25.SetTitle(name+" 25 GeV")
		self.h25.Draw("hist")
		self.h25_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h25, "Corrections Applied")
                l1.AddEntry(self.h25_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c25.SaveAs("./plots/trigSF_comp_25GeV_2018.png")

		ofile.WriteObject(c25, "25GeV")
		c25.Close()

		c50 = TCanvas()
		c50.cd()
#                gPad.SetLogy()
		self.h50.SetTitle(name+" 50 GeV")
		self.h50.Draw("hist")
		self.h50_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h50, "Corrections Applied")
                l1.AddEntry(self.h50_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c50.SaveAs("./plots/trigSF_comp_50GeV_2018.png")

		ofile.WriteObject(c50, "50GeV")
		c50.Close()

		c75 = TCanvas()
		c75.cd()
#                gPad.SetLogy()
		self.h75.SetTitle(name+" 75 GeV")
		self.h75.Draw("hist")
		self.h75_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.h75, "Corrections Applied")
                l1.AddEntry(self.h75_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c75.SaveAs("./plots/trigSF_comp_75GeV_2018.png")

		ofile.WriteObject(c75, "75GeV")
		c75.Close()
		
		cWG = TCanvas()
		cWG.cd()
#                gPad.SetLogy()
		self.hWG.SetTitle(name+" WGamma")
		self.hWG.Draw("hist")
		self.hWG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.hWG, "Corrections Applied")
                l1.AddEntry(self.hWG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cWG.SaveAs("./plots/trigSF_comp_WG_2018.png")

		ofile.WriteObject(cWG, "WG")
		cWG.Close()

		cZG = TCanvas()
		cZG.cd()
#                gPad.SetLogy()
		self.hZG.SetTitle(name+" ZGamma")
		self.hZG.Draw("hist")
		self.hZG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.hZG, "Corrections Applied")
                l1.AddEntry(self.hZG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cZG.SaveAs("./plots/trigSF_comp_ZG_2018.png")

		ofile.WriteObject(cZG, "ZG")
		cZG.Close()
		

		c10 = TCanvas()
		c10.cd()
#                gPad.SetLogy()
		self.p10.SetTitle("Passing "+name+" 10 GeV")
		self.p10.Draw("hist")
		self.p10_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.p10, "Corrections Applied")
                l1.AddEntry(self.p10_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c10.SaveAs("./plots/trigSF_comp_pass_10GeV_2018.png")

		ofile.WriteObject(c10, "10GeV_pass")
		c10.Close()
		
		c25 = TCanvas()
		c25.cd()
#                gPad.SetLogy()
		self.p25.SetTitle("Passing "+name+" 25 GeV")
		self.p25.Draw("hist")
		self.p25_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.p25, "Corrections Applied")
                l1.AddEntry(self.p25_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c25.SaveAs("./plots/trigSF_comp_pass_25GeV_2018.png")

		ofile.WriteObject(c25, "25GeV_pass")
		c25.Close()

		c50 = TCanvas()
		c50.cd()
#                gPad.SetLogy()
		self.p50.SetTitle("Passing "+name+" 50 GeV")
		self.p50.Draw("hist")
		self.p50_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.p50, "Corrections Applied")
                l1.AddEntry(self.p50_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c50.SaveAs("./plots/trigSF_comp_pass_50GeV_2018.png")

		ofile.WriteObject(c50, "50GeV_pass")
		c50.Close()

		c75 = TCanvas()
		c75.cd()
#                gPad.SetLogy()
		self.p75.SetTitle("Passing "+name+" 75 GeV")
		self.p75.Draw("hist")
		self.p75_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.p75, "Corrections Applied")
                l1.AddEntry(self.p75_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c75.SaveAs("./plots/trigSF_comp_pass_75GeV_2018.png")

		ofile.WriteObject(c75, "75GeV_pass")
		c75.Close()
		
		cWG = TCanvas()
		cWG.cd()
#                gPad.SetLogy()
		self.pWG.SetTitle("Passing "+name+" WGamma")
		self.pWG.Draw("hist")
		self.pWG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.pWG, "Corrections Applied")
                l1.AddEntry(self.pWG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cWG.SaveAs("./plots/trigSF_comp_pass_WG_2018.png")

		ofile.WriteObject(cWG, "WG_pass")
		cWG.Close()

		cZG = TCanvas()
		cZG.cd()
#                gPad.SetLogy()
		self.pZG.SetTitle("Passing "+name+" ZGamma")
		self.pZG.Draw("hist")
		self.pZG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.pZG, "Corrections Applied")
                l1.AddEntry(self.pZG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cZG.SaveAs("./plots/trigSF_comp_pass_ZG_2018.png")

		ofile.WriteObject(cZG, "ZG_pass")
		cZG.Close()
		
		c10 = TCanvas()
		c10.cd()
#                gPad.SetLogy()
		self.f10.SetTitle("Failing "+name+" 10 GeV")
		self.f10.Draw("hist")
		self.f10_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.f10, "Corrections Applied")
                l1.AddEntry(self.f10_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c10.SaveAs("./plots/trigSF_comp_fail_10GeV_2018.png")

		ofile.WriteObject(c10, "10GeV_fail")
		c10.Close()
		

		c25 = TCanvas()
		c25.cd()
#                gPad.SetLogy()
		self.f25.SetTitle("Failing "+name+" 25 GeV")
		self.f25.Draw("hist")
		self.f25_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.f25, "Corrections Applied")
                l1.AddEntry(self.f25_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c25.SaveAs("./plots/trigSF_comp_fail_25GeV_2018.png")

		ofile.WriteObject(c25, "25GeV_fail")
		c25.Close()

		c50 = TCanvas()
		c50.cd()
#                gPad.SetLogy()
		self.f50.SetTitle("Failing "+name+" 50 GeV")
		self.f50.Draw("hist")
		self.f50_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.f50, "Corrections Applied")
                l1.AddEntry(self.f50_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c50.SaveAs("./plots/trigSF_comp_fail_50GeV_2018.png")

		ofile.WriteObject(c50, "50GeV_fail")
		c50.Close()

		c75 = TCanvas()
		c75.cd()
#                gPad.SetLogy()
		self.f75.SetTitle("Failing "+name+" 75 GeV")
		self.f75.Draw("hist")
		self.f75_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.f75, "Corrections Applied")
                l1.AddEntry(self.f75_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		c75.SaveAs("./plots/trigSF_comp_fail_75GeV_2018.png")

		ofile.WriteObject(c75, "75GeV_fail")
		c75.Close()
		
		cWG = TCanvas()
		cWG.cd()
#                gPad.SetLogy()
		self.fWG.SetTitle("Failing "+name+" WGamma")
		self.fWG.Draw("hist")
		self.fWG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.fWG, "Corrections Applied")
                l1.AddEntry(self.fWG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cWG.SaveAs("./plots/trigSF_comp_fail_WG_2018.png")

		ofile.WriteObject(cWG, "WG_fail")
		cWG.Close()

		cZG = TCanvas()
		cZG.cd()
#                gPad.SetLogy()
		self.fZG.SetTitle("Failing "+name+" ZGamma")
		self.fZG.Draw("hist")
		self.fZG_trigSF.Draw("same hist")
                l1 = TLegend(.6, .75, .9, .9)
                l1.AddEntry(self.fZG, "Corrections Applied")
                l1.AddEntry(self.fZG_trigSF, "Trigger SF Applied")
                l1.Draw()
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
                gPad.Update()
		cZG.SaveAs("./plots/trigSF_comp_fail_ZG_2018.png")

		ofile.WriteObject(cZG, "ZG_fail")
		cZG.Close()
		
