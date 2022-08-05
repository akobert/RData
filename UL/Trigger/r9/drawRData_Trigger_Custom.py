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
	def __init__(self, name, ifile1, ifile2, ifile3, ifile4, tag):
		gROOT.SetBatch(True)

		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();
		
		self.notrig_cut = self.f.Get("photon_pt_mva_notrig")
		self.r110_cut = self.f.Get("photon_pt_mva_110")
		self.r200_cut = self.f.Get("photon_pt_mva_200")
		self.rOR_cut = self.f.Get("photon_pt_mva_OR")
		
		self.g = TFile.Open(ifile2, "READ")
		self.g.ls();
		
		self.notrig_mva1 = self.g.Get("photon_pt_mva_notrig")
		self.r110_mva1 = self.g.Get("photon_pt_mva_110")
		self.r200_mva1 = self.g.Get("photon_pt_mva_200")
		self.rOR_mva1 = self.g.Get("photon_pt_mva_OR")

		self.h = TFile.Open(ifile3, "READ")
		self.h.ls();
		
		self.notrig_mva2 = self.h.Get("photon_pt_mva_notrig")
		self.r110_mva2 = self.h.Get("photon_pt_mva_110")
		self.r200_mva2 = self.h.Get("photon_pt_mva_200")
		self.rOR_mva2 = self.h.Get("photon_pt_mva_OR")
		
#		self.j = TFile.Open(ifile4, "READ")
#		self.j.ls();
		
#		self.notrig_mva3 = self.j.Get("photon_pt_mva_notrig")
#		self.r110_mva3 = self.j.Get("photon_pt_mva_110")
#		self.r200_mva3 = self.j.Get("photon_pt_mva_200")
#		self.rOR_mva3 = self.j.Get("photon_pt_mva_OR")


		self.r110_cut.Divide(self.notrig_cut)
		self.r200_cut.Divide(self.notrig_cut)
		self.rOR_cut.Divide(self.notrig_cut)
	
		self.r110_cut.SetAxisRange(0,1.0, "Z")	
		self.r200_cut.SetAxisRange(0,1.0, "Z")	
		self.rOR_cut.SetAxisRange(0,1.0, "Z")	
		
		self.r110_cut.SetTitle("Photon110 Photon pT vs. r9 "+tag)
		self.r200_cut.SetTitle("Photon200 Photon pT vs. r9 "+tag)
		self.rOR_cut.SetTitle("OR Photon pT vs. r9 "+tag)

		self.r110_mva1.Divide(self.notrig_mva1)
		self.r200_mva1.Divide(self.notrig_mva1)
		self.rOR_mva1.Divide(self.notrig_mva1)
	
		self.r110_mva1.SetAxisRange(0,1.0, "Z")	
		self.r200_mva1.SetAxisRange(0,1.0, "Z")	
		self.rOR_mva1.SetAxisRange(0,1.0, "Z")	
		
		self.r110_mva1.SetTitle("Photon110 Photon pT vs. r9 "+tag)
		self.r200_mva1.SetTitle("Photon200 Photon pT vs. r9 "+tag)
		self.rOR_mva1.SetTitle("OR Photon pT vs. r9 "+tag)
		
		self.r110_mva2.Divide(self.notrig_mva2)
		self.r200_mva2.Divide(self.notrig_mva2)
		self.rOR_mva2.Divide(self.notrig_mva2)
	
		self.r110_mva2.SetAxisRange(0,1.0, "Z")	
		self.r200_mva2.SetAxisRange(0,1.0, "Z")	
		self.rOR_mva2.SetAxisRange(0,1.0, "Z")	
		
		self.r110_mva2.SetTitle("Photon110 Photon pT vs. r9 "+tag)
		self.r200_mva2.SetTitle("Photon200 Photon pT vs. r9 "+tag)
		self.rOR_mva2.SetTitle("OR Photon pT vs. r9 "+tag)
		
