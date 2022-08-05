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
	#	Rdf_PreSel = Rdf_noCut.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 > 0) && nPhoton > 0. && nselectedPatJetsAK8PFPuppi > 0. && selectedPatJetsAK8PFPuppi_softdropMass.size()>0")
		nocut += int(Rdf_noCut.Count())
		total_events += float(Rdf_noCut.Count().GetValue())
		total_events_slice += float(Rdf_noCut.Count().GetValue())
		
		Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0")
		ten_pass += float(Rdf_noCut.Count().GetValue())
		ten_pass_slice += float(Rdf_noCut.Count().GetValue())

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
		npcut += int(Rdf_PreSel.Count().GetValue())

		Rdf_PreSel = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")
		njcut += int(Rdf_PreSel.Count().GetValue())

		num_pass += float(Rdf_PreSel.Count().GetValue())
		num_pass_slice += float(Rdf_PreSel.Count().GetValue())


		Rdf_cflow = Rdf_PreSel.Filter("PPT(Photon_pt, nPhoton)")
		ppt_pass += float(Rdf_cflow.Count().GetValue())
		ppt_pass_slice += float(Rdf_cflow.Count().GetValue())
	
		Rdf_cflow = Rdf_cflow.Filter("JPT(selectedPatJetsAK8PFPuppi_pt, nselectedPatJetsAK8PFPuppi)")
		jpt_pass += float(Rdf_cflow.Count().GetValue())
		jpt_pass_slice += float(Rdf_cflow.Count().GetValue())


		Rdf_cflow = Rdf_cflow.Filter("PETA(Photon_pt, Photon_eta, nPhoton)")
		peta_pass += float(Rdf_cflow.Count().GetValue())
		peta_pass_slice += float(Rdf_cflow.Count().GetValue())


		Rdf_cflow = Rdf_cflow.Filter("JETA(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, nselectedPatJetsAK8PFPuppi)")
		jeta_pass += float(Rdf_cflow.Count().GetValue())
		jeta_pass_slice += float(Rdf_cflow.Count().GetValue())


		Rdf_cflow = Rdf_cflow.Filter("PID(Photon_pt, Photon_eta, Photon_cutBased, nPhoton)")
		pid_pass += float(Rdf_cflow.Count().GetValue())
		pid_pass_slice += float(Rdf_cflow.Count().GetValue())


		Rdf_cflow = Rdf_cflow.Filter("JID(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId, nselectedPatJetsAK8PFPuppi)")
		jid_pass += float(Rdf_cflow.Count().GetValue())
		jid_pass_slice += float(Rdf_cflow.Count().GetValue())
	

		Rdf_cflow = Rdf_cflow.Filter("JSOFT(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId,selectedPatJetsAK8PFPuppi_softdropMass, nselectedPatJetsAK8PFPuppi)")
		jsoft_pass += float(Rdf_cflow.Count().GetValue())
		jsoft_pass_slice += float(Rdf_cflow.Count().GetValue())
	       
		if F[2] == 1: 
			Rdf_cflow = Rdf_cflow.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 >0.0)")
		elif F[2] == 2:
			Rdf_cflow = Rdf_cflow.Filter("(HLT_Photon200 >0.0)")

		trig_pass += float(Rdf_cflow.Count().GetValue())
		trig_pass_slice += float(Rdf_cflow.Count().GetValue())
		
		Rdf_cflow = Rdf_cflow.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_softdropMass, selectedPatJetsAK8PFPuppi_jetId)")
		Rdf_cflow = Rdf_cflow.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

		Rdf_cflow = Rdf_cflow.Filter("selectedPatJetsAK8PFPuppi_ak8PFJetsPuppiSoftDropValueMap_nb1AK8PuppiSoftDropN2[jIndex]")
		n2_pass += float(Rdf_cflow.Count().GetValue())
		n2_pass_slice += float(Rdf_cflow.Count().GetValue())

		Rdf_cflow = Rdf_cflow.Define("Rho", "rho(selectedPatJetsAK8PFPuppi_pt[jIndex], selectedPatJetsAK8PFPuppi_softdropMass[jIndex])")
		Rdf_cflow = Rdf_cflow.Filter("Rho > -7 && Rho < -2")
		
		rho_pass += float(Rdf_cflow.Count().GetValue())
		rho_pass_slice += float(Rdf_cflow.Count().GetValue())



	
		#ROOT.gInterpreter.Declare('#include "Help.h"')
		Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_softdropMass, selectedPatJetsAK8PFPuppi_jetId)")
		Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")
