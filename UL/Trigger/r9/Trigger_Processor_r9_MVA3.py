#
import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os
from array import array
import math
import numpy as np

#determines cutoff bin for value of rho or pt for N2DDT plotting
def bin_num(self, val, i):
	if i == 1:      #Rho Value
		#if val>-2 or val<-7:
		#       print("bin_num error, val: ", val)
		return int(((val+8.0)*2.0)+1.0)
	elif i == 2:     #Pt Value
		#if val>2000 or val<100:
		#       print("bin_num error, val: ", val)
		return int(((val)/50.0)+1.0)

def Proj(i, j, n2_bin, temp, t1):
	for x in range (n2_bin):
		temp.SetBinContent(x+1, t1.GetBinContent(i+1,j+1,x+1))


def Rho(msoft, pt):
	print(type(msoft))
	print(type(pt))
	return math.log(math.pow(msoft, 2)/math.pow(pt, 2))


def DDTpass(cut_hist, n2, pt, msoft):
	if n2 - cut_hist.GetBinContent(self.bin_num(Rho(msoft, pt) ,1), self.bin_num(pt,2)) < 0:
		return true
	else:
		return false

def DDT(cut_hist, n2, pt, msoft, rdf):

	ddt =  n2 - cut_hist.GetBinContent(bin_num(Rho(float(msoft), float(pt)) ,1), bin_num(float(pt),2))

	return rdf.Define("ddt", ddt)