#		self.r110_mva3.Divide(self.notrig_mva3)
#		self.r200_mva3.Divide(self.notrig_mva3)
#		self.rOR_mva3.Divide(self.notrig_mva3)
	
#		self.r110_mva3.SetAxisRange(0,1.0, "Z")	
#		self.r200_mva3.SetAxisRange(0,1.0, "Z")	
#		self.rOR_mva3.SetAxisRange(0,1.0, "Z")	
		
#		self.r110_mva3.SetTitle("Photon110 Photon pT vs. r9 "+tag)
#		self.r200_mva3.SetTitle("Photon200 Photon pT vs. r9 "+tag)
#		self.rOR_mva3.SetTitle("OR Photon pT vs. r9 "+tag)

		ROOT.gStyle.SetOptStat(0)

		c1 = TCanvas()
		c1.cd()
		self.r110_cut.Draw("COLZ")
		c1.SaveAs("./"+name+"_110_cut.png")
		c1.SaveAs("./"+name+"_110_cut.root")
		c1.Close()
		
		c2 = TCanvas()
		c2.cd()
		self.r200_cut.Draw("COLZ")
		c2.SaveAs("./"+name+"_200_cut.png")
		c2.SaveAs("./"+name+"_200_cut.root")
		c2.Close()
		
		c3 = TCanvas()
		c3.cd()
		self.rOR_cut.Draw("COLZ")
		c3.SaveAs("./"+name+"_OR_cut.png")
		c3.SaveAs("./"+name+"_OR_cut.root")
		c3.Close()
		
		c4 = TCanvas()
		c4.cd()
		self.r110_mva1.Draw("COLZ")
		c4.SaveAs("./"+name+"_110_mva1.png")
		c4.SaveAs("./"+name+"_110_mva1.root")
		c4.Close()
		
		c5 = TCanvas()
		c5.cd()
		self.r200_mva1.Draw("COLZ")
		c5.SaveAs("./"+name+"_200_mva1.png")
		c5.SaveAs("./"+name+"_200_mva1.root")
		c5.Close()
		
		c6 = TCanvas()
		c6.cd()
		self.rOR_mva1.Draw("COLZ")
		c6.SaveAs("./"+name+"_OR_mva1.png")
		c6.SaveAs("./"+name+"_OR_mva1.root")
		c6.Close()
		
		c7 = TCanvas()
		c7.cd()
		self.r110_mva2.Draw("COLZ")
		c7.SaveAs("./"+name+"_110_mva2.png")
		c7.SaveAs("./"+name+"_110_mva2.root")
		c7.Close()
		
		c8 = TCanvas()
		c8.cd()
		self.r200_mva2.Draw("COLZ")
		c8.SaveAs("./"+name+"_200_mva2.png")
		c8.SaveAs("./"+name+"_200_mva2.root")
		c8.Close()
		
		c9 = TCanvas()
		c9.cd()
		self.rOR_mva2.Draw("COLZ")
		c9.SaveAs("./"+name+"_OR_mva2.png")
		c9.SaveAs("./"+name+"_OR_mva2.root")
		c9.Close()
		
#		c10 = TCanvas()
#		c10.cd()
#		self.r110_mva3.Draw("COLZ")
#		c10.SaveAs("./"+name+"_110_mva3.png")
#		c10.SaveAs("./"+name+"_110_mva3.root")
#		c10.Close()
		
#		c11 = TCanvas()
#		c11.cd()
#		self.r200_mva3.Draw("COLZ")
#		c11.SaveAs("./"+name+"_200_mva3.png")
#		c11.SaveAs("./"+name+"_200_mva3.root")
#		c11.Close()
		
#		c12 = TCanvas()
#		c12.cd()
#		self.rOR_mva3.Draw("COLZ")
#		c12.SaveAs("./"+name+"_OR_mva3.png")
#		c12.SaveAs("./"+name+"_OR_mva3.root")
#		c12.Close()