#		Rdf_PreSel = Rdf_PreSel.Define("Nsubjet", "nselectedPatJetsAK8PFPuppiSoftDrop_Subjets")

		Rdf = Rdf_PreSel.Filter("pIndex >= 0")
		pcut += int(Rdf.Count())
		
		Rdf = Rdf.Filter("jIndex >= 0")
		jcut += int(Rdf.Count())
		
		#Rdf = Rdf.Filter("Nsubjet >= 2")
		#nsubcut += int(Rdf.Count())

		#Note corrected softdrop mass is being used

		Rdf = Rdf.Define("jM", "selectedPatJetsAK8PFPuppi_softdropMass[jIndex]/(1-selectedPatJetsAK8PFPuppi_rawFactor[jIndex])")
#		Rdf = Rdf.Define("sub_jM", "submass((selectedPatJetsAK8PFPuppiSoftDrop_Subjets_pt[jIndex]), selectedPatJetsAK8PFPuppiSoftDrop_Subjets_eta[jIndex], selectedPatJetsAK8PFPuppiSoftDrop_Subjets_phi[jIndex],selectedPatJetsAK8PFPuppiSoftDrop_Subjets_mass[jIndex], (selectedPatJetsAK8PFPuppiSoftDrop_Subjets_pt[1+jIndex]), selectedPatJetsAK8PFPuppiSoftDrop_Subjets_eta[1+jIndex], selectedPatJetsAK8PFPuppiSoftDrop_Subjets_phi[1+jIndex],selectedPatJetsAK8PFPuppiSoftDrop_Subjets_mass[1+jIndex])")
		Rdf = Rdf.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
		Rdf = Rdf.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
		Rdf = Rdf.Define("jPt", "selectedPatJetsAK8PFPuppi_pt[jIndex]")
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

		trigcut += int(Rdf_Trig.Count().GetValue())

		Rdf_Final = Rdf_Trig.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2")
		dR_pass += float(Rdf_Final.Count().GetValue())
		dR_pass_slice += float(Rdf_Final.Count().GetValue())
		
		
		
		final += int(Rdf_Final.Count().GetValue())

		Rdf_Pass = Rdf_Final.Filter("n2ddt<0")
		pass_events += int(Rdf_Pass.Count().GetValue())
		pass_pass += float(Rdf_Pass.Count().GetValue())
		pass_pass_weight += float(Rdf_Pass.Count().GetValue())*float(F[1])
		pass_pass_slice += float(Rdf_Pass.Count().GetValue())
		pass_pass_weight_slice += float(Rdf_Pass.Count().GetValue())*float(F[1])
#		


		Rdf_Fail = Rdf_Final.Filter("n2ddt>0")
		fail_events += int(Rdf_Fail.Count().GetValue())
		fail_pass += float(Rdf_Fail.Count().GetValue())
		fail_pass_weight += float(Rdf_Fail.Count().GetValue())*float(F[1])
		fail_pass_slice += float(Rdf_Fail.Count().GetValue())
		fail_pass_weight_slice += float(Rdf_Fail.Count().GetValue())*float(F[1])

#		t1 = Rdf.Histo1D(("t1",  ';N^{2}_{1}', 100, 0, 1.0), "N2", "weight")
#		t1 = t1.Clone()
#		t1.SetTitle("N2")
#		t1.SetXTitle("N2")
#		h1.Add(t1)
#
		t2 = Rdf_Final.Histo1D(("t2", "Softdrop Mass", 40, 0, 200), "jM", "weight")
		t2 = t2.Clone()
		t2.SetTitle("Softdrop Mass")
		t2.SetXTitle("Softdrop Mass")
		h2.Add(t2)
#
#
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
		
