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

	ROOT.gInterpreter.Declare("Double_t widebins[35] = {0, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")

#	h4_pt = TH1F("h4_pt", "Photon pT", 34, widebins)
		
	h4_110 = TH1F("h4_110", "Photon pT (cutBased)", 34, widebins)
	h4_200 = TH1F("h4_200", "Photon pT (cutBased)", 34, widebins)
	h4_OR = TH1F("h4_OR", "Photon pT (cutBased)", 34, widebins)
	h4_notrig = TH1F("h4_notrig", "Photon pT (cutBased)", 34, widebins)
        h4_OR_thin = TH1F("h4_OR_thin", "Photon pT (cutBased)", 500, 0, 500)
        h4_notrig_thin = TH1F("h4_notrig_thin", "Photon pT (cutBased)", 500, 0, 500)
	
	h4_110_mva80 = TH1F("h4_110_mva80", "Photon pT (WP80)", 34, widebins)
	h4_200_mva80 = TH1F("h4_200_mva80", "Photon pT (WP80)", 34, widebins)
	h4_OR_mva80 = TH1F("h4_OR_mva80", "Photon pT (WP80)", 34, widebins)
	h4_notrig_mva80 = TH1F("h4_notrig_mva80", "Photon pT (WP80)", 34, widebins)
        h4_OR_thin_mva80 = TH1F("h4_OR_thin_mva80", "Photon pT (WP80)", 500, 0, 500)
        h4_notrig_thin_mva80 = TH1F("h4_notrig_thin_mva80", "Photon pT (WP80)", 500, 0, 500)
	
	h4_110_mva90 = TH1F("h4_110_mva90", "Photon pT (WP90)", 34, widebins)
	h4_200_mva90 = TH1F("h4_200_mva90", "Photon pT (WP90)", 34, widebins)
	h4_OR_mva90 = TH1F("h4_OR_mva90", "Photon pT (WP90)", 34, widebins)
	h4_notrig_mva90 = TH1F("h4_notrig_mva90", "Photon pT (WP90)", 34, widebins)
        h4_OR_thin_mva90 = TH1F("h4_OR_thin_mva90", "Photon pT (WP90)", 500, 0, 500)
        h4_notrig_thin_mva90 = TH1F("h4_notrig_thin_mva90", "Photon pT (WP90)", 500, 0, 500)
	
	h4_110_mva8 = TH1F("h4_110_mva8", "Photon pT (MVA >= 0.8)", 34, widebins)
	h4_200_mva8 = TH1F("h4_200_mva8", "Photon pT (MVA >= 0.8)", 34, widebins)
	h4_OR_mva8 = TH1F("h4_OR_mva8", "Photon pT (MVA >= 0.8)", 34, widebins)
	h4_notrig_mva8 = TH1F("h4_notrig_mva8", "Photon pT (MVA >= 0.8)", 34, widebins)
        h4_OR_thin_mva8 = TH1F("h4_OR_thin_mva8", "Photon pT (MVA >= 0.8)", 500, 0, 500)
        h4_notrig_thin_mva8 = TH1F("h4_notrig_thin_mva8", "Photon pT (MVA >= 0.8)", 500, 0, 500)
	
	h4_110_mva85 = TH1F("h4_110_mva85", "Photon pT (MVA >= 0.85)", 34, widebins)
	h4_200_mva85 = TH1F("h4_200_mva85", "Photon pT (MVA >= 0.85)", 34, widebins)
	h4_OR_mva85 = TH1F("h4_OR_mva85", "Photon pT (MVA >= 0.85)", 34, widebins)
	h4_notrig_mva85 = TH1F("h4_notrig_mva85", "Photon pT (MVA >= 0.85)", 34, widebins)
        h4_OR_thin_mva85 = TH1F("h4_OR_thin_mva85", "Photon pT (MVA >= 0.85)", 500, 0, 500)
        h4_notrig_thin_mva85 = TH1F("h4_notrig_thin_mva85", "Photon pT (MVA >= 0.85)", 500, 0, 500)
	
	h4_110_mva9 = TH1F("h4_110_mva9", "Photon pT (MVA >= 0.9)", 34, widebins)
	h4_200_mva9 = TH1F("h4_200_mva9", "Photon pT (MVA >= 0.9)", 34, widebins)
	h4_OR_mva9 = TH1F("h4_OR_mva9", "Photon pT (MVA >= 0.9)", 34, widebins)
	h4_notrig_mva9 = TH1F("h4_notrig_mva9", "Photon pT (MVA >= 0.9)", 34, widebins)
        h4_OR_thin_mva9 = TH1F("h4_OR_thin_mva9", "Photon pT (MVA >= 0.9)", 500, 0, 500)
        h4_notrig_thin_mva9 = TH1F("h4_notrig_thin_mva9", "Photon pT (MVA >= 0.9)", 500, 0, 500)

	h5_notrig = TH2F("h5_notrig_pt_eta", "Jet Eta vs. Jet pT No Trigger (CutBased ID)", 30, -1.5, 1.5, 20, 150, 250)
	h5_110 = TH2F("h5_110_pt_eta", "Jet Eta vs. Jet pT Photon110 (CutBased ID)", 30, -1.5, 1.5, 20, 150, 250)
	h5_200 = TH2F("h5_200_pt_eta", "Jet Eta vs. Jet pT Photon200 (CutBased ID)", 30, -1.5, 1.5, 20, 150, 250)
	h5_OR = TH2F("h5_110_pt_eta", "Jet Eta vs. Jet pT OR Triggers (CutBased ID)", 30, -1.5, 1.5, 20, 150, 250)

	h5_notrig.SetXTitle("Photon Eta")
	h5_notrig.SetYTitle("Photon pT")
	h5_110.SetXTitle("Photon Eta")
	h5_110.SetYTitle("Photon pT")
	h5_200.SetXTitle("Photon Eta")
	h5_200.SetYTitle("Photon pT")
	h5_OR.SetXTitle("Photon Eta")
	h5_OR.SetYTitle("Photon pT")
	

	for F in sample:
		Chain = ROOT.TChain("Events")
		for path, subdirs, files in os.walk(F[0]):
			for name in files:
				File = os.path.join(path, name)
				if (File.endswith(".root")):
					print os.path.join(path, name) 
					#n = RDF(File).Count()
					#print n.GetValue()
					f = TFile.Open(File, "READ")
					tree = f.Get("Events")
					tx = 0
					for branch in tree.GetListOfBranches():
						if(branch.GetName() == "HLT_Photon110EB_TightID_TightIso"):
							tx = 1
							break
					if tx == 0:
						print("Branch Missing: "+os.path.join(path,name))
					Chain.Add(File)
	
		Rdf_noCut = RDF(Chain)
                nocut = int(Rdf_noCut.Count())
		print(str(nocut)+" Events in Sample")

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
                precut = int(Rdf_PreSel.Count())
		print(str(precut)+" Events with nPhoton > 0 in Sample")
		Rdf_PreSel = Rdf_PreSel.Define("pPt", "Photon_pt[0]")
		Rdf_PreSel = Rdf_PreSel.Define("mva", "Photon_mvaID[0]")