def DataPro(sample, fname):

	gROOT.SetBatch(True)

	ofile = ROOT.TFile("RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()

		

#	h4_110 = TH1F("h4_110", "Photon pT", 25, widebins)
#	h4_200 = TH1F("h4_200", "Photon pT", 25, widebins)
#	h4_OR = TH1F("h4_OR", "Photon pT", 25, widebins)
#	h4_notrig = TH1F("h4_notrig", "Photon pT", 25, widebins)
#	h4_pt = TH1F("h4_pt", "Photon pT", 25, widebins)

	ROOT.gInterpreter.Declare("Double_t widebins[26] = {0, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")


	h1_110 = TH2F("h1_110", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1)
	h1_200 = TH2F("h1_200", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1)
	h1_OR = TH2F("h1_OR", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1)
	h1_notrig = TH2F("h1_notrig", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1)

	for F in sample:
		Chain = ROOT.TChain("Events")
		for path, subdirs, files in os.walk(F[0]):
			for name in files:
				File = os.path.join(path, name)
				if (File.endswith(".root")):
					print os.path.join(path, name) 
					#n = RDF(File).Count()
					#print n.GetValue()
					Chain.Add(File)
	
		Rdf_noCut = RDF(Chain)
                nocut = int(Rdf_noCut.Count())
		print(str(nocut)+" Events in Sample")

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
                precut = int(Rdf_PreSel.Count())
		print(str(precut)+" Events with nPhoton > 0 in Sample")
		Rdf_PreSel = Rdf_PreSel.Define("pPt", "Photon_pt[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pID", "Photon_mvaID[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pEta", "Photon_eta[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pIso", "Photon_pfRelIso03_all[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pCut", "Photon_cutBased[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pR9", "Photon_r9[0]")
		Rdf_PreSel = Rdf_PreSel.Define("weight", F[1])
		
#		Rdf_pt = Rdf_PreSel.Filter("pPt > 200")
 #               cut_pt = int(Rdf_pt.Count())
#		print(str(cut_pt)+" Events passing 200 pt cut in Sample")
		
		#Rdf_notrig = Rdf_PreSel.Filter("abs(pEta)<1.44 && pID[0] > 0 && pIso < .2 && pPt > 110 && pCut >= 4")
		Rdf_notrig = Rdf_PreSel.Filter("abs(pEta)<1.44 && pID > 0.9")
                cut_notrig = int(Rdf_notrig.Count())
		print(str(cut_notrig)+" Events passing non-trig cuts in Sample")

		#Rdf_110 = Rdf_PreSel.Filter("HLT_Photon110EB_TightID_TightIso > 0 && abs(pEta)<1.4 && pID > 0 && pIso > .2")
		Rdf_110 = Rdf_notrig.Filter("HLT_Photon110EB_TightID_TightIso > 0")
                cut_110 = int(Rdf_110.Count())
		print(str(cut_110)+" Events passing 110 trig in Sample")
		Rdf_200 = Rdf_notrig.Filter("HLT_Photon200 > 0")
                cut_200 = int(Rdf_200.Count())
		print(str(cut_200)+" Events passing 200 trig in Sample")
		
		Rdf_OR = Rdf_notrig.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
                cut_OR = int(Rdf_OR.Count())
		print(str(cut_OR)+" Events passing either trig in Sample")

		t1_110 = Rdf_110.Histo2D(("t1_110", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1), "pPt", "pR9", "weight")
		t1_110 = t1_110.Clone()
		t1_110.SetTitle("Photon pT vs. R9 Score")
		t1_110.SetXTitle("Photon pT")
		t1_110.SetYTitle("R9 Score")
		h1_110.Add(t1_110)
		
		t1_200 = Rdf_200.Histo2D(("t1_200", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1), "pPt", "pR9", "weight")
		t1_200 = t1_200.Clone()
		h1_200.Add(t1_200)

		t1_OR = Rdf_OR.Histo2D(("t1_OR", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1), "pPt", "pR9", "weight")
		t1_OR = t1_OR.Clone()
		h1_OR.Add(t1_OR)

		t1_notrig = Rdf_notrig.Histo2D(("t1_notrig", "Photon pT vs. R9 Score", 25, widebins, 100, 0, 1), "pPt", "pR9", "weight")
		t1_notrig = t1_notrig.Clone()
		h1_notrig.Add(t1_notrig)

#		t4_110 = Rdf_110.Histo1D(("t4_110", "Photon pT", 25, widebins), "pPt", "weight")
#		t4_110 = t4_110.Clone()
#		t4_110.SetTitle("Photon pT")
#		t4_110.SetXTitle("Photon pT")
#		h4_110.Add(t4_110)
		
#		t4_200 = Rdf_200.Histo1D(("t4_200", "Photon pT", 25, widebins), "pPt", "weight")
#		t4_200 = t4_200.Clone()
#		t4_200.SetTitle("Photon pT")
#		t4_200.SetXTitle("Photon pT")
#		h4_200.Add(t4_200)
		
#		t4_notrig = Rdf_notrig.Histo1D(("t4_notrig", "Photon pT", 25, widebins), "pPt", "weight")
#		t4_notrig = t4_notrig.Clone()
#		t4_notrig.SetTitle("Photon pT")
#		t4_notrig.SetXTitle("Photon pT")
#		h4_notrig.Add(t4_notrig)
		
#		t4_OR = Rdf_OR.Histo1D(("t4_OR", "Photon pT", 25, widebins), "pPt", "weight")
#		t4_OR = t4_OR.Clone()
#		t4_OR.SetTitle("Photon pT")
#		t4_OR.SetXTitle("Photon pT")
#		h4_OR.Add(t4_OR)

		
#		t4_pt = Rdf_pt.Histo1D(("t4_pt", "Photon pT", 25, widebins), "pPt", "weight")
#		t4_pt = t4_pt.Clone()
#		t4_pt.SetTitle("Photon pT")
#		t4_pt.SetXTitle("Photon pT")
#		h4_pt.Add(t4_pt)
		
	
	h1_110.SetXTitle("Photon pT")
	h1_110.SetYTitle("R9 Score")
	h1_200.SetXTitle("Photon pT")
	h1_200.SetYTitle("R9 Score")
	h1_notrig.SetXTitle("Photon pT")
	h1_notrig.SetYTitle("R9 Score")
	h1_OR.SetXTitle("Photon pT")
	h1_OR.SetYTitle("R9 Score")

	ofile.WriteObject(h1_110, "photon_pt_mva_110")
	ofile.WriteObject(h1_200, "photon_pt_mva_200")
	ofile.WriteObject(h1_notrig, "photon_pt_mva_notrig")
	ofile.WriteObject(h1_OR, "photon_pt_mva_OR")
	
#	ofile.WriteObject(h4_110, "photon_pt_110")
#	ofile.WriteObject(h4_200, "photon_pt_200")
#	ofile.WriteObject(h4_notrig, "photon_pt_notrig")
#	ofile.WriteObject(h4_OR, "photon_pt_OR")
#	ofile.WriteObject(h4_notrig, "photon_pt_pt")
	
#	h4.SetTitle("Photon pT")
#	h4.SetXTitle("pT")

#	n4 = TCanvas()
#	n4.cd()
#	h4.Draw("hist")
#	n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pho_pt.png")
#	n4.Close()
	
	
	
	ofile.Write()