#		Rdf_sig10_pass = Rdf_Pass.Filter("jM > 5 && jM < 15")
#		pass_sig_pass10 += float(Rdf_sig10_pass.Count().GetValue())
#		pass_sig_pass10_slice += float(Rdf_sig10_pass.Count().GetValue())
#		Rdf_sig25_pass = Rdf_Pass.Filter("jM > 20 && jM < 35")
#		pass_sig_pass25 += float(Rdf_sig25_pass.Count().GetValue())
#		pass_sig_pass25_slice += float(Rdf_sig25_pass.Count().GetValue())
#		Rdf_sig50_pass = Rdf_Pass.Filter("jM > 30 && jM < 60")
#		pass_sig_pass50 += float(Rdf_sig50_pass.Count().GetValue())
#		pass_sig_pass50_slice += float(Rdf_sig50_pass.Count().GetValue())
#		Rdf_sig75_pass = Rdf_Pass.Filter("jM > 70 && jM < 85")
#		pass_sig_pass75 += float(Rdf_sig75_pass.Count().GetValue())
#		pass_sig_pass75_slice += float(Rdf_sig75_pass.Count().GetValue())
#		Rdf_sig100_pass = Rdf_Pass.Filter("jM > 65 && jM < 115")
#		pass_sig_pass100 += float(Rdf_sig100_pass.Count().GetValue())
#		pass_sig_pass100_slice += float(Rdf_sig100_pass.Count().GetValue())
#		Rdf_sig125_pass = Rdf_Pass.Filter("jM > 90 && jM < 140")
#		pass_sig_pass125 += float(Rdf_sig125_pass.Count().GetValue())
#		pass_sig_pass125_slice += float(Rdf_sig125_pass.Count().GetValue())
		
#		s10 = Rdf_sig10_pass.Histo1D(("s10", "Signal 10 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s10 = s10.Clone()
#		sig10.Add(s10)
#		pass_sig_pass_weight10 += float(s10.Integral())
#		pass_sig_pass_weight10_slice += float(s10.Integral())
		
#		s25 = Rdf_sig25_pass.Histo1D(("s25", "Signal 25 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s25 = s25.Clone()
#		sig25.Add(s25)
#		pass_sig_pass_weight25 += float(s25.Integral())
#		pass_sig_pass_weight25_slice += float(s25.Integral())
		
#		s50 = Rdf_sig50_pass.Histo1D(("s50", "Signal 50 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s50 = s50.Clone()
#		sig50.Add(s50)
#		pass_sig_pass_weight50 += float(s50.Integral())
#		pass_sig_pass_weight50_slice += float(s50.Integral())
		
#		s75 = Rdf_sig75_pass.Histo1D(("s75", "Signal 75 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s75 = s75.Clone()
#		sig75.Add(s75)
#		pass_sig_pass_weight75 += float(s75.Integral())
#		pass_sig_pass_weight75_slice += float(s75.Integral())
		
#		s100 = Rdf_sig100_pass.Histo1D(("s100", "Signal 100 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s100 = s100.Clone()
#		sig100.Add(s100)
#		pass_sig_pass_weight100 += float(s100.Integral())
#		pass_sig_pass_weight100_slice += float(s100.Integral())
		
#		s125 = Rdf_sig125_pass.Histo1D(("s125", "Signal 125 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s125 = s125.Clone()
#		sig125.Add(s125)
#		pass_sig_pass_weight125 += float(s125.Integral())
#		pass_sig_pass_weight125_slice += float(s125.Integral())
#		
#		Rdf_sig_thin10_pass = Rdf_Pass.Filter("jM > 5 && jM < 15")
#		pass_sig_thin_pass10 += float(Rdf_sig_thin10_pass.Count().GetValue())
#		pass_sig_thin_pass10_slice += float(Rdf_sig_thin10_pass.Count().GetValue())
#		Rdf_sig_thin25_pass = Rdf_Pass.Filter("jM > 15 && jM < 30 && jPt > 100 && jPt < 300")
#		pass_sig_thin_pass25 += float(Rdf_sig_thin25_pass.Count().GetValue())
#		pass_sig_thin_pass25_slice += float(Rdf_sig_thin25_pass.Count().GetValue())
#		Rdf_sig_thin50_pass = Rdf_Pass.Filter("jM > 30 && jM < 60")
#		pass_sig_thin_pass50 += float(Rdf_sig_thin50_pass.Count().GetValue())
#		pass_sig_thin_pass50_slice += float(Rdf_sig_thin50_pass.Count().GetValue())
#		Rdf_sig_thin75_pass = Rdf_Pass.Filter("jM > 65 && jM < 80 && jPt > 150 && jPt < 350")
#		pass_sig_thin_pass75 += float(Rdf_sig_thin75_pass.Count().GetValue())
#		pass_sig_thin_pass75_slice += float(Rdf_sig_thin75_pass.Count().GetValue())
#		Rdf_sig_thin100_pass = Rdf_Pass.Filter("jM > 65 && jM < 115")
#		pass_sig_thin_pass100 += float(Rdf_sig_thin100_pass.Count().GetValue())
#		pass_sig_thin_pass100_slice += float(Rdf_sig_thin100_pass.Count().GetValue())
#		Rdf_sig_thin125_pass = Rdf_Pass.Filter("jM > 90 && jM < 140")
#		pass_sig_thin_pass125 += float(Rdf_sig_thin125_pass.Count().GetValue())
#		pass_sig_thin_pass125_slice += float(Rdf_sig_thin125_pass.Count().GetValue())
		