#		Rdf_PreSel = Rdf_PreSel.Define("pID_80", "Photon_mvaID_WP80[0]")
#		Rdf_PreSel = Rdf_PreSel.Define("pID_90", "Photon_mvaID_WP90[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pEta", "Photon_eta[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pIso", "Photon_pfRelIso03_all[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pCut", "Photon_cutBased[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pR9", "Photon_r9[0]")

		if F[3] == "mc" or F[3] == "GJ" or F[3] == "QCD":
	                Rdf_PreSel = Rdf_PreSel.Define("xs_lumi", F[1])
	                Rdf_PreSel = Rdf_PreSel.Define("weight", "xs_lumi*puWeight")
	        elif F[3] == "data":
	                Rdf_PreSel = Rdf_PreSel.Define("weight", F[1])

		
		
		Rdf_notrig = Rdf_PreSel.Filter("abs(pEta)<1.44 && pCut >= 3 && HLT_Mu50 > 0")
                cut_notrig = int(Rdf_notrig.Count())
		print(str(cut_notrig)+" Events passing non-trig cuts (cutBased) in Sample")
		
		Rdf_notrig_mva80 = Rdf_PreSel.Filter("abs(pEta)<1.44 && Photon_mvaID_WP80[0] == 1 && HLT_Mu50 > 0")
                cut_notrig_mva80 = int(Rdf_notrig_mva80.Count())
		print(str(cut_notrig_mva80)+" Events passing non-trig cuts (WP80) in Sample")
		
		Rdf_notrig_mva90 = Rdf_PreSel.Filter("abs(pEta)<1.44 && Photon_mvaID_WP90[0] == 1 && HLT_Mu50 > 0")
                cut_notrig_mva90 = int(Rdf_notrig_mva90.Count())
		print(str(cut_notrig_mva90)+" Events passing non-trig cuts (WP90) in Sample")
		
		Rdf_notrig_mva8 = Rdf_PreSel.Filter("abs(pEta)<1.44 && mva >= 0.8 && HLT_Mu50 > 0")
                cut_notrig_mva8 = int(Rdf_notrig_mva8.Count())
		print(str(cut_notrig_mva8)+" Events passing non-trig cuts (MVA >= 0.8) in Sample")
		
		Rdf_notrig_mva85 = Rdf_PreSel.Filter("abs(pEta)<1.44 && mva >= 0.85 && HLT_Mu50 > 0")
                cut_notrig_mva85 = int(Rdf_notrig_mva85.Count())
		print(str(cut_notrig_mva85)+" Events passing non-trig cuts (MVA >= 0.85) in Sample")
		
		Rdf_notrig_mva9 = Rdf_PreSel.Filter("abs(pEta)<1.44 && mva >= 0.9 && HLT_Mu50 > 0")
                cut_notrig_mva9 = int(Rdf_notrig_mva9.Count())
		print(str(cut_notrig_mva9)+" Events passing non-trig cuts (MVA >= 0.9) in Sample")
		
		if F[2] == 1:
			Rdf_110 = Rdf_notrig.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110 = int(Rdf_110.Count())
			print(str(cut_110)+" Events passing 110 trig (cutBased) in Sample")
			
			Rdf_110_mva80 = Rdf_notrig_mva80.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110_mva80 = int(Rdf_110_mva80.Count())
			print(str(cut_110_mva80)+" Events passing 110 trig (WP80) in Sample")
			
			Rdf_110_mva90 = Rdf_notrig_mva90.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110_mva90 = int(Rdf_110_mva90.Count())
			print(str(cut_110_mva90)+" Events passing 110 trig (WP90) in Sample")
			
			Rdf_110_mva8 = Rdf_notrig_mva8.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110_mva8 = int(Rdf_110_mva8.Count())
			print(str(cut_110_mva8)+" Events passing 110 trig (MVA >= 0.8) in Sample")
			
			Rdf_110_mva85 = Rdf_notrig_mva85.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110_mva85 = int(Rdf_110_mva85.Count())
			print(str(cut_110_mva85)+" Events passing 110 trig (MVA >= 0.85) in Sample")
			
			Rdf_110_mva9 = Rdf_notrig_mva9.Filter("HLT_Photon110EB_TightID_TightIso > 0")
	                cut_110_mva9 = int(Rdf_110_mva9.Count())
			print(str(cut_110_mva9)+" Events passing 110 trig (MVA >= 0.9) in Sample")

		Rdf_200 = Rdf_notrig.Filter("HLT_Photon200 > 0")
                cut_200 = int(Rdf_200.Count())
		print(str(cut_200)+" Events passing 200 trig (cutBased) in Sample")
		
		Rdf_200_mva80 = Rdf_notrig_mva80.Filter("HLT_Photon200 > 0")
                cut_200_mva80 = int(Rdf_200_mva80.Count())
		print(str(cut_200)+" Events passing 200 trig (WP80) in Sample")
		
		Rdf_200_mva90 = Rdf_notrig_mva90.Filter("HLT_Photon200 > 0")
                cut_200_mva90 = int(Rdf_200_mva90.Count())
		print(str(cut_200)+" Events passing 200 trig (WP90) in Sample")
		
		Rdf_200_mva8 = Rdf_notrig_mva8.Filter("HLT_Photon200 > 0")
                cut_200_mva8 = int(Rdf_200_mva8.Count())
		print(str(cut_200)+" Events passing 200 trig (MVA >= 0.8) in Sample")
		
		Rdf_200_mva85 = Rdf_notrig_mva85.Filter("HLT_Photon200 > 0")
                cut_200_mva85 = int(Rdf_200_mva85.Count())
		print(str(cut_200)+" Events passing 200 trig (MVA >= 0.85) in Sample")
		
		Rdf_200_mva9 = Rdf_notrig_mva9.Filter("HLT_Photon200 > 0")
                cut_200_mva9 = int(Rdf_200_mva9.Count())
		print(str(cut_200)+" Events passing 200 trig (MVA >= 0.9) in Sample")
		
		if F[2] == 1:
			Rdf_OR = Rdf_notrig.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
			Rdf_OR_mva80 = Rdf_notrig_mva80.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
			Rdf_OR_mva90 = Rdf_notrig_mva90.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
			Rdf_OR_mva8 = Rdf_notrig_mva8.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
			Rdf_OR_mva85 = Rdf_notrig_mva85.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
			Rdf_OR_mva9 = Rdf_notrig_mva9.Filter("HLT_Photon200 > 0 || HLT_Photon110EB_TightID_TightIso > 0")
		
		#Currently avoiding branch_missing
