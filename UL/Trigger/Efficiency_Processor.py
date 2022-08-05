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

	ROOT.gInterpreter.Declare("Double_t widebins[35] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")
	

	h4_MVA8 = TH1F("h4_MVA8", "Photon pT MVA>.8", 34, widebins)
	h4_MVA85 = TH1F("h4_MVA85", "Photon pT MVA>.85", 34, widebins)
	h4_MVA9 = TH1F("h4_MVA9", "Photon pT MVA>.9", 34, widebins)
	h4_WP90 = TH1F("h4_WP90", "Photon pT WP90", 34, widebins)
	h4_WP80 = TH1F("h4_WP80", "Photon pT WP80", 34, widebins)
	h4_allPho = TH1F("h4_allPho", "Photon pT (All Barrel)", 34, widebins)
	h4_bitmap = TH1F("h4_bitmap", "Photon pT Tight Bitmap_v2", 34, widebins)
	
	
	h5_mvaID = TH1F("h5_mvaID", "MVA Score", 100, -1, 1)

	tot_nocut = 0
	tot_precut = 0
	tot_presel = 0
	tot_cut_80 = 0
	tot_cut_90 = 0
	tot_cut_MVA8 = 0
	tot_cut_MVA85 = 0
	tot_cut_MVA9 = 0
	tot_cut_bit = 0
	tot_test = 0

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
		tot_nocut += nocut
		print(str(nocut)+" Events in Sample")

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
		Rdf_PreSel = Rdf_PreSel.Filter("GenPart_pdgId[Photon_genPartIdx[0]] == 22")
                precut = int(Rdf_PreSel.Count())
		tot_precut += precut
		print(str(precut)+" Events with nPhoton > 0 in Sample")
		Rdf_PreSel = Rdf_PreSel.Define("pPt", "Photon_pt[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pID", "Photon_mvaID[0]")
                Rdf_PreSel = Rdf_PreSel.Define("pID80", "Photon_mvaID_WP80")
		Rdf_PreSel = Rdf_PreSel.Define("pID90", "Photon_mvaID_WP90")
		Rdf_PreSel = Rdf_PreSel.Define("pEta", "Photon_eta[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pIso", "Photon_pfRelIso03_all[0]")
                Rdf_PreSel = Rdf_PreSel.Define("pCut", "Photon_cutBased[0]")
		Rdf_PreSel = Rdf_PreSel.Define("pR9", "Photon_r9[0]")
		Rdf_PreSel = Rdf_PreSel.Define("weight", F[1])

		Rdf_PreSel = Rdf_PreSel.Filter("abs(pEta) < 1.44")
                presel = int(Rdf_PreSel.Count())
		tot_presel += presel
		print(str(presel)+" Events with a photon in the barrel in Sample")
		
		Rdf_test = Rdf_PreSel.Filter("pPt > 75")
                test = int(Rdf_test.Count())
		tot_test += test
		print(str(test)+" Events with a photon in the barrel > 75 GeV in Sample")
		
		t5_mvaID = Rdf_PreSel.Histo1D(("t5_mvaID", "MVA Score", 100, -1, 1), "pID", "weight")
		t5_mvaID = t5_mvaID.Clone()
		t5_mvaID.SetTitle("MVA Score")
		t5_mvaID.SetXTitle("MVA Score")
		h5_mvaID.Add(t5_mvaID)
		
		Rdf_WP80 = Rdf_PreSel.Filter("pID80[0] > 0")
                cut_80 = int(Rdf_WP80.Count())
		tot_cut_80 += cut_80
		print(str(cut_80)+" Events passing WP80 in Sample")
		
		Rdf_WP90 = Rdf_PreSel.Filter("pID90[0] > 0")
                cut_90 = int(Rdf_WP90.Count())
		tot_cut_90 += cut_90
		print(str(cut_90)+" Events passing WP90 in Sample")
		
		Rdf_MVA8 = Rdf_PreSel.Filter("pID > 0.8")
                cut_MVA8 = int(Rdf_MVA8.Count())
		tot_cut_MVA8 += cut_MVA8
		print(str(cut_MVA8)+" Events passing with MVA score > .8 in Sample")
		
		Rdf_MVA85 = Rdf_PreSel.Filter("pID > 0.85")
                cut_MVA85 = int(Rdf_MVA85.Count())
		tot_cut_MVA85 += cut_MVA85
		print(str(cut_MVA85)+" Events passing with MVA score > .85 in Sample")
		
		Rdf_MVA9 = Rdf_PreSel.Filter("pID > 0.9")
                cut_MVA9 = int(Rdf_MVA9.Count())
		tot_cut_MVA9 += cut_MVA9
		print(str(cut_MVA9)+" Events passing with MVA score > .9 in Sample")
		
		Rdf_bit = Rdf_PreSel.Filter("pCut >= 3")
                cut_bit = int(Rdf_bit.Count())
		tot_cut_bit += cut_bit
		print(str(cut_bit)+" Events passing Tight Bitmap_v2 in Sample")
		

		t4_MVA8 = Rdf_MVA8.Histo1D(("t4_MVA8", "Photon pT", 34, widebins), "pPt", "weight")
		t4_MVA8 = t4_MVA8.Clone()
		t4_MVA8.SetTitle("Photon pT")
		t4_MVA8.SetXTitle("Photon pT")
		h4_MVA8.Add(t4_MVA8)
		
		t4_MVA85 = Rdf_MVA85.Histo1D(("t4_MVA85", "Photon pT", 34, widebins), "pPt", "weight")
		t4_MVA85 = t4_MVA85.Clone()
		t4_MVA85.SetTitle("Photon pT")
		t4_MVA85.SetXTitle("Photon pT")
		h4_MVA85.Add(t4_MVA85)
		
		t4_MVA9 = Rdf_MVA9.Histo1D(("t4_MVA9", "Photon pT", 34, widebins), "pPt", "weight")
		t4_MVA9 = t4_MVA9.Clone()
		t4_MVA9.SetTitle("Photon pT")
		t4_MVA9.SetXTitle("Photon pT")
		h4_MVA9.Add(t4_MVA9)
		
		t4_allPho = Rdf_PreSel.Histo1D(("t4_allPho", "Photon pT", 34, widebins), "pPt", "weight")
		t4_allPho = t4_allPho.Clone()
		t4_allPho.SetTitle("Photon pT")
		t4_allPho.SetXTitle("Photon pT")
		h4_allPho.Add(t4_allPho)
		
		t4_WP80 = Rdf_WP80.Histo1D(("t4_WP80", "Photon pT", 34, widebins), "pPt", "weight")
		t4_WP80 = t4_WP80.Clone()
		t4_WP80.SetTitle("Photon pT")
		t4_WP80.SetXTitle("Photon pT")
		h4_WP80.Add(t4_WP80)
		
		t4_WP90 = Rdf_WP90.Histo1D(("t4_WP90", "Photon pT", 34, widebins), "pPt", "weight")
		t4_WP90 = t4_WP90.Clone()
		t4_WP90.SetTitle("Photon pT")
		t4_WP90.SetXTitle("Photon pT")
		h4_WP90.Add(t4_WP90)

		t4_bitmap = Rdf_bit.Histo1D(("t4_bitmap", "Photon pT", 34, widebins), "pPt", "weight")
		t4_bitmap = t4_bitmap.Clone()
		t4_bitmap.SetTitle("Photon pT")
		t4_bitmap.SetXTitle("Photon pT")
		h4_bitmap.Add(t4_bitmap)
		
		
	


	print("Total Events in Sample: "+str(tot_nocut))
	print("Total Events with nPhoton>0 in Sample: "+str(tot_precut))
	print("Total Events with a Photon in the Barrel in Sample: "+str(tot_presel))
	print("Total Events in the Barrel Passing WP80 in Sample: "+str(tot_cut_80))
	print("Total Events in the Barrel Passing WP90 in Sample: "+str(tot_cut_90))
	print("Total Events in the Barrel Passing MVA Score > .8 in Sample: "+str(tot_cut_MVA8))
	print("Total Events in the Barrel Passing MVA Score > .85 in Sample: "+str(tot_cut_MVA85))
	print("Total Events in the Barrel Passing MVA Score > .9 in Sample: "+str(tot_cut_MVA9))
	print("Total Events in the Barrel Passing Tight Bitmap_v2 in Sample: "+str(tot_cut_bit))
	print("Total Events with a photon in the barrel > 75 GeV in Sample: "+str(tot_test))
	
	ofile.WriteObject(h4_WP80, "photon_pt_WP80")
	ofile.WriteObject(h4_WP90, "photon_pt_WP90")
	ofile.WriteObject(h4_MVA8, "photon_pt_MVA8")
	ofile.WriteObject(h4_MVA85, "photon_pt_MVA85")
	ofile.WriteObject(h4_MVA9, "photon_pt_MVA9")
	ofile.WriteObject(h4_allPho, "photon_pt_allPho")
	ofile.WriteObject(h4_bitmap, "photon_pt_bitmap")

	ofile.WriteObject(h5_mvaID, "mva_score")



#	n4 = TCanvas()
#	n4.cd()
#	h4.Draw("hist")
#	n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pho_pt.png")
#	n4.Close()
	
	
	
	ofile.Write()