#		s_thin10 = Rdf_sig_thin10_pass.Histo1D(("s10", "Signal 10 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin10 = s_thin10.Clone()
#		sig_thin10.Add(s_thin10)
#		pass_sig_thin_pass_weight10 += float(s_thin10.Integral())
#		pass_sig_thin_pass_weight10_slice += float(s_thin10.Integral())
		
#		s_thin25 = Rdf_sig_thin25_pass.Histo1D(("s25", "Signal 25 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin25 = s_thin25.Clone()
#		sig_thin25.Add(s_thin25)
#		pass_sig_thin_pass_weight25 += float(s_thin25.Integral())
#		pass_sig_thin_pass_weight25_slice += float(s_thin25.Integral())
#		
#		s_thin50 = Rdf_sig_thin50_pass.Histo1D(("s50", "Signal 50 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin50 = s_thin50.Clone()
#		sig_thin50.Add(s_thin50)
#		pass_sig_thin_pass_weight50 += float(s_thin50.Integral())
#		pass_sig_thin_pass_weight50_slice += float(s_thin50.Integral())
 #       	
#		s_thin75 = Rdf_sig_thin75_pass.Histo1D(("s75", "Signal 75 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin75 = s_thin75.Clone()
#		sig_thin75.Add(s_thin75)
#		pass_sig_thin_pass_weight75 += float(s_thin75.Integral())
#		pass_sig_thin_pass_weight75_slice += float(s_thin75.Integral())
#		
#		s_thin100 = Rdf_sig_thin100_pass.Histo1D(("s100", "Signal 100 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin100 = s_thin100.Clone()
#		sig_thin100.Add(s_thin100)
#		pass_sig_thin_pass_weight100 += float(s_thin100.Integral())
#		pass_sig_thin_pass_weight100_slice += float(s_thin100.Integral())
#		
#		s_thin125 = Rdf_sig_thin125_pass.Histo1D(("s125", "Signal 125 Softdrop Mass Sig Region", 40, 0, 200), "jM", "weight")
 #       	s_thin125 = s_thin125.Clone()
#		sig_thin125.Add(s_thin125)
#		pass_sig_thin_pass_weight125 += float(s_thin125.Integral())
#		pass_sig_thin_pass_weight125_slice += float(s_thin125.Integral())
#		
#		
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

		#Individual slice cutflow
		print("Cutflow Percentages For Slice "+str(slicenum)+": ")
		print("10% of events passed: "+str(ten_pass_slice/total_events_slice * 100)+"%")
		print("Num Pho and Num Jet passed: "+str(num_pass_slice/total_events_slice * 100)+"%")
		print("Photon pT passed: "+str(ppt_pass_slice/total_events_slice * 100)+"%")
		print("Jet pT passed: "+str(jpt_pass_slice/total_events_slice * 100)+"%")
		print("Photon Eta passed: "+str(peta_pass_slice/total_events_slice * 100)+"%")
		print("Jet Eta passed: "+str(jeta_pass_slice/total_events_slice * 100)+"%")
		print("Cut Based ID passed: "+str(pid_pass_slice/total_events_slice * 100)+"%")
		print("Jet ID passed: "+str(jid_pass_slice/total_events_slice * 100)+"%")
		print("Softdrop passed: "+str(jsoft_pass_slice/total_events_slice * 100)+"%")
		print("Trigger passed: "+str(trig_pass_slice/total_events_slice * 100)+"%")
		print("N2 passed: "+str(n2_pass_slice/total_events_slice * 100)+"%")
		print("Rho passed: "+str(rho_pass_slice/total_events_slice * 100)+"%")
		print("DeltaR passed: "+str(dR_pass_slice/total_events_slice * 100)+"%")
		print("Passing Events: "+str(pass_pass_slice/total_events_slice * 100)+"%")
		print("Failing Events: "+str(fail_pass_slice/total_events_slice * 100)+"%")
	
		print("Passing Fraction: "+str(pass_pass_weight_slice/(pass_pass_weight_slice+fail_pass_weight_slice)))