#		if F[2] == 2:
#			Rdf_OR = Rdf_notrig.Filter("HLT_Photon200 > 0")
#			Rdf_OR_mva80 = Rdf_notrig_mva80.Filter("HLT_Photon200 > 0")
#			Rdf_OR_mva90 = Rdf_notrig_mva90.Filter("HLT_Photon200 > 0")
#			Rdf_OR_mva8 = Rdf_notrig_mva8.Filter("HLT_Photon200 > 0")
#			Rdf_OR_mva85 = Rdf_notrig_mva85.Filter("HLT_Photon200 > 0")
#			Rdf_OR_mva9 = Rdf_notrig_mva9.Filter("HLT_Photon200 > 0")
                cut_OR = int(Rdf_OR.Count())
		print(str(cut_OR)+" Events passing either trig (cutBased) in Sample")
                cut_OR_mva80 = int(Rdf_OR_mva80.Count())
		print(str(cut_OR_mva80)+" Events passing either trig (WP80) in Sample")
                cut_OR_mva90 = int(Rdf_OR_mva90.Count())
		print(str(cut_OR_mva90)+" Events passing either trig (WP90) in Sample")
                cut_OR_mva8 = int(Rdf_OR_mva8.Count())
		print(str(cut_OR_mva8)+" Events passing either trig (WP8) in Sample")
                cut_OR_mva85 = int(Rdf_OR_mva85.Count())
		print(str(cut_OR_mva85)+" Events passing either trig (WP85) in Sample")
                cut_OR_mva9 = int(Rdf_OR_mva9.Count())
		print(str(cut_OR_mva9)+" Events passing either trig (WP9) in Sample")
		

		if F[2] == 1:
			t4_110 = Rdf_110.Histo1D(("t4_110", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110 = t4_110.Clone()
			t4_110.SetTitle("Photon pT")
			t4_110.SetXTitle("Photon pT")
			h4_110.Add(t4_110)
			
			t5_110 = Rdf_110.Histo2D(("t5_110", "Photon Eta vs. Photon pT", 30, -1.5, 1.5, 20, 150, 250), "pEta", "pPt", "weight")
			t5_110 = t5_110.Clone()
			t5_110.SetXTitle("Photon Eta")
			t5_110.SetYTitle("Photon pT")
			h5_110.Add(t5_110)
		
		t4_200 = Rdf_200.Histo1D(("t4_200", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200 = t4_200.Clone()
		t4_200.SetTitle("Photon pT")
		t4_200.SetXTitle("Photon pT")
		h4_200.Add(t4_200)
		
		t5_200 = Rdf_200.Histo2D(("t5_200", "Photon Eta vs. Photon pT", 30, -1.5, 1.5, 20, 150, 250), "pEta", "pPt", "weight")
		t5_200 = t5_200.Clone()
		t5_200.SetXTitle("Photon Eta")
		t5_200.SetYTitle("Photon pT")
		h5_200.Add(t5_200)
		
		t4_notrig = Rdf_notrig.Histo1D(("t4_notrig", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig = t4_notrig.Clone()
		t4_notrig.SetTitle("Photon pT")
		t4_notrig.SetXTitle("Photon pT")
		h4_notrig.Add(t4_notrig)
		
		t5_notrig = Rdf_notrig.Histo2D(("t5_notrig", "Photon Eta vs. Photon pT", 30, -1.5, 1.5, 20, 150, 250), "pEta", "pPt", "weight")
		t5_notrig = t5_notrig.Clone()
		t5_notrig.SetXTitle("Photon Eta")
		t5_notrig.SetYTitle("Photon pT")
		h5_notrig.Add(t5_notrig)
		
		t4_OR = Rdf_OR.Histo1D(("t4_OR", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR = t4_OR.Clone()
		t4_OR.SetTitle("Photon pT")
		t4_OR.SetXTitle("Photon pT")
		h4_OR.Add(t4_OR)
		
		t5_OR = Rdf_OR.Histo2D(("t5_OR", "Photon Eta vs. Photon pT", 30, -1.5, 1.5, 20, 150, 250), "pEta", "pPt", "weight")
		t5_OR = t5_OR.Clone()
		t5_OR.SetXTitle("Photon Eta")
		t5_OR.SetYTitle("Photon pT")
		h5_OR.Add(t5_OR)


                t4_notrig_thin = Rdf_notrig.Histo1D(("t4_notrig_thin", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin = t4_notrig_thin.Clone()
                t4_notrig_thin.SetTitle("Photon pT")
                t4_notrig_thin.SetXTitle("Photon pT")
                h4_notrig_thin.Add(t4_notrig_thin)

                t4_OR_thin = Rdf_OR.Histo1D(("t4_OR_thin", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin = t4_OR_thin.Clone()
                t4_OR_thin.SetTitle("Photon pT")
                t4_OR_thin.SetXTitle("Photon pT")
                h4_OR_thin.Add(t4_OR_thin)
		
		if F[2] == 1:
			t4_110_mva80 = Rdf_110_mva80.Histo1D(("t4_110_mva80", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110_mva80 = t4_110_mva80.Clone()
			t4_110_mva80.SetTitle("Photon pT")
			t4_110_mva80.SetXTitle("Photon pT")
			h4_110_mva80.Add(t4_110_mva80)
		
		t4_200_mva80 = Rdf_200_mva80.Histo1D(("t4_200_mva80", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200_mva80 = t4_200_mva80.Clone()
		t4_200_mva80.SetTitle("Photon pT")
		t4_200_mva80.SetXTitle("Photon pT")
		h4_200_mva80.Add(t4_200_mva80)
		
		t4_notrig_mva80 = Rdf_notrig_mva80.Histo1D(("t4_notrig_mva80", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig_mva80 = t4_notrig_mva80.Clone()
		t4_notrig_mva80.SetTitle("Photon pT")
		t4_notrig_mva80.SetXTitle("Photon pT")
		h4_notrig_mva80.Add(t4_notrig_mva80)
		
		t4_OR_mva80 = Rdf_OR_mva80.Histo1D(("t4_OR_mva80", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR_mva80 = t4_OR_mva80.Clone()
		t4_OR_mva80.SetTitle("Photon pT")
		t4_OR_mva80.SetXTitle("Photon pT")
		h4_OR_mva80.Add(t4_OR_mva80)


                t4_notrig_thin_mva80 = Rdf_notrig_mva80.Histo1D(("t4_notrig_thin_mva80", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin_mva80 = t4_notrig_thin_mva80.Clone()
                t4_notrig_thin_mva80.SetTitle("Photon pT")
                t4_notrig_thin_mva80.SetXTitle("Photon pT")
                h4_notrig_thin_mva80.Add(t4_notrig_thin_mva80)

                t4_OR_thin_mva80 = Rdf_OR_mva80.Histo1D(("t4_OR_thin_mva80", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin_mva80 = t4_OR_thin_mva80.Clone()
                t4_OR_thin_mva80.SetTitle("Photon pT")
                t4_OR_thin_mva80.SetXTitle("Photon pT")
                h4_OR_thin_mva80.Add(t4_OR_thin_mva80)
		
		if F[2] == 1:
			t4_110_mva90 = Rdf_110_mva90.Histo1D(("t4_110_mva90", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110_mva90 = t4_110_mva90.Clone()
			t4_110_mva90.SetTitle("Photon pT")
			t4_110_mva90.SetXTitle("Photon pT")
			h4_110_mva90.Add(t4_110_mva90)
		
		t4_200_mva90 = Rdf_200_mva90.Histo1D(("t4_200_mva90", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200_mva90 = t4_200_mva90.Clone()
		t4_200_mva90.SetTitle("Photon pT")
		t4_200_mva90.SetXTitle("Photon pT")
		h4_200_mva90.Add(t4_200_mva90)
		
		t4_notrig_mva90 = Rdf_notrig_mva90.Histo1D(("t4_notrig_mva90", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig_mva90 = t4_notrig_mva90.Clone()
		t4_notrig_mva90.SetTitle("Photon pT")
		t4_notrig_mva90.SetXTitle("Photon pT")
		h4_notrig_mva90.Add(t4_notrig_mva90)
		
		t4_OR_mva90 = Rdf_OR_mva90.Histo1D(("t4_OR_mva90", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR_mva90 = t4_OR_mva90.Clone()
		t4_OR_mva90.SetTitle("Photon pT")
		t4_OR_mva90.SetXTitle("Photon pT")
		h4_OR_mva90.Add(t4_OR_mva90)


                t4_notrig_thin_mva90 = Rdf_notrig_mva90.Histo1D(("t4_notrig_thin_mva90", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin_mva90 = t4_notrig_thin_mva90.Clone()
                t4_notrig_thin_mva90.SetTitle("Photon pT")
                t4_notrig_thin_mva90.SetXTitle("Photon pT")
                h4_notrig_thin_mva90.Add(t4_notrig_thin_mva90)

                t4_OR_thin_mva90 = Rdf_OR_mva90.Histo1D(("t4_OR_thin_mva90", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin_mva90 = t4_OR_thin_mva90.Clone()
                t4_OR_thin_mva90.SetTitle("Photon pT")
                t4_OR_thin_mva90.SetXTitle("Photon pT")
                h4_OR_thin_mva90.Add(t4_OR_thin_mva90)
		
		if F[2] == 1:
			t4_110_mva8 = Rdf_110_mva8.Histo1D(("t4_110_mva8", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110_mva8 = t4_110_mva8.Clone()
			t4_110_mva8.SetTitle("Photon pT")
			t4_110_mva8.SetXTitle("Photon pT")
			h4_110_mva8.Add(t4_110_mva8)
		
		t4_200_mva8 = Rdf_200_mva8.Histo1D(("t4_200_mva8", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200_mva8 = t4_200_mva8.Clone()
		t4_200_mva8.SetTitle("Photon pT")
		t4_200_mva8.SetXTitle("Photon pT")
		h4_200_mva8.Add(t4_200_mva8)
		
		t4_notrig_mva8 = Rdf_notrig_mva8.Histo1D(("t4_notrig_mva8", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig_mva8 = t4_notrig_mva8.Clone()
		t4_notrig_mva8.SetTitle("Photon pT")
		t4_notrig_mva8.SetXTitle("Photon pT")
		h4_notrig_mva8.Add(t4_notrig_mva8)
		
		t4_OR_mva8 = Rdf_OR_mva8.Histo1D(("t4_OR_mva8", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR_mva8 = t4_OR_mva8.Clone()
		t4_OR_mva8.SetTitle("Photon pT")
		t4_OR_mva8.SetXTitle("Photon pT")
		h4_OR_mva8.Add(t4_OR_mva8)


                t4_notrig_thin_mva8 = Rdf_notrig_mva8.Histo1D(("t4_notrig_thin_mva8", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin_mva8 = t4_notrig_thin_mva8.Clone()
                t4_notrig_thin_mva8.SetTitle("Photon pT")
                t4_notrig_thin_mva8.SetXTitle("Photon pT")
                h4_notrig_thin_mva8.Add(t4_notrig_thin_mva8)

                t4_OR_thin_mva8 = Rdf_OR_mva8.Histo1D(("t4_OR_thin_mva8", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin_mva8 = t4_OR_thin_mva8.Clone()
                t4_OR_thin_mva8.SetTitle("Photon pT")
                t4_OR_thin_mva8.SetXTitle("Photon pT")
                h4_OR_thin_mva8.Add(t4_OR_thin_mva8)
		
		if F[2] == 1:
			t4_110_mva85 = Rdf_110_mva85.Histo1D(("t4_110_mva85", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110_mva85 = t4_110_mva85.Clone()
			t4_110_mva85.SetTitle("Photon pT")
			t4_110_mva85.SetXTitle("Photon pT")
			h4_110_mva85.Add(t4_110_mva85)
		
		t4_200_mva85 = Rdf_200_mva85.Histo1D(("t4_200_mva85", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200_mva85 = t4_200_mva85.Clone()
		t4_200_mva85.SetTitle("Photon pT")
		t4_200_mva85.SetXTitle("Photon pT")
		h4_200_mva85.Add(t4_200_mva85)
		
		t4_notrig_mva85 = Rdf_notrig_mva85.Histo1D(("t4_notrig_mva85", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig_mva85 = t4_notrig_mva85.Clone()
		t4_notrig_mva85.SetTitle("Photon pT")
		t4_notrig_mva85.SetXTitle("Photon pT")
		h4_notrig_mva85.Add(t4_notrig_mva85)
		
		t4_OR_mva85 = Rdf_OR_mva85.Histo1D(("t4_OR_mva85", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR_mva85 = t4_OR_mva85.Clone()
		t4_OR_mva85.SetTitle("Photon pT")
		t4_OR_mva85.SetXTitle("Photon pT")
		h4_OR_mva85.Add(t4_OR_mva85)


                t4_notrig_thin_mva85 = Rdf_notrig_mva85.Histo1D(("t4_notrig_thin_mva85", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin_mva85 = t4_notrig_thin_mva85.Clone()
                t4_notrig_thin_mva85.SetTitle("Photon pT")
                t4_notrig_thin_mva85.SetXTitle("Photon pT")
                h4_notrig_thin_mva85.Add(t4_notrig_thin_mva85)

                t4_OR_thin_mva85 = Rdf_OR_mva85.Histo1D(("t4_OR_thin_mva85", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin_mva85 = t4_OR_thin_mva85.Clone()
                t4_OR_thin_mva85.SetTitle("Photon pT")
                t4_OR_thin_mva85.SetXTitle("Photon pT")
                h4_OR_thin_mva85.Add(t4_OR_thin_mva85)
		
		if F[2] == 1:
			t4_110_mva9 = Rdf_110_mva9.Histo1D(("t4_110_mva9", "Photon pT", 34, widebins), "pPt", "weight")
			t4_110_mva9 = t4_110_mva9.Clone()
			t4_110_mva9.SetTitle("Photon pT")
			t4_110_mva9.SetXTitle("Photon pT")
			h4_110_mva9.Add(t4_110_mva9)
		
		t4_200_mva9 = Rdf_200_mva9.Histo1D(("t4_200_mva9", "Photon pT", 34, widebins), "pPt", "weight")
		t4_200_mva9 = t4_200_mva9.Clone()
		t4_200_mva9.SetTitle("Photon pT")
		t4_200_mva9.SetXTitle("Photon pT")
		h4_200_mva9.Add(t4_200_mva9)
		
		t4_notrig_mva9 = Rdf_notrig_mva9.Histo1D(("t4_notrig_mva9", "Photon pT", 34, widebins), "pPt", "weight")
		t4_notrig_mva9 = t4_notrig_mva9.Clone()
		t4_notrig_mva9.SetTitle("Photon pT")
		t4_notrig_mva9.SetXTitle("Photon pT")
		h4_notrig_mva9.Add(t4_notrig_mva9)
		
		t4_OR_mva9 = Rdf_OR_mva9.Histo1D(("t4_OR_mva9", "Photon pT", 34, widebins), "pPt", "weight")
		t4_OR_mva9 = t4_OR_mva9.Clone()
		t4_OR_mva9.SetTitle("Photon pT")
		t4_OR_mva9.SetXTitle("Photon pT")
		h4_OR_mva9.Add(t4_OR_mva9)


                t4_notrig_thin_mva9 = Rdf_notrig_mva9.Histo1D(("t4_notrig_thin_mva9", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_notrig_thin_mva9 = t4_notrig_thin_mva9.Clone()
                t4_notrig_thin_mva9.SetTitle("Photon pT")
                t4_notrig_thin_mva9.SetXTitle("Photon pT")
                h4_notrig_thin_mva9.Add(t4_notrig_thin_mva9)

                t4_OR_thin_mva9 = Rdf_OR_mva9.Histo1D(("t4_OR_thin_mva9", "Photon pT", 500, 0, 500), "pPt", "weight")
                t4_OR_thin_mva9 = t4_OR_thin_mva9.Clone()
                t4_OR_thin_mva9.SetTitle("Photon pT")
                t4_OR_thin_mva9.SetXTitle("Photon pT")
                h4_OR_thin_mva9.Add(t4_OR_thin_mva9)
		
		
	ofile.WriteObject(h4_110, "photon_pt_110")
	ofile.WriteObject(h4_200, "photon_pt_200")
	ofile.WriteObject(h4_notrig, "photon_pt_notrig")
	ofile.WriteObject(h4_OR, "photon_pt_OR")
	
        ofile.WriteObject(h4_notrig_thin, "photon_pt_notrig_thin")
        ofile.WriteObject(h4_OR_thin, "photon_pt_OR_thin")
	
	ofile.WriteObject(h5_110, "photon_pt_eta_110")
	ofile.WriteObject(h5_200, "photon_pt_eta_200")
	ofile.WriteObject(h5_notrig, "photon_pt_eta_notrig")
	ofile.WriteObject(h5_OR, "photon_pt_eta_OR")
	
	ofile.WriteObject(h4_110_mva80, "photon_pt_110_mva80")
	ofile.WriteObject(h4_200_mva80, "photon_pt_200_mva80")
	ofile.WriteObject(h4_notrig_mva80, "photon_pt_notrig_mva80")
	ofile.WriteObject(h4_OR_mva80, "photon_pt_OR_mva80")
	
        ofile.WriteObject(h4_notrig_thin_mva80, "photon_pt_notrig_thin_mva80")
        ofile.WriteObject(h4_OR_thin_mva80, "photon_pt_OR_thin_mva80")

	ofile.WriteObject(h4_110_mva90, "photon_pt_110_mva90")
	ofile.WriteObject(h4_200_mva90, "photon_pt_200_mva90")
	ofile.WriteObject(h4_notrig_mva90, "photon_pt_notrig_mva90")
	ofile.WriteObject(h4_OR_mva90, "photon_pt_OR_mva90")
	
        ofile.WriteObject(h4_notrig_thin_mva90, "photon_pt_notrig_thin_mva90")
        ofile.WriteObject(h4_OR_thin_mva90, "photon_pt_OR_thin_mva90")

	ofile.WriteObject(h4_110_mva8, "photon_pt_110_mva8")
	ofile.WriteObject(h4_200_mva8, "photon_pt_200_mva8")
	ofile.WriteObject(h4_notrig_mva8, "photon_pt_notrig_mva8")
	ofile.WriteObject(h4_OR_mva8, "photon_pt_OR_mva8")
	
        ofile.WriteObject(h4_notrig_thin_mva8, "photon_pt_notrig_thin_mva8")
        ofile.WriteObject(h4_OR_thin_mva8, "photon_pt_OR_thin_mva8")

	ofile.WriteObject(h4_110_mva85, "photon_pt_110_mva85")
	ofile.WriteObject(h4_200_mva85, "photon_pt_200_mva85")
	ofile.WriteObject(h4_notrig_mva85, "photon_pt_notrig_mva85")
	ofile.WriteObject(h4_OR_mva85, "photon_pt_OR_mva85")
	
        ofile.WriteObject(h4_notrig_thin_mva85, "photon_pt_notrig_thin_mva85")
        ofile.WriteObject(h4_OR_thin_mva85, "photon_pt_OR_thin_mva85")

	ofile.WriteObject(h4_110_mva9, "photon_pt_110_mva9")
	ofile.WriteObject(h4_200_mva9, "photon_pt_200_mva9")
	ofile.WriteObject(h4_notrig_mva9, "photon_pt_notrig_mva9")
	ofile.WriteObject(h4_OR_mva9, "photon_pt_OR_mva9")
	
        ofile.WriteObject(h4_notrig_thin_mva9, "photon_pt_notrig_thin_mva9")
        ofile.WriteObject(h4_OR_thin_mva9, "photon_pt_OR_thin_mva9")


#	h4.SetTitle("Photon pT")
#	h4.SetXTitle("pT")

#	n4 = TCanvas()
#	n4.cd()
#	h4.Draw("hist")
#	n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pho_pt.png")
#	n4.Close()
	
	
	
	ofile.Write()
