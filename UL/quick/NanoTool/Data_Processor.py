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



def DataPro(sample, fname, cut_hist, percentage=20):

	gROOT.SetBatch(True)

	ofile = ROOT.TFile("RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()


	rho_bins = cut_hist.GetNbinsX()
	pt_bins = cut_hist.GetNbinsY()

		

#	h1 = TH1F("h1", "N2", 25, 0, .5)
	h2 = TH1F("h2", "Softdrop Mass", 40, 0, 200)
	h4 = TH1F("h4", "Photon Pt", 40, 0, 1000)
	h5 = TH1F("h5", "Jet Pt", 40, 0, 2000)
        h5_1 = TH1F("h5_1", "Thin Jet Pt", 2000, 0, 2000)
	h6 = TH1F("h6", "Jet Eta", 20, -2.5, 2.5)
#	h7 = TH1F("h7", "Rho", 28, -8, -1)
	h7_1 = TH1F("h7_1", "Rho", 28, -8, -1)	
	h8 = TH1F("h8", "Photon Eta", 20, -2.5, 2.5)
#	h9 = TH1F("h9", "N2DDT", 50, -.5, .5)

	h11 = TH2F("n2_n2ddt", "N2 vs. N2DDT", 25, 0, .5, 50, -.5, .5)
	h12 = TH1F("N2", "N2", 25, 0, .5)
	h13 = TH1F("N2DDT", "N2DDT", 50, -.5, .5)
	h14 = TH2F("n2_soft", "N2 vs. Softdrop Mass", 25, 0, .5, 40, 0, 200)
	h15 = TH2F("n2ddt_soft", "N2DDT vs. Softdrop Mass", 50, -.5, .5, 40, 0, 200)
	h15_1 = TH2F("soft_n2ddt", "Softdrop Mass vs. N2DDT", 40, 0, 200, 50, -.5, .5)
	
	h16 = TH2F("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h17 = TH2F("rho_soft_pass", "Passing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h18 = TH2F("rho_soft_fail", "Failing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h19 = TH2F("n2_pt", "N2 vs. Jet pT", 25, 0, .5, 40, 0, 2000)
	h20 = TH2F("n2ddt_pt", "N2DDT vs. Jet pT", 50, -.5, .5, 40, 0, 2000)
	h20_1 = TH2F("pt_n2ddt", "Jet pT vs. N2DDT", 40, 0, 2000, 50, -.5, .5)

	#Wide bin declaration
	ROOT.gInterpreter.Declare("Double_t widebins[9] = {0, 125, 135, 145, 160, 175, 200, 245, 2000};")
 	h21 = TH2F("jet_pt_soft_pass", "Passing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)
        h21_w = TH2F("jet_pt_soft_pass_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200)
        h21_1 = TH2F("jet_pt_soft_total", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)
        h21_1_w = TH2F("jet_pt_soft_total_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200)
        h22 = TH2F("jet_pt_soft2", "Passing Jet pT vs. Softdrop Mass (Coarse)", 20, 0, 2000, 20, 0, 200)
        h23 = TH2F("jet_pt_soft_fail", "Failing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)
        h23_w = TH2F("jet_pt_soft_fail_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200)


	h24 = TH2F("jet_pt_rho_pass", "Passing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1)
	h25 = TH2F("jet_pt_rho_fail", "Failing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1)
	
	ROOT.gInterpreter.Declare("Double_t widebins3[15] = {0, 120, 135, 155, 175, 200, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
        h26_w = TH2F("jet_pt_soft_pass_wide3", "Passing Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200)
        h27_w = TH2F("jet_pt_soft_total_wide3", "Total Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200)
        h28_w = TH2F("jet_pt_soft_fail_wide3", "Failing Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200)
	
	ROOT.gInterpreter.Declare("Double_t widebins4[16] = {0, 120, 130, 145, 160, 180, 200, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
        h29_w = TH2F("jet_pt_soft_pass_wide4", "Passing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        h30_w = TH2F("jet_pt_soft_total_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        h31_w = TH2F("jet_pt_soft_fail_wide4", "Failing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)


	p1 = TH1F("p1", "passing softdrop mass", 40, 0, 200)
	p1_1 = TH1F("p1_1", "passing softdrop mass with overlap removed", 40, 0, 200)
	p2 = TH1F("p2", "passing photon pt", 40, 0, 1000)
	p3 = TH1F("p3", "passing jet pt", 40, 0, 2000)
	p4 = TH1F("p4", "passing rho", 28, -8, -1)
	p5 = TH1F("p5", "passing photon eta", 20, -2.5, 2.5)
	p6 = TH1F("p6", "passing jet eta", 20, -2.5, 2.5)

	f1 = TH1F("f1", "failing softdrop mass", 40, 0, 200)
	f2 = TH1F("f2", "passing photon pt", 40, 0, 1000)
	f3 = TH1F("f3", "passing jet pt", 40, 0, 2000)
	f4 = TH1F("f4", "passing rho", 28, -8, -1)
	f5 = TH1F("f5", "passing photon eta", 20, -2.5, 2.5)
	f6 = TH1F("f6", "passing jet eta", 20, -2.5, 2.5)

#	sig10 = TH1F("sig10", "Softdrop Mass in 10 GeV Signal Region", 40, 0, 200)
#	sig25 = TH1F("sig25", "Softdrop Mass in 25 GeV Signal Region", 40, 0, 200)
#	sig50 = TH1F("sig50", "Softdrop Mass in 50 GeV Signal Region", 40, 0, 200)
#	sig75 = TH1F("sig75", "Softdrop Mass in 75 GeV Signal Region", 40, 0, 200)
#	sig100 = TH1F("sig100", "Softdrop Mass in 100 GeV Signal Region", 40, 0, 200)
#	sig125 = TH1F("sig125", "Softdrop Mass in 125 GeV Signal Region", 40, 0, 200)
	
#	sig_thin10 = TH1F("sig_thin10", "Softdrop Mass in Thin 10 GeV Signal Region", 40, 0, 200)
#	sig_thin25 = TH1F("sig_thin25", "Softdrop Mass in Thin 25 GeV Signal Region", 40, 0, 200)
#	sig_thin50 = TH1F("sig_thin50", "Softdrop Mass in Thin 50 GeV Signal Region", 40, 0, 200)
#	sig_thin75 = TH1F("sig_thin75", "Softdrop Mass in Thin 75 GeV Signal Region", 40, 0, 200)
#	sig_thin100 = TH1F("sig_thin100", "Softdrop Mass in Thin 100 GeV Signal Region", 40, 0, 200)
#	sig_thin125 = TH1F("sig_thin125", "Softdrop Mass in Thin 125 GeV Signal Region", 40, 0, 200)

	nocut = 0
	npcut = 0
	njcut = 0
	pcut = 0
	jcut = 0
	nsubcut = 0

	trigcut = 0

	final = 0

	pass_events = 0
	fail_events = 0

	total_events = 0
	num_pass = 0
	ppt_pass = 0
	jpt_pass = 0
	peta_pass = 0
	jeta_pass = 0
	pid_pass = 0
	jid_pass = 0
	jsoft_pass = 0
	trig_pass = 0
	n2_pass = 0
	rho_pass = 0
	dR_pass = 0
	ten_pass = 0
	pass_pass_weight = 0
	fail_pass_weight = 0
	pass_pass = 0
	fail_pass = 0
#	pass_sig_pass10 = 0
#	pass_sig_pass25 = 0
#	pass_sig_pass50 = 0
#	pass_sig_pass75 = 0
#	pass_sig_pass100 = 0
#	pass_sig_pass125 = 0
#	pass_sig_pass_weight10 = 0
#	pass_sig_pass_weight25 = 0
#	pass_sig_pass_weight50 = 0
#	pass_sig_pass_weight75 = 0
#	pass_sig_pass_weight100 = 0
#	pass_sig_pass_weight125 = 0
	
#	pass_sig_thin_pass10 = 0
#	pass_sig_thin_pass25 = 0
#	pass_sig_thin_pass50 = 0
#	pass_sig_thin_pass75 = 0
#	pass_sig_thin_pass100 = 0
#	pass_sig_thin_pass125 = 0
#	pass_sig_thin_pass_weight10 = 0
#	pass_sig_thin_pass_weight25 = 0
#	pass_sig_thin_pass_weight50 = 0
#	pass_sig_thin_pass_weight75 = 0
#	pass_sig_thin_pass_weight100 = 0
#	pass_sig_thin_pass_weight125 = 0


	slicenum = 0	

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
		slicenum += 1
		#Individual Slice Cutflow values
		total_events_slice = 0
		num_pass_slice = 0
		ppt_pass_slice = 0
		jpt_pass_slice = 0
		peta_pass_slice = 0
		jeta_pass_slice = 0
		pid_pass_slice = 0
		jid_pass_slice = 0
		jsoft_pass_slice = 0
		trig_pass_slice = 0
		n2_pass_slice = 0
		rho_pass_slice = 0
		dR_pass_slice = 0
		ten_pass_slice = 0
		pass_pass_weight_slice = 0
		fail_pass_weight_slice = 0
		pass_pass_slice = 0
		fail_pass_slice = 0
#		pass_sig_pass10_slice = 0
#		pass_sig_pass25_slice = 0
#		pass_sig_pass50_slice = 0
#		pass_sig_pass75_slice = 0
#		pass_sig_pass100_slice = 0
#		pass_sig_pass125_slice = 0
#		pass_sig_pass_weight10_slice = 0
#		pass_sig_pass_weight25_slice = 0
#		pass_sig_pass_weight50_slice = 0
#		pass_sig_pass_weight75_slice = 0
#		pass_sig_pass_weight100_slice = 0
#		pass_sig_pass_weight125_slice = 0
		
#		pass_sig_thin_pass10_slice = 0
#		pass_sig_thin_pass25_slice = 0
#		pass_sig_thin_pass50_slice = 0
#		pass_sig_thin_pass75_slice = 0
#		pass_sig_thin_pass100_slice = 0
#		pass_sig_thin_pass125_slice = 0
#		pass_sig_thin_pass_weight10_slice = 0
#		pass_sig_thin_pass_weight25_slice = 0
#		pass_sig_thin_pass_weight50_slice = 0
#		pass_sig_thin_pass_weight75_slice = 0
#		pass_sig_thin_pass_weight100_slice = 0
#		pass_sig_thin_pass_weight125_slice = 0
	
		Rdf_noCut = RDF(Chain)
	#	Rdf_PreSel = Rdf_noCut.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 > 0) && nPhoton > 0. && nselectedPatJetsAK8PFPuppi > 0. && selectedPatJetsAK8PFPuppi_msoftdrop_nom.size()>0")
		
		Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0")

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")

		Rdf_PreSel = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")

	       
	
		#ROOT.gInterpreter.Declare('#include "Help.h"')
		Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_msoftdrop_nom, selectedPatJetsAK8PFPuppi_jetId)")
		Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")
#		Rdf_PreSel = Rdf_PreSel.Define("Nsubjet", "nselectedPatJetsAK8PFPuppiSoftDrop_Subjets")

		Rdf = Rdf_PreSel.Filter("pIndex >= 0")
		
		Rdf = Rdf.Filter("jIndex >= 0")
		
		Rdf = Rdf.Define("jM", "selectedPatJetsAK8PFPuppi_msoftdrop_nom[jIndex]")
		Rdf = Rdf.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
		Rdf = Rdf.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
		Rdf = Rdf.Define("jPt", "selectedPatJetsAK8PFPuppi_pt_nom[jIndex]")
		Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
		Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
		Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
		Rdf = Rdf.Define("N2", "selectedPatJetsAK8PFPuppi_ak8PFJetsPuppiSoftDropValueMap_nb1AK8PuppiSoftDropN2[jIndex]")
		Rdf = Rdf.Define("jID", "selectedPatJetsAK8PFPuppi_jetId[jIndex]")
		Rdf = Rdf.Define("n2ddt", "ddt(jPt, jM, N2)")

		Rdf = Rdf.Define("Rho", "rho(jPt, jM)")

		Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
                Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")
		Rdf = Rdf.Define("weight", F[1])
		
		if F[2] == 1: 
			Rdf_Trig = Rdf.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 >0.0)")
		elif F[2] == 2:
			Rdf_Trig = Rdf.Filter("(HLT_Photon200 >0.0)")


		Rdf_Final = Rdf_Trig.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2")

		Rdf_Pass = Rdf_Final.Filter("n2ddt<0")
		Rdf_Fail = Rdf_Final.Filter("n2ddt>0")

		t2 = Rdf_Final.Histo1D(("t2", "Softdrop Mass", 40, 0, 200), "jM", "weight")
		t2 = t2.Clone()
		t2.SetTitle("Softdrop Mass")
		t2.SetXTitle("Softdrop Mass")
		h2.Add(t2)

		t4 = Rdf_Final.Histo1D(("t4", "Photon Pt", 40, 0, 1000), "pPt", "weight")
		t4 = t4.Clone()
		t4.SetTitle("Photon Pt")
		t4.SetXTitle("Pt")
		h4.Add(t4)
		
		t5 = Rdf_Final.Histo1D(("t5", "Jet Pt", 40, 0, 2000), "jPt", "weight")
		t5 = t5.Clone()
		t5.SetTitle("Jet Pt")
		t5.SetXTitle("Pt")
		h5.Add(t5)

                t5_1 = Rdf_Final.Histo1D(("t5_1", "Thin Jet Pt", 2000, 0, 2000), "jPt", "weight")
                t5_1 = t5_1.Clone()
                t5_1.SetTitle("Thin Jet Pt")
                t5_1.SetXTitle("Pt")
                h5_1.Add(t5_1)

		t6 = Rdf_Final.Histo1D(("t6", "Jet Eta", 20, -2.5, 2.5), "jEta", "weight")
		t6 = t6.Clone()
		t6.SetTitle("Jet Eta")
		t6.SetXTitle("Eta")
		h6.Add(t6)


#		t7 = Rdf.Histo1D(("t7", "Rho", 28, -8, -1), "Rho", "weight")
#		t7 = t7.Clone()
#		t7.SetTitle("Rho")
#		t7.SetXTitle("Rho")
#		h7.Add(t7)

		print("Make Photon Eta Histogram")

		t8 = Rdf_Final.Histo1D(("t8", "Photon Eta", 20, -2.5, -2.5), "pEta", "weight")
		print("Clone Photon Eta Histogram")
		t8 = t8.Clone()
		t8.SetTitle("Photon Eta")
		t8.SetXTitle("Eta")
		print("Combine Photon Eta Histogram")
		h8.Add(t8)
#		
#		t9 = Rdf.Histo1D(("t9", "N2DDT", 50, -.5, .5), "n2ddt", "weight")
#		t9 = t9.Clone()
#		t9.SetTitle("N2DDT")
#		t9.SetXTitle("N2DDT")
#		h9.Add(t9)
#

		q1 = Rdf_Pass.Histo1D(("q1", "Passing Softdrop Mass", 40, 0, 200), "jM", "weight")
		q1 = q1.Clone()
		q1.SetTitle("Passing Softdrop Mass")
		q1.SetXTitle("Softdrop Mass")
		p1.Add(q1)
		
		q2 = Rdf_Pass.Histo1D(("q2", "Passing Photon pT", 40, 0, 1000), "pPt", "weight")
		q2 = q2.Clone()
		q2.SetTitle("Passing Photon pT")
		q2.SetXTitle("Photon pT")
		p2.Add(q2)
		
		q3 = Rdf_Pass.Histo1D(("q3", "Passing Jet pT", 40, 0, 2000), "jPt", "weight")
		q3 = q3.Clone()
		q3.SetTitle("Passing Jet pT")
		q3.SetXTitle("Jet pT")
		p3.Add(q3)
		
		q4 = Rdf_Pass.Histo1D(("q4", "Passing Rho", 28, -8, -1), "Rho", "weight")
		q4 = q4.Clone()
		q4.SetTitle("Passing Rho")
		q4.SetXTitle("Rho")
		p4.Add(q4)
		
		q5 = Rdf_Pass.Histo1D(("q5", "Passing Photon Eta", 20, -2.5, 2.5), "pEta", "weight")
		q5 = q5.Clone()
		q5.SetTitle("Passing Photon Eta")
		q5.SetXTitle("Photon Eta")
		p5.Add(q5)
		
		q6 = Rdf_Pass.Histo1D(("q6", "Passing Jet Eta", 20, -2.5, 2.5), "jEta", "weight")
		q6 = q6.Clone()
		q6.SetTitle("Passing Jet Eta")
		q6.SetXTitle("Jet Eta")
		p6.Add(q6)
		
		u1 = Rdf_Fail.Histo1D(("u1", "Failing Softdrop Mass", 40, 0, 200), "jM", "weight")
		u1 = u1.Clone()
#		u1.Scale(1.0/9.0)
		u1.SetTitle("Failing Softdrop Mass")
		u1.SetXTitle("Softdrop Mass")
		f1.Add(u1)
		
		u2 = Rdf_Fail.Histo1D(("u2", "Failing Photon pT", 40, 0, 1000), "pPt", "weight")
		u2 = u2.Clone()
#		u2.Scale(1.0/9.0)
		u2.SetTitle("Failing Photon pT")
		u2.SetXTitle("Photon pT")
		f2.Add(u2)
		
		u3 = Rdf_Fail.Histo1D(("u3", "Failing Jet pT", 40, 0, 2000), "jPt", "weight")
		u3 = u3.Clone()
#		u3.Scale(1.0/9.0)
		u3.SetTitle("Failing Jet pT")
		u3.SetXTitle("Jet pT")
		f3.Add(u3)
		
		u4 = Rdf_Fail.Histo1D(("u4", "Failing Rho", 28, -8, -1), "Rho", "weight")
		u4 = u4.Clone()
#		u4.Scale(1.0/9.0)
		u4.SetTitle("Failing Rho")
		u4.SetXTitle("Rho")
		f4.Add(u4)
		
		u5 = Rdf_Fail.Histo1D(("u5", "Failing Photon Eta", 20, -2.5, 2.5), "pEta", "weight")
		u5 = u5.Clone()
#		u5.Scale(1.0/9.0)
		u5.SetTitle("Failing Photon Eta")
		u5.SetXTitle("Photon Eta")
		f5.Add(u5)
		
		u6 = Rdf_Fail.Histo1D(("u6", "Failing Jet Eta", 20, -2.5, 2.5), "jEta", "weight")
		u6 = u6.Clone()
#		u6.Scale(1.0/9.0)
		u6.SetTitle("Failing Jet Eta")
		u6.SetXTitle("Jet Eta")
		f6.Add(u6)
		
		j11 =  Rdf_Final.Histo2D(("n2_n2ddt", "N2 vs. N2DDT", 25, 0, .5, 50, -.5, .5), "N2", "n2ddt", "weight")
		j11 = j11.Clone()
		h11.Add(j11)

		j12 = Rdf_Final.Histo1D(("N2",  ';N^{2}_{1}', 25, 0, .5), "N2", "weight")
		j12 = j12.Clone()
		h12.Add(j12)
		
		j13 = Rdf_Final.Histo1D(("N2DDT",  "N2DDT", 50, -.5, .5), "n2ddt", "weight")
		j13 = j13.Clone()
		h13.Add(j13)
		
		j14 = Rdf_Final.Histo2D(("n2_soft", "N2 vs. Softdrop Mass", 25, 0, .5, 40, 0, 200), "N2", "jM", "weight")
		j14 = j14.Clone()
		h14.Add(j14)

		j15 = Rdf_Final.Histo2D(("n2ddt_soft", "N2DDT vs. Softdrop Mass", 50, -.5, .5, 40, 0, 200), "n2ddt", "jM", "weight")
		j15 = j15.Clone()
		h15.Add(j15)
		
		j15_1 = Rdf_Final.Histo2D(("soft_n2ddt", "Softdrop Mass vs. N2DDT", 40, 0, 200, 50, -.5, .5), "jM", "n2ddt", "weight")
		j15_1 = j15_1.Clone()
		h15_1.Add(j15_1)

		j16 = Rdf_Final.Histo2D(("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200), "Rho", "jM", "weight")
		j16 = j16.Clone()
		h16.Add(j16)

		j19 = Rdf_Final.Histo2D(("n2_pt", "N2 vs. Jet pT", 25, 0, .5, 40, 0, 2000), "N2", "jPt", "weight")
		j19 = j19.Clone()
		h19.Add(j19)

		j20 = Rdf_Final.Histo2D(("n2ddt_pt", "N2DDT vs. Jet pT", 50, -.5, .5, 40, 0, 2000), "n2ddt", "jPt", "weight")
		j20 = j20.Clone()
		h20.Add(j20)
		
		j20_1 = Rdf_Final.Histo2D(("pt_n2ddt", "Jet pT vs. N2DDT", 40, 0, 2000, 50, -.5, .5), "jPt", "n2ddt", "weight")
		j20_1 = j20_1.Clone()
		h20_1.Add(j20_1)

                j21 = Rdf_Pass.Histo2D(("pt_soft_pass", "Passing Jet pT vs. N2DDT", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
                j21 = j21.Clone()
                h21.Add(j21)

                j21_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide", "Passing Jet pT vs. N2DDT", 8, widebins, 40, 0, 200), "jPt", "jM", "weight")
                j21_w = j21_w.Clone()
                h21_w.Add(j21_w)

                j21_1 = Rdf_Final.Histo2D(("pt_soft_tot", "Total Jet pT vs. N2DDT", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
                j21_1 = j21_1.Clone()
                h21_1.Add(j21_1)

                j21_1_w = Rdf_Final.Histo2D(("pt_soft_tot_wide", "Total Jet pT vs. N2DDT", 8, widebins, 40, 0, 200), "jPt", "jM", "weight")
                j21_1_w = j21_1_w.Clone()
                h21_1_w.Add(j21_1_w)

                j22 = Rdf_Pass.Histo2D(("pt_soft2", "Passing Jet pT vs. N2DDT (Coarse)", 20, 0, 2000, 20, 0, 200), "jPt", "jM", "weight")
                j22 = j22.Clone()
                h22.Add(j22)

                j23 = Rdf_Fail.Histo2D(("pt_soft_fail", "Failing Jet pT vs. N2DDT", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
                j23 = j23.Clone()
                h23.Add(j23)

                j23_w = Rdf_Fail.Histo2D(("pt_soft_fail_wide", "Failing Jet pT vs. N2DDT", 8, widebins, 40, 0, 200), "jPt", "jM", "weight")
                j23_w = j23_w.Clone()
                h23_w.Add(j23_w)
        

                
		j26_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide3", "Passing Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200), "jPt", "jM", "weight")
                j26_w = j26_w.Clone()
                h26_w.Add(j26_w)
		
		j27_w = Rdf_Final.Histo2D(("pt_soft_tot_wide3", "Total Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200), "jPt", "jM", "weight")
                j27_w = j27_w.Clone()
                h27_w.Add(j27_w)
		
		j28_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide3", "Failing Jet pT vs. Softdrop Mass", 14, widebins3, 40, 0, 200), "jPt", "jM", "weight")
                j28_w = j28_w.Clone()
                h28_w.Add(j28_w)
	
                j29_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide4", "Passing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
                j29_w = j29_w.Clone()
                h29_w.Add(j29_w)

                j30_w = Rdf_Final.Histo2D(("pt_soft_tot_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
                j30_w = j30_w.Clone()
                h30_w.Add(j30_w)

                j31_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide4", "Failing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
                j31_w = j31_w.Clone()
                h31_w.Add(j31_w)

	

		j24 = Rdf_Pass.Histo2D(("pt_rho_pass", "Passing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1), "jPt", "Rho", "weight")
		j24 = j24.Clone()
		h24.Add(j24)

		j25 = Rdf_Fail.Histo2D(("pt_rho_fail", "Failing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1), "jPt", "Rho", "weight")
		j25 = j25.Clone()
		h25.Add(j25)

		t7_1 = Rdf_Final.Histo1D(("t7_1", "Rho", 28, -8, -1), "Rho", "weight")
		t7_1 = t7_1.Clone()
		t7_1.SetTitle("Rho")
		t7_1.SetXTitle("Rho")
		h7_1.Add(t7_1)


#	ofile.WriteObject(h1, "test_N2")
	ofile.WriteObject(h2, "softdrop")
	ofile.WriteObject(h4, "photon_pt")
	ofile.WriteObject(h5, "jet_pt")
        ofile.WriteObject(h5_1, "thin_jet_pt")
	ofile.WriteObject(h6, "jet_eta")
  #      ofile.WriteObject(h7, "test_rho")
	ofile.WriteObject(h8, "photon_eta")

	ofile.WriteObject(p1, "pass_soft")
	ofile.WriteObject(p1_1, "pass_soft_over")
	ofile.WriteObject(p2, "pass_photon_pt")
	ofile.WriteObject(p3, "pass_jet_pt")
	ofile.WriteObject(p4, "pass_rho")
	ofile.WriteObject(p5, "pass_photon_eta")
	ofile.WriteObject(p6, "pass_jet_eta")

	ofile.WriteObject(f1, "fail_soft")
	ofile.WriteObject(f2, "fail_photon_pt")
	ofile.WriteObject(f3, "fail_jet_pt")
	ofile.WriteObject(f4, "fail_rho")
	ofile.WriteObject(f5, "fail_photon_eta")
	ofile.WriteObject(f6, "fail_jet_eta")
	

	p1.SetXTitle("Softdrop Mass")

	
	h2.SetTitle("Softdrop Mass")
	h2.SetXTitle("Softdrop Mass")

	
	h4.SetTitle("Photon pT")
	h4.SetXTitle("pT")

	
	h5.SetTitle("Jet pT")
	h5.SetXTitle("pT")


	h5_1.SetTitle("Thin Jet pT")
	h5_1.SetXTitle("Jet pT")


	
	h6.SetTitle("Jet Eta")
	h6.SetXTitle("Eta")

	
	h8.SetTitle("Photon Eta")
	h8.SetXTitle("Eta")


	
	h11.SetTitle("N2 vs. N2DDT")
	h11.SetXTitle("N2")
	h11.SetYTitle("N2DDT")
	ofile.WriteObject(h11, "n2_n2ddt")
	

	
	h12.SetTitle("N2")
	h12.SetXTitle("N2")
	ofile.WriteObject(h12, "N2")
	
	
	h13.SetTitle("N2DDT")
	h13.SetXTitle("N2DDT")
	ofile.WriteObject(h13, "N2DDT")

	
	h14.SetTitle("N2 vs. Softdrop Mass")
	h14.SetXTitle("N2")
	h14.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h14, "n2_soft")

	
	h15.SetTitle("N2DDT vs. Softdrop Mass")
	h15.SetXTitle("N2DDT")
	h15.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h15, "n2ddt_soft")

	
	h15_1.SetTitle("Softdrop Mass vs. N2DDT")
	h15_1.SetYTitle("N2DDT")
	h15_1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h15_1, "soft_n2ddt")


	h16.SetTitle("Rho vs. Softdrop Mass")
	h16.SetXTitle("Rho")
	h16.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h16, "rho_soft")



	h19.SetTitle("N2 vs. Jet pT")
	h19.SetXTitle("N2")
	h19.SetYTitle("Jet pT")
	ofile.WriteObject(h19, "n2_jet_pt")


	h20.SetTitle("N2DDT vs. Jet pT")
	h20.SetXTitle("N2DDT")
	h20.SetYTitle("Jet pT")
	ofile.WriteObject(h20, "n2ddt_jet_pt")

	
	h20_1.SetTitle("Jet pT vs. N2DDT")
	h20_1.SetYTitle("N2DDT")
	h20_1.SetXTitle("Jet pT")
	ofile.WriteObject(h20_1, "jet_pt_n2ddt")


        h21.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h21.SetYTitle("Softdrop Mass")
        h21.SetXTitle("Jet pT")
        ofile.WriteObject(h21, "jet_pt_soft_pass")


        h21_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h21_w.SetYTitle("Softdrop Mass")
        h21_w.SetXTitle("Jet pT")
        ofile.WriteObject(h21_w, "jet_pt_soft_pass_wide")


        h21_1.SetTitle("Total Jet pT vs. Softdrop Mass")
        h21_1.SetYTitle("Softdrop Mass")
        h21_1.SetXTitle("Jet pT")
        ofile.WriteObject(h21_1, "jet_pt_soft_total")


        h21_1_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h21_1_w.SetYTitle("Softdrop Mass")
        h21_1_w.SetXTitle("Jet pT")
        ofile.WriteObject(h21_1_w, "jet_pt_soft_total_wide")


        h22.SetTitle("Passing Jet pT vs. Softdrop Mass (Coarse)")
        h22.SetYTitle("Softdrop Mass")
        h22.SetXTitle("Jet pT")
        ofile.WriteObject(h22, "jet_pt_soft2")


        h23.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h23.SetYTitle("Softdrop Mass")
        h23.SetXTitle("Jet pT")
        ofile.WriteObject(h23, "jet_pt_soft_fail")


        h23_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h23_w.SetYTitle("Softdrop Mass")
        h23_w.SetXTitle("Jet pT")
        ofile.WriteObject(h23_w, "jet_pt_soft_fail_wide")


	h26_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h26_w.SetYTitle("Softdrop Mass")
        h26_w.SetXTitle("Jet pT")
        ofile.WriteObject(h26_w, "jet_pt_soft_pass_wide3")



        h27_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h27_w.SetYTitle("Softdrop Mass")
        h27_w.SetXTitle("Jet pT")
        ofile.WriteObject(h27_w, "jet_pt_soft_total_wide3")


        h28_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h28_w.SetYTitle("Softdrop Mass")
        h28_w.SetXTitle("Jet pT")
        ofile.WriteObject(h28_w, "jet_pt_soft_fail_wide3")



        h29_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h29_w.SetYTitle("Softdrop Mass")
        h29_w.SetXTitle("Jet pT")
        ofile.WriteObject(h29_w, "jet_pt_soft_pass_wide4")



        h30_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h30_w.SetYTitle("Softdrop Mass")
        h30_w.SetXTitle("Jet pT")
        ofile.WriteObject(h30_w, "jet_pt_soft_total_wide4")


        h31_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h31_w.SetYTitle("Softdrop Mass")
        h31_w.SetXTitle("Jet pT")
        ofile.WriteObject(h31_w, "jet_pt_soft_fail_wide4")



	
	ofile.Write()