#		print("Passing Signal Region Events (10GeV): "+str(pass_sig_pass10_slice))
 #       	print("Passing Signal Region Events (25GeV): "+str(pass_sig_pass25_slice))
  #      	print("Passing Signal Region Events (50GeV): "+str(pass_sig_pass50_slice))
   #     	print("Passing Signal Region Events (75GeV): "+str(pass_sig_pass75_slice))
    #    	print("Passing Signal Region Events (100GeV): "+str(pass_sig_pass100_slice))
     #   	print("Passing Signal Region Events (125GeV): "+str(pass_sig_pass125_slice))
      #  	print("Weighted Passing Signal Region Events (10GeV) (Number): "+str(pass_sig_pass_weight10_slice))
#		print("Weighted Passing Signal Region Events (25GeV) (Number): "+str(pass_sig_pass_weight25_slice))
 #       	print("Weighted Passing Signal Region Events (50GeV) (Number): "+str(pass_sig_pass_weight50_slice))
  #      	print("Weighted Passing Signal Region Events (75GeV) (Number): "+str(pass_sig_pass_weight75_slice))
   #     	print("Weighted Passing Signal Region Events (100GeV) (Number): "+str(pass_sig_pass_weight100_slice))
    #    	print("Weighted Passing Signal Region Events (125GeV) (Number): "+str(pass_sig_pass_weight125_slice))
				
#		print("Passing Thin Signal Region Events (10GeV): "+str(pass_sig_thin_pass10_slice))
 #       	print("Passing Thin Signal Region Events (25GeV): "+str(pass_sig_thin_pass25_slice))
  #      	print("Passing Thin Signal Region Events (50GeV): "+str(pass_sig_thin_pass50_slice))
   #     	print("Passing Thin Signal Region Events (75GeV): "+str(pass_sig_thin_pass75_slice))
    #    	print("Passing Thin Signal Region Events (100GeV): "+str(pass_sig_thin_pass100_slice))
     #   	print("Passing Thin Signal Region Events (125GeV): "+str(pass_sig_thin_pass125_slice))
      #  	print("Weighted Passing Thin Signal Region Events (10GeV) (Number): "+str(pass_sig_thin_pass_weight10_slice))
       # 	print("Weighted Passing Thin Signal Region Events (25GeV) (Number): "+str(pass_sig_thin_pass_weight25_slice))
	#	print("Weighted Passing Thin Signal Region Events (50GeV) (Number): "+str(pass_sig_thin_pass_weight50_slice))
	#	print("Weighted Passing Thin Signal Region Events (75GeV) (Number): "+str(pass_sig_thin_pass_weight75_slice))
	#	print("Weighted Passing Thin Signal Region Events (100GeV) (Number): "+str(pass_sig_thin_pass_weight100_slice))
	#	print("Weighted Passing Thin Signal Region Events (125GeV) (Number): "+str(pass_sig_thin_pass_weight125_slice))
			
		
	print(str(nocut)+" Events Before Cuts in "+fname+" Sample")		
	print(str(npcut)+" Events After nPho>0 in in "+fname+" Sample")		
	print(str(njcut)+" Events After nselectedPatJetsAK8PFPuppi>0 in "+fname+" Sample")		
#	print(str(nsubcut)+" Events After nselectedsubjet >= 2 in "+fname+" Sample")		
	print(str(pcut)+" Events After Photon Cuts in "+fname+" Sample")		
	print(str(jcut)+" Events After Jet Cuts in "+fname+" Sample")		
	print(str(trigcut)+" Events After Trigger Cuts in "+fname+" Sample")		
	print(str(final)+" Events After Final Cuts in "+fname+" Sample")		
	print(str(pass_events)+" Passing Events in "+fname+" Sample")		
	print(str(fail_events)+" Failing Events in "+fname+" Sample")		
	

 	print("Total Number of Events: "+str(total_events))

	print("Cutflow Percentages: ")
	print("10% cut applied passed: "+str(ten_pass/total_events * 100)+"%")
	print("Num Pho and Num Jet passed: "+str(num_pass/total_events * 100)+"%")
	print("Photon pT passed: "+str(ppt_pass/total_events * 100)+"%")
	print("Jet pT passed: "+str(jpt_pass/total_events * 100)+"%")
	print("Photon Eta passed: "+str(peta_pass/total_events * 100)+"%")
	print("Jet Eta passed: "+str(jeta_pass/total_events * 100)+"%")
	print("Cut Based ID passed: "+str(pid_pass/total_events * 100)+"%")
	print("Jet ID passed: "+str(jid_pass/total_events * 100)+"%")
	print("Softdrop passed: "+str(jsoft_pass/total_events * 100)+"%")
	print("Trigger passed: "+str(trig_pass/total_events * 100)+"%")
	print("N2 passed: "+str(n2_pass/total_events * 100)+"%")
	print("Rho passed: "+str(rho_pass/total_events * 100)+"%")
	print("DeltaR passed: "+str(dR_pass/total_events * 100)+"%")
	print("Passing Events: "+str(pass_pass/total_events * 100)+"%")
	print("Failing Events: "+str(fail_pass/total_events * 100)+"%")
	
	print("Passing Fraction: "+str(pass_pass_weight/(pass_pass_weight+fail_pass_weight)))

 #       print("Passing Signal Region Events (10GeV): "+str(pass_sig_pass10))
#	print("Passing Signal Region Events (25GeV): "+str(pass_sig_pass25))
 #       print("Passing Signal Region Events (50GeV): "+str(pass_sig_pass50))
  #      print("Passing Signal Region Events (75GeV): "+str(pass_sig_pass75))
   #     print("Passing Signal Region Events (100GeV): "+str(pass_sig_pass100))
    #    print("Passing Signal Region Events (125GeV): "+str(pass_sig_pass125))
     #   print("Weighted Passing Signal Region Events (10GeV) (Number): "+str(pass_sig_pass_weight10))
      #  print("Weighted Passing Signal Region Events (25GeV) (Number): "+str(pass_sig_pass_weight25))
       # print("Weighted Passing Signal Region Events (50GeV) (Number): "+str(pass_sig_pass_weight50))
#	print("Weighted Passing Signal Region Events (75GeV) (Number): "+str(pass_sig_pass_weight75))
 #       print("Weighted Passing Signal Region Events (100GeV) (Number): "+str(pass_sig_pass_weight100))
  #      print("Weighted Passing Signal Region Events (125GeV) (Number): "+str(pass_sig_pass_weight125))
#
#	print("Passing Thin Signal Region Events (10GeV): "+str(pass_sig_thin_pass10))
 #       print("Passing Thin Signal Region Events (25GeV): "+str(pass_sig_thin_pass25))
  #      print("Passing Thin Signal Region Events (50GeV): "+str(pass_sig_thin_pass50))
   #     print("Passing Thin Signal Region Events (75GeV): "+str(pass_sig_thin_pass75))
    #    print("Passing Thin Signal Region Events (100GeV): "+str(pass_sig_thin_pass100))
     #   print("Passing Thin Signal Region Events (125GeV): "+str(pass_sig_thin_pass125))
      #  print("Weighted Passing Thin Signal Region Events (10GeV) (Number): "+str(pass_sig_thin_pass_weight10))
       # print("Weighted Passing Thin Signal Region Events (25GeV) (Number): "+str(pass_sig_thin_pass_weight25))
#	print("Weighted Passing Thin Signal Region Events (50GeV) (Number): "+str(pass_sig_thin_pass_weight50))
 #       print("Weighted Passing Thin Signal Region Events (75GeV) (Number): "+str(pass_sig_thin_pass_weight75))
  #      print("Weighted Passing Thin Signal Region Events (100GeV) (Number): "+str(pass_sig_thin_pass_weight100))
   #     print("Weighted Passing Thin Signal Region Events (125GeV) (Number): "+str(pass_sig_thin_pass_weight125))


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
	
#	ofile.WriteObject(sig10, "sig10")
#	ofile.WriteObject(sig25, "sig25")
#	ofile.WriteObject(sig50, "sig50")
#	ofile.WriteObject(sig75, "sig75")
#	ofile.WriteObject(sig100, "sig100")
#	ofile.WriteObject(sig125, "sig125")
#	
#	ofile.WriteObject(sig_thin10, "sig_thin10")
#	ofile.WriteObject(sig_thin25, "sig_thin25")
#	ofile.WriteObject(sig_thin50, "sig_thin50")
#	ofile.WriteObject(sig_thin75, "sig_thin75")
#	ofile.WriteObject(sig_thin100, "sig_thin100")
#	ofile.WriteObject(sig_thin125, "sig_thin125")

	p1.SetXTitle("Softdrop Mass")

	pc1 = TCanvas()
	pc1.cd()
	p1.Draw("hist")
	pc1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_soft.png")
	pc1.Close()
	
	
	h7_1.SetTitle("Rho")
	h7_1.SetXTitle("Rho")
	ofile.WriteObject(h7_1, "fine_rho")

	n0 = TCanvas()
	n0.cd()
	n0.SetLogy()
	h7_1.Draw("hist")
	n0.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_finerho.png")
	n0.Close()
	
	h2.SetTitle("Softdrop Mass")
	h2.SetXTitle("Softdrop Mass")

	n1 = TCanvas()
	n1.cd()
#	n1.SetLogy()
	h2.Draw("hist")
	n1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_softdrop.png")
	n1.Close()
	
	h4.SetTitle("Photon pT")
	h4.SetXTitle("pT")

	n4 = TCanvas()
	n4.cd()
	h4.Draw("hist")
	n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pho_pt.png")
	n4.Close()
	
	h5.SetTitle("Jet pT")
	h5.SetXTitle("pT")

	n5 = TCanvas()
	n5.cd()
	h5.Draw("hist")
	n5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt.png")
	n5.Close()

	h5_1.SetTitle("Thin Jet pT")
	h5_1.SetXTitle("Jet pT")

        m3_1 = TCanvas()
        m3_1.cd()
#        m3_1.SetLogy()
        h5_1.Draw("hist")
        m3_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_thin.png")
        m3_1.Close()

	
	h6.SetTitle("Jet Eta")
	h6.SetXTitle("Eta")

	n6 = TCanvas()
	n6.cd()
	h6.Draw("hist")
	n6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_eta.png")
	n6.Close()
	
	h8.SetTitle("Photon Eta")
	h8.SetXTitle("Eta")

	n8 = TCanvas()
	n8.cd()
	h8.Draw("hist")
	n8.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pho_eta.png")
	n8.Close()

	
	h11.SetTitle("N2 vs. N2DDT")
	h11.SetXTitle("N2")
	h11.SetYTitle("N2DDT")
	ofile.WriteObject(h11, "n2_n2ddt")
	
	n1 = TCanvas()
	n1.cd()
	h11.Draw("COLZ")
	n1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2_n2ddt.png")
	n1.Close()

	
	h12.SetTitle("N2")
	h12.SetXTitle("N2")
	ofile.WriteObject(h12, "N2")
	
	n2 = TCanvas()
	n2.cd()
	h12.Draw()
	n2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_N2.png")
	n2.Close()

	
	h13.SetTitle("N2DDT")
	h13.SetXTitle("N2DDT")
	ofile.WriteObject(h13, "N2DDT")

	n3 = TCanvas()
	n3.cd()
	h13.Draw()
	n3.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_N2DDT.png")
	n3.Close()
	
	
	h14.SetTitle("N2 vs. Softdrop Mass")
	h14.SetXTitle("N2")
	h14.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h14, "n2_soft")

	n4 = TCanvas()
	n4.cd()
	h14.Draw("COLZ")
	n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2_soft.png")
	n4.Close()

	
	h15.SetTitle("N2DDT vs. Softdrop Mass")
	h15.SetXTitle("N2DDT")
	h15.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h15, "n2ddt_soft")

	n5 = TCanvas()
	n5.cd()
	h15.Draw("COLZ")
	n5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2ddt_soft.png")
	n5.Close()
	
	h15_1.SetTitle("Softdrop Mass vs. N2DDT")
	h15_1.SetYTitle("N2DDT")
	h15_1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h15_1, "soft_n2ddt")

	n5_1 = TCanvas()
	n5_1.cd()
	h15_1.Draw("COLZ")
	n5_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_soft_n2ddt.png")
	n5_1.Close()

	h16.SetTitle("Rho vs. Softdrop Mass")
	h16.SetXTitle("Rho")
	h16.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h16, "rho_soft")

	n6 = TCanvas()
	n6.cd()
	h16.Draw("COLZ")
	n6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_rho_soft.png")
	n6.Close()


	h19.SetTitle("N2 vs. Jet pT")
	h19.SetXTitle("N2")
	h19.SetYTitle("Jet pT")
	ofile.WriteObject(h19, "n2_jet_pt")

	n9 = TCanvas()
	n9.cd()
	h19.Draw("COLZ")
	n9.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2_jet_pt.png")
	n9.Close()

	h20.SetTitle("N2DDT vs. Jet pT")
	h20.SetXTitle("N2DDT")
	h20.SetYTitle("Jet pT")
	ofile.WriteObject(h20, "n2ddt_jet_pt")

	n10 = TCanvas()
	n10.cd()
	h20.Draw("COLZ")
	n10.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2ddt_jet_pt.png")
	n10.Close()
	
	h20_1.SetTitle("Jet pT vs. N2DDT")
	h20_1.SetYTitle("N2DDT")
	h20_1.SetXTitle("Jet pT")
	ofile.WriteObject(h20_1, "jet_pt_n2ddt")

	n10_1 = TCanvas()
	n10_1.cd()
	h20_1.Draw("COLZ")
	n10_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_n2ddt.png")
	n10_1.Close()

        h21.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h21.SetYTitle("Softdrop Mass")
        h21.SetXTitle("Jet pT")
        ofile.WriteObject(h21, "jet_pt_soft_pass")

        n11 = TCanvas()
        n11.cd()
        h21.Draw("COLZ")
        n11.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_pass.png")
        n11.Close()

        h21_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h21_w.SetYTitle("Softdrop Mass")
        h21_w.SetXTitle("Jet pT")
        ofile.WriteObject(h21_w, "jet_pt_soft_pass_wide")

        n11_w = TCanvas()
        n11_w.cd()
        h21_w.Draw("COLZ")
        n11_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_pass_wide.png")
        n11_w.Close()

        h21_1.SetTitle("Total Jet pT vs. Softdrop Mass")
        h21_1.SetYTitle("Softdrop Mass")
        h21_1.SetXTitle("Jet pT")
        ofile.WriteObject(h21_1, "jet_pt_soft_total")

        n11_1 = TCanvas()
        n11_1.cd()
        h21_1.Draw("COLZ")
        n11_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_total.png")
        n11_1.Close()

        h21_1_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h21_1_w.SetYTitle("Softdrop Mass")
        h21_1_w.SetXTitle("Jet pT")
        ofile.WriteObject(h21_1_w, "jet_pt_soft_total_wide")

        n11_1_w = TCanvas()
        n11_1_w.cd()
        h21_1_w.Draw("COLZ")
        n11_1_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_total_wide.png")
        n11_1_w.Close()

        h22.SetTitle("Passing Jet pT vs. Softdrop Mass (Coarse)")
        h22.SetYTitle("Softdrop Mass")
        h22.SetXTitle("Jet pT")
        ofile.WriteObject(h22, "jet_pt_soft2")

        n12 = TCanvas()
        n12.cd()
        h22.Draw("COLZ")
        n12.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft2.png")
        n12.Close()

        h23.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h23.SetYTitle("Softdrop Mass")
        h23.SetXTitle("Jet pT")
        ofile.WriteObject(h23, "jet_pt_soft_fail")

        n13 = TCanvas()
        n13.cd()
        h23.Draw("COLZ")
        n13.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_fail.png")
        n13.Close()

        h23_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h23_w.SetYTitle("Softdrop Mass")
        h23_w.SetXTitle("Jet pT")
        ofile.WriteObject(h23_w, "jet_pt_soft_fail_wide")

        n13_w = TCanvas()
        n13_w.cd()
        h23_w.Draw("COLZ")
        n13_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_fail_wide.png")
        n13_w.Close()



	n12 = TCanvas()
	n12.cd()
	h22.Draw("COLZ")
	n12.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft2.png")
	n12.Close()

	h24.SetTitle("Passing Jet pT vs. Rho")
	h24.SetYTitle("Rho")
	h24.SetXTitle("Jet pT")
	ofile.WriteObject(h24, "jet_pt_rho_pass")

	n14 = TCanvas()
	n14.cd()
	h24.Draw("COLZ")
	n14.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_rho_pass.png")
	n14.Close()

	h25.SetTitle("Passing Jet pT vs. Rho")
	h25.SetYTitle("Rho")
	h25.SetXTitle("Jet pT")
	ofile.WriteObject(h25, "jet_pt_rho_fail")

	n15 = TCanvas()
	n15.cd()
	h25.Draw("COLZ")
	n15.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_rho_fail.png")
	n15.Close()

	
	
	ofile.Write()
