#
import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os
from array import array
import math
import numpy as np


#This version of W-peak analysis does NOT have truth matching

#determines cutoff bin for value of rho or pt for N2DDT plotting
def bin_num(self, val, i):
	if i == 1:      #Rho Value
		#if val>-2 or val<-7:
		#       print("bin_num error, val: ", val)
		return int(((val+8.0)*2.0)+1)
	elif i == 2:     #Pt Value
		#if val>2000 or val<100:
		#       print("bin_num error, val: ", val)
		return int(((val)/50.0)+1)

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

	ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/Wpeak/output/RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()


	rho_bins = cut_hist.GetNbinsX()
	pt_bins = cut_hist.GetNbinsY()

		

	h1 = TH1F("h1", "N2", 50, 0, 0.5)
	h2 = TH1F("h2", "Softdrop Mass", 40, 0, 200)
	h2_1 = TH1F("h2_1", "Thin Softdrop Mass", 100, 0, 200)
	h2_2 = TH1F("h2_2", "Thin (Uncorrected) Softdrop Mass", 100, 0, 200)
#	h4 = TH1F("h4", "Photon pT", 100, 0, 2000)
	h5 = TH1F("h5", "Jet pT", 40, 0, 2000)
        h5_1 = TH1F("h5_1", "Thin Jet pT", 2000, 0, 2000)
	h6 = TH1F("h6", "Jet Eta", 70, -3.5, 3.5)
	h7 = TH1F("h7", "Rho", 28, -8, -1)
#	h8 = TH1F("h8", "Photon Eta", 70, -3.5, 3.5)
	h9 = TH1F("h9", "N2DDT", 100, -.5, .5)
	
#	h1_presel = TH1F("h1_presel", "PreSel N2", 50, 0, 0.5)
#	h2_presel = TH1F("h2_presel", "PreSel Softdrop Mass", 40, 0, 200)
#	h4_presel = TH1F("h4_presel", "PreSel Photon pT", 100, 0, 2000)
#	h5_presel = TH1F("h5_presel", "PreSel Jet pT", 40, 0, 2000)
 #       h5_1_presel = TH1F("h5_1_presel", "PreSel Thin Jet pT", 2000, 0, 2000)
#	h6_presel = TH1F("h6_presel", "PreSel Jet Eta", 70, -3.5, 3.5)
#	h7_presel = TH1F("h7_presel", "PreSel Rho", 28, -8, -1)
#	h8_presel = TH1F("h8_presel", "PreSel Photon Eta", 70, -3.5, 3.5)

	h11 = TH2F("n2_n2ddt", "N2 vs. N2DDT", 50, 0, 0.5, 100, -.5, .5)
	h14 = TH2F("n2_soft", "N2 vs. Softdrop Mass", 100, 0, 1, 40, 0, 200)
	h14_1 = TH2F("soft_n2", "Softdrop Mass vs. N2", 40, 0, 200, 100, 0, 1)
	h15 = TH2F("n2ddt_soft", "N2DDT vs. Softdrop Mass", 100, -.5, .5, 40, 0, 200)
	h15_1 = TH2F("soft_n2ddt", "Softdrop Mass vs. N2DDT", 40, 0, 200, 100, -.5, .5)
	
	h16 = TH2F("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h17 = TH2F("rho_soft_pass", "Passing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h18 = TH2F("rho_soft_fail", "Failing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h19 = TH2F("n2_pt", "N2 vs. Jet pT", 100, 0, 1, 400, 0, 2000)
	h19_1 = TH2F("pt_n2", "Jet pT vs. N2", 400, 0, 2000, 100, 0, 1)
	h20 = TH2F("n2ddt_pt", "N2DDT vs. Jet pT", 100, -.5, .5, 400, 0, 2000)
	h20_1 = TH2F("pt_n2ddt", "Jet pT vs. N2DDT", 400, 0, 2000, 100, -.5, .5)

 	h21 = TH2F("jet_pt_soft_pass", "Passing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)
        h21_1 = TH2F("jet_pt_soft_total", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)
        h23 = TH2F("jet_pt_soft_fail", "Failing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)


	h24 = TH2F("jet_pt_rho_pass", "Passing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1)
	h25 = TH2F("jet_pt_rho_fail", "Failing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1)


        h50 = TH1F("ak4_eta", "AK4 Jet Eta", 70, -3.5, 3.5)
        h51 = TH1F("ak4_phi", "AK4 Jet Phi", 80, -4, 4)
        h52 = TH1F("ak4_njet", "AK4 nJet", 25, 0, 25)
        h53 = TH1F("ak4_btag", "AK4 BTag", 100, 0, 1)

        h56 = TH1F("PuppiMETPT", "PuppiMET pT", 500, 0, 500)
        h57 = TH1F("METplusMUON", "PuppiMET pT + Muon pT", 700, 0, 700)


#	h65 = TH2F("eta_pho_pt", "Eta vs. Photon pT", 70, -3.5, 3.5, 100, 0, 2000)
	
	h80 = TH1F("HT", "AK4 HT", 1000, 0, 5000)
	h81 = TH1F("HT_AK8", "AK8 HT", 1000, 0, 5000)
	
	h90 = TH1F("h90", "AK4 Jet pT", 200, 0, 2000)
	
	h91 = TH1F("h91", "Muon pT", 100, 0, 1000)
        h91_1 = TH1F("h91_1", "Thin Muon pT", 1000, 0, 1000)
	h92 = TH1F("h92", "Muon Eta", 70, -3.5, 3.5)

	p1 = TH1F("p1", "passing softdrop mass", 40, 0, 200)
        p1_1 = TH1F("p1_1", "thin passing softdrop mass", 100, 0, 200)
        p1_2 = TH1F("p1_2", "thin (uncorrected) passing softdrop mass", 100, 0, 200)
	p2 = TH1F("p2", "passing photon pt", 100, 0, 2000)
	p3 = TH1F("p3", "passing jet pt", 40, 0, 2000)
	p4 = TH1F("p4", "passing rho", 28, -8, -1)
	p5 = TH1F("p5", "passing photon eta", 70, -3.5, 3.5)
	p6 = TH1F("p6", "passing jet eta", 70, -3.5, 3.5)

	f1 = TH1F("f1", "failing softdrop mass", 40, 0, 200)
        f1_1 = TH1F("f1_1", "failing softdrop mass", 100, 0, 200)
        f1_2 = TH1F("f1_2", "failing (uncorrected) softdrop mass", 100, 0, 200)
	f2 = TH1F("f2", "failing photon pt", 100, 0, 2000)
	f3 = TH1F("f3", "failing jet pt", 40, 0, 2000)
	f4 = TH1F("f4", "failing rho", 28, -8, -1)
	f5 = TH1F("f5", "failing photon eta", 70, -3.5, 3.5)
	f6 = TH1F("f6", "failing jet eta", 70, -3.5, 3.5)

	nocut = 0
	npcut = 0
	njcut = 0
	pcut = 0
	jcut = 0
	mucut = 0
	nsubcut = 0

	trigcut = 0

	final = 0

	pass_events = 0
	fail_events = 0

	total_events = 0
	num_pass = 0
	ppt_pass = 0
	dir_prompt_pass = 0
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



	Chain = ROOT.TChain("Events")
	print(sample[0])
	
	Chain.Add(sample[0])

#		for path, subdirs, files in os.walk(F[0]):
#			for name in files:
#				File = os.path.join(path, name)
#				if (File.endswith(".root")):
#					print os.path.join(path, name) 
#					#n = RDF(File).Count()
					#print n.GetValue()
#					Chain.Add(File)
	
	Rdf_noCut = RDF(Chain)
	nocut += float(Rdf_noCut.Count().GetValue())
	total_events += float(Rdf_noCut.Count().GetValue())

	
	
#	if sample[3] == "data": #Take 10% of Data
#                Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0")
#                ten_pass += float(Rdf_noCut.Count().GetValue())
	#Rdf_noCut = Rdf_noCut.Filter("(HLT_Photon200 >0.0)")
	Rdf_noCut = Rdf_noCut.Filter("(HLT_Mu50 >0.0)")

	trig_pass += float(Rdf_noCut.Count().GetValue())

	Rdf_PreSel = Rdf_noCut.Filter("nFatJet > 0. && nMuon > 0.")
	njcut += float(Rdf_PreSel.Count().GetValue())
	num_pass += float(Rdf_PreSel.Count().GetValue())


	
	
	#ROOT.gInterpreter.Declare('#include "Help.h"')
	
	#Direct Prompt Filter
	if sample[3] == "GJ":
		Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	if sample[3] == "QCD":
		Rdf_PreSel = Rdf_PreSel.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	#Trigger Filter
	#Rdf_PreSel = Rdf_PreSel.Filter("(HLT_Photon200 >0.0)")
	Rdf = Rdf_PreSel.Filter("(HLT_Mu50 >0.0)")

	trigcut += float(Rdf.Count().GetValue())
	
		
	
	#New Muon Stuff Added
	Rdf = Rdf.Define("mIndex", "muon_index_define(nMuon, Muon_eta, Muon_tightId)")
	Rdf = Rdf.Filter("mIndex >= 0")
	
	Rdf = Rdf.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
	Rdf = Rdf.Filter("jIndex >= 0")

	Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]")
	Rdf = Rdf.Define("jEta", "FatJet_eta[jIndex]")
	Rdf = Rdf.Define("jPhi", "FatJet_phi[jIndex]")
	Rdf = Rdf.Define("jPt", "FatJet_pt_nom[jIndex]")
#	Rdf = Rdf.Define("pPt", "Photon_pt[0]")
#	Rdf = Rdf.Define("pEta", "Photon_eta[0]")
#	Rdf = Rdf.Define("pPhi", "Photon_phi[0]")
	Rdf = Rdf.Define("mPt", "Muon_pt[mIndex]")
	Rdf = Rdf.Define("mEta", "Muon_eta[mIndex]")
	Rdf = Rdf.Define("mPhi", "Muon_phi[mIndex]")
	Rdf = Rdf.Define("mID", "Muon_tightId[mIndex]")
	Rdf = Rdf.Define("N2", "FatJet_n2b1[0]")
	Rdf = Rdf.Define("jID", "FatJet_jetId[0]")
	Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
	Rdf = Rdf.Define("n2ddt", "ddt(jPt, jM, N2)")

	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")

#	Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
        Rdf = Rdf.Define("pCut", "Photon_cutBased[0]")

        Rdf = Rdf.Define("nj4", "nJet")
        Rdf = Rdf.Define("ak4_muon", "ak4_match_muon(nj4, Jet_eta, Jet_phi, mEta, mPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that are separated from Muon candidate by at least dR > 0.3

        Rdf = Rdf.Define("j4eta", "ak4_ret(ak4_muon, Jet_eta)[0]")
        Rdf = Rdf.Define("j4phi", "ak4_ret(ak4_muon, Jet_phi)[0]")
        Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_muon, Jet_btagDeepFlavB)[0]")

        Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")
        
	Rdf = Rdf.Define("MET_mPt", "PuppiMETpt + mPt") #Define here leptonic energy
        
	Rdf = Rdf.Define("jHT", "HT(Jet_pt, Jet_eta)")
	Rdf = Rdf.Define("jHT_AK8", "HT_AK8(FatJet_pt_nom, FatJet_eta)")
	
	Rdf = Rdf.Define("jPt_AK4", "Jet_pt[0]")
        
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
                Rdf = Rdf.Define("xs_lumi", sample[1])
                Rdf = Rdf.Define("weight", "xs_lumi*puWeight")
        elif sample[3] == "data":
                Rdf = Rdf.Define("weight", sample[1])
		

	


#        Rdf_Final = Rdf_Final.Filter("PuppiMETpt < 75 && jBtag < 0.0532")
	#Muon Cut on min missing ET and medium b-tag WP
	#Requre min AK8 jet pT
        Rdf_Final = Rdf.Filter("PuppiMETpt > 40 && MET_mPt > 220 && jBtag > 0.3040 && Rho < -2 && Rho > -7")

        final += float(Rdf_Final.Count().GetValue())
#	print(final)	


	Rdf_Pass = Rdf_Final.Filter("n2ddt<0")
	pass_events += float(Rdf_Pass.Count().GetValue())
	pass_pass += float(Rdf_Pass.Count().GetValue())
	pass_pass_weight += float(Rdf_Pass.Count().GetValue())*float(sample[1])


	Rdf_Fail = Rdf_Final.Filter("n2ddt>0")
	fail_events += float(Rdf_Fail.Count().GetValue())
	fail_pass += float(Rdf_Fail.Count().GetValue())
	fail_pass_weight += float(Rdf_Fail.Count().GetValue())*float(sample[1])

	t1 = Rdf_Final.Histo1D(("t1",  ';N^{2}_{1}', 50, 0, 0.5), "N2", "weight")
	t1 = t1.Clone()
	t1.SetTitle("N2")
	t1.SetXTitle("N2")
	h1.Add(t1)

	t2 = Rdf_Final.Histo1D(("t2", "Softdrop Mass", 40, 0, 200), "jM", "weight")
	t2 = t2.Clone()
	t2.SetTitle("Softdrop Mass")
	t2.SetXTitle("Softdrop Mass")
	h2.Add(t2)
	
	t2_1 = Rdf_Final.Histo1D(("t2_1", "Thin Softdrop Mass", 100, 0, 200), "jM", "weight")
	t2_1 = t2_1.Clone()
	t2_1.SetTitle("Thin Softdrop Mass")
	t2_1.SetXTitle("Softdrop Mass")
	h2_1.Add(t2_1)
	
	t2_2 = Rdf_Final.Histo1D(("t2_2", "Thin (Uncorrected) Softdrop Mass", 100, 0, 200), "jM_uncorr", "weight")
	t2_2 = t2_2.Clone()
	t2_2.SetTitle("Thin (Uncorrected) Softdrop Mass")
	t2_2.SetXTitle("Softdrop Mass")
	h2_2.Add(t2_2)


#	t4 = Rdf_Final.Histo1D(("t4", "Photon pT", 100, 0, 2000), "pPt", "weight")
#	t4 = t4.Clone()
#	t4.SetTitle("Photon pT")
#	t4.SetXTitle("pT")
#	h4.Add(t4)
		
	t5 = Rdf_Final.Histo1D(("t5", "Jet pT", 40, 0, 2000), "jPt", "weight")
	t5 = t5.Clone()
	t5.SetTitle("Jet pT")
	t5.SetXTitle("pT")
	h5.Add(t5)

        t5_1 = Rdf_Final.Histo1D(("t5_1", "Thin Jet pT", 2000, 0, 2000), "jPt", "weight")
        t5_1 = t5_1.Clone()
        t5_1.SetTitle("Thin Jet pT")
        t5_1.SetXTitle("pT")
        h5_1.Add(t5_1)

	t6 = Rdf_Final.Histo1D(("t6", "Jet Eta", 70, -3.5, 3.5), "jEta", "weight")
	t6 = t6.Clone()
	t6.SetTitle("Jet Eta")
	t6.SetXTitle("Eta")
	h6.Add(t6)


	t7 = Rdf_Final.Histo1D(("t7", "Rho", 28, -8, -1), "Rho", "weight")
	t7 = t7.Clone()
	t7.SetTitle("Rho")
	t7.SetXTitle("Rho")
	h7.Add(t7)

#	t8 = Rdf_Final.Histo1D(("t8", "Photon Eta", 70, -3.5, -3.5), "pEta", "weight")
#	t8 = t8.Clone()
#	t8.SetTitle("Photon Eta")
#	t8.SetXTitle("Eta")
#	h8.Add(t8)
		
	t9 = Rdf_Final.Histo1D(("t9", "N2DDT", 100, -.5, .5), "n2ddt", "weight")
	t9 = t9.Clone()
	t9.SetTitle("N2DDT")
	t9.SetXTitle("N2DDT")
	h9.Add(t9)
	
#	t1_presel = Rdf_PreSel.Histo1D(("t1_presel",  ';N^{2}_{1}', 50, 0, 0.5), "N2", "weight")
#	t1_presel = t1_presel.Clone()
#	t1_presel.SetTitle("N2")
#	t1_presel.SetXTitle("N2")
#	h1_presel.Add(t1_presel)

#	t2_presel = Rdf_PreSel.Histo1D(("t2_presel", "Softdrop Mass", 40, 0, 200), "jM", "weight")
#	t2_presel = t2_presel.Clone()
#	t2_presel.SetTitle("Softdrop Mass")
#	t2_presel.SetXTitle("Softdrop Mass")
#	h2_presel.Add(t2_presel)


#	t4_presel = Rdf_PreSel.Histo1D(("t4_presel", "Photon pT", 100, 0, 2000), "pPt", "weight")
#	t4_presel = t4_presel.Clone()
#	t4_presel.SetTitle("Photon pT")
#	t4_presel.SetXTitle("pT")
#	h4_presel.Add(t4_presel)
		
#	t5_presel = Rdf_PreSel.Histo1D(("t5_presel", "Jet pT", 40, 0, 2000), "jPt", "weight")
#	t5_presel = t5_presel.Clone()
#	t5_presel.SetTitle("Jet pT")
#	t5_presel.SetXTitle("pT")
#	h5_presel.Add(t5_presel)

 #       t5_1_presel = Rdf_PreSel.Histo1D(("t5_1_presel", "Thin Jet pT", 2000, 0, 2000), "jPt", "weight")
  #      t5_1_presel = t5_1_presel.Clone()
   #     t5_1_presel.SetTitle("Thin Jet pT")
    #    t5_1_presel.SetXTitle("pT")
     #   h5_1_presel.Add(t5_1_presel)

#	t6_presel = Rdf_PreSel.Histo1D(("t6_presel", "Jet Eta", 70, -3.5, 3.5), "jEta", "weight")
#	t6_presel = t6_presel.Clone()
#	t6_presel.SetTitle("Jet Eta")
#	t6_presel.SetXTitle("Eta")
#	h6_presel.Add(t6_presel)


#	t7_presel = Rdf_PreSel.Histo1D(("t7_presel", "Rho", 28, -8, -1), "Rho", "weight")
#	t7_presel = t7_presel.Clone()
#	t7_presel.SetTitle("Rho")
#	t7_presel.SetXTitle("Rho")
#	h7_presel.Add(t7_presel)

#	t8_presel = Rdf_PreSel.Histo1D(("t8_presel", "Photon Eta", 70, -3.5, -3.5), "pEta", "weight")
#	t8_presel = t8_presel.Clone()
#	t8_presel.SetTitle("Photon Eta")
#	t8_presel.SetXTitle("Eta")
#	h8_presel.Add(t8_presel)

	q1 = Rdf_Pass.Histo1D(("q1", "Passing Softdrop Mass", 40, 0, 200), "jM", "weight")
	q1 = q1.Clone()
	q1.SetTitle("Passing Softdrop Mass")
	q1.SetXTitle("Softdrop Mass")
	p1.Add(q1)
	
        q1_1 = Rdf_Pass.Histo1D(("q1_1", "Thin Passing Softdrop Mass", 100, 0, 200), "jM", "weight")
        q1_1 = q1_1.Clone()
        q1_1.SetTitle("Passing Softdrop Mass")
        q1_1.SetXTitle("Softdrop Mass")
        p1_1.Add(q1_1)
        
	q1_2 = Rdf_Pass.Histo1D(("q1_2", "Thin (Uncorrected) Passing Softdrop Mass", 100, 0, 200), "jM_uncorr", "weight")
        q1_2 = q1_2.Clone()
        q1_2.SetTitle("Thin (Uncorrected) Passing Softdrop Mass")
        q1_2.SetXTitle("Softdrop Mass")
        p1_2.Add(q1_2)
	
#	q2 = Rdf_Pass.Histo1D(("q2", "Passing Photon pT", 100, 0, 2000), "pPt", "weight")
#	q2 = q2.Clone()
#	q2.SetTitle("Passing Photon pT")
#	q2.SetXTitle("Photon pT")
#	p2.Add(q2)
		
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
		
#	q5 = Rdf_Pass.Histo1D(("q5", "Passing Photon Eta", 70, -3.5, 3.5), "pEta", "weight")
#	q5 = q5.Clone()
#	q5.SetTitle("Passing Photon Eta")
#	q5.SetXTitle("Photon Eta")
#	p5.Add(q5)
		
	q6 = Rdf_Pass.Histo1D(("q6", "Passing Jet Eta", 70, -3.5, 3.5), "jEta", "weight")
	q6 = q6.Clone()
	q6.SetTitle("Passing Jet Eta")
	q6.SetXTitle("Jet Eta")
	p6.Add(q6)
		
	u1 = Rdf_Fail.Histo1D(("u1", "Failing Softdrop Mass", 40, 0, 200), "jM", "weight")
	u1 = u1.Clone()
#		u1.Scale(1/9.0)
	u1.SetTitle("Failing Softdrop Mass")
	u1.SetXTitle("Softdrop Mass")
	f1.Add(u1)

        u1_1 = Rdf_Fail.Histo1D(("u1_1", "Failing Softdrop Mass", 100, 0, 200), "jM", "weight")
        u1_1 = u1_1.Clone()
#               u1.Scale(1/9.0)
        u1_1.SetTitle("Failing Softdrop Mass")
        u1_1.SetXTitle("Softdrop Mass")
        f1_1.Add(u1_1)
        
	u1_2 = Rdf_Fail.Histo1D(("u1_2", "Thin (Uncorrected) Failing Softdrop Mass", 100, 0, 200), "jM_uncorr", "weight")
        u1_2 = u1_2.Clone()
#               u1.Scale(1/9.0)
        u1_2.SetTitle("Thin (Uncorrected) Failing Softdrop Mass")
        u1_2.SetXTitle("Softdrop Mass")
        f1_2.Add(u1_2)
		
#	u2 = Rdf_Fail.Histo1D(("u2", "Failing Photon pT", 100, 0, 2000), "pPt", "weight")
#	u2 = u2.Clone()
#		u2.Scale(1/9.0)
#	u2.SetTitle("Failing Photon pT")
#	u2.SetXTitle("Photon pT")
#	f2.Add(u2)
		
	u3 = Rdf_Fail.Histo1D(("u3", "Failing Jet pT", 40, 0, 2000), "jPt", "weight")
	u3 = u3.Clone()
#		u3.Scale(1/9.0)
	u3.SetTitle("Failing Jet pT")
	u3.SetXTitle("Jet pT")
	f3.Add(u3)
		
	u4 = Rdf_Fail.Histo1D(("u4", "Failing Rho", 28, -8, -1), "Rho", "weight")
	u4 = u4.Clone()
#		u4.Scale(1/9.0)
	u4.SetTitle("Failing Rho")
	u4.SetXTitle("Rho")
	f4.Add(u4)
		
#	u5 = Rdf_Fail.Histo1D(("u5", "Failing Photon Eta", 70, -3.5, 3.5), "pEta", "weight")
#	u5 = u5.Clone()
#		u5.Scale(1/9.0)
#	u5.SetTitle("Failing Photon Eta")
#	u5.SetXTitle("Photon Eta")
#	f5.Add(u5)
		
	u6 = Rdf_Fail.Histo1D(("u6", "Failing Jet Eta", 70, -3.5, 3.5), "jEta", "weight")
	u6 = u6.Clone()
#		u6.Scale(1/9.0)
	u6.SetTitle("Failing Jet Eta")
	u6.SetXTitle("Jet Eta")
	f6.Add(u6)
		
	j11 =  Rdf_Final.Histo2D(("n2_n2ddt", "N2 vs. N2DDT", 50, 0, 0.5, 100, -.5, .5), "N2", "n2ddt", "weight")
	j11 = j11.Clone()
	h11.Add(j11)

		
		
	j14 = Rdf_Final.Histo2D(("n2_soft", "N2 vs. Softdrop Mass", 100, 0, 1, 40, 0, 200), "N2", "jM", "weight")
	j14 = j14.Clone()
	h14.Add(j14)
	
	j14_1 = Rdf_Final.Histo2D(("soft_n2", "Softdrop Mass vs. N2", 40, 0, 200, 100, 0, 1), "jM", "N2", "weight")
	j14_1 = j14_1.Clone()
	h14_1.Add(j14_1)

	j15 = Rdf_Final.Histo2D(("n2ddt_soft", "N2DDT vs. Softdrop Mass", 100, -.5, .5, 40, 0, 200), "n2ddt", "jM", "weight")
	j15 = j15.Clone()
	h15.Add(j15)
		
	j15_1 = Rdf_Final.Histo2D(("soft_n2ddt", "Softdrop Mass vs. N2DDT", 40, 0, 200, 100, -.5, .5), "jM", "n2ddt", "weight")
	j15_1 = j15_1.Clone()
	h15_1.Add(j15_1)

	j16 = Rdf_Final.Histo2D(("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200), "Rho", "jM", "weight")
	j16 = j16.Clone()
	h16.Add(j16)
	
	j17 = Rdf_Pass.Histo2D(("rho_soft_pass", "Passing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200), "Rho", "jM", "weight")
	j17 = j17.Clone()
	h17.Add(j17)
	
	j18 = Rdf_Fail.Histo2D(("rho_soft_fail", "Failing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200), "Rho", "jM", "weight")
	j18 = j18.Clone()
	h18.Add(j18)

	j19 = Rdf_Final.Histo2D(("n2_pt", "N2 vs. Jet pT", 100, 0, 1, 400, 0, 2000), "N2", "jPt", "weight")
	j19 = j19.Clone()
	h19.Add(j19)
	
	j19_1 = Rdf_Final.Histo2D(("pt_n2", "Jet pT vs. N2", 400, 0, 2000, 100, 0, 1), "jPt", "N2", "weight")
	j19_1 = j19_1.Clone()
	h19_1.Add(j19_1)

	j20 = Rdf_Final.Histo2D(("n2ddt_pt", "N2DDT vs. Jet pT", 100, -.5, .5, 400, 0, 2000), "n2ddt", "jPt", "weight")
	j20 = j20.Clone()
	h20.Add(j20)
		
	j20_1 = Rdf_Final.Histo2D(("pt_n2ddt", "Jet pT vs. N2DDT", 400, 0, 2000, 100, -.5, .5), "jPt", "n2ddt", "weight")
	j20_1 = j20_1.Clone()
	h20_1.Add(j20_1)

        j21 = Rdf_Pass.Histo2D(("pt_soft_pass", "Passing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
        j21 = j21.Clone()
        h21.Add(j21)


        j21_1 = Rdf_Final.Histo2D(("pt_soft_tot", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
        j21_1 = j21_1.Clone()
        h21_1.Add(j21_1)


        j23 = Rdf_Fail.Histo2D(("pt_soft_fail", "Failing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
        j23 = j23.Clone()
        h23.Add(j23)

		

	j24 = Rdf_Pass.Histo2D(("pt_rho_pass", "Passing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1), "jPt", "Rho", "weight")
	j24 = j24.Clone()
	h24.Add(j24)

	j25 = Rdf_Fail.Histo2D(("pt_rho_fail", "Failing Jet pT vs. Rho", 40, 0, 2000, 28, -8, -1), "jPt", "Rho", "weight")
	j25 = j25.Clone()
	h25.Add(j25)



        j50 = Rdf_Final.Histo1D(("j50", "AK4 Jet Eta", 70, -3.5, 3.5), "j4eta", "weight")
        j50 = j50.Clone()
        h50.Add(j50)
        j51 = Rdf_Final.Histo1D(("j51", "AK4 Jet Phi", 80, -4, 4), "j4phi", "weight")
        j51 = j51.Clone()
        h51.Add(j51)
        j52 = Rdf_Final.Histo1D(("j52", "AK4 nJet", 25, 0, 25), "nJet", "weight")
        j52 = j52.Clone()
        h52.Add(j52)
        j53 = Rdf_Final.Histo1D(("j53", "AK4 BTag", 100, 0, 1), "jBtag", "weight")
        j53 = j53.Clone()
        h53.Add(j53)
        
	j56 = Rdf_Final.Histo1D(("j56", "PuppiMET pT", 500, 0, 500), "PuppiMETpt", "weight")
        j56 = j56.Clone()
        h56.Add(j56)
	
	j57 = Rdf_Final.Histo1D(("j57", "PuppiMET pT + Muon pT", 700, 0, 700), "MET_mPt", "weight")
        j57 = j57.Clone()
        h57.Add(j57)


#        j65 = Rdf_Final.Histo2D(("j65", "Eta vs. Photon pT", 70, -3.5, 3.5, 100, 0, 2000), "pEta", "jPt", "weight")
#	j65 = j65.Clone()
#	h65.Add(j65)
        
	
	j80 = Rdf_Final.Histo1D(("j80", "AK4 HT", 1000, 0, 5000), "jHT", "weight")
        j80 = j80.Clone()
        h80.Add(j80)
	
	j81 = Rdf_Final.Histo1D(("j81", "AK8 HT", 1000, 0, 5000), "jHT_AK8", "weight")
        j81 = j81.Clone()
        h81.Add(j81)
	
	j90 = Rdf_Final.Histo1D(("j90", "AK4 Jet pT", 200, 0, 2000), "jPt_AK4", "weight")
        j90 = j90.Clone()
        h90.Add(j90)
	
	j91 = Rdf_Final.Histo1D(("j91", "Muon pT", 100, 0, 1000), "mPt", "weight")
        j91 = j91.Clone()
        h91.Add(j91)
	
	j91_1 = Rdf_Final.Histo1D(("j91_1", "(Thin) Muon pT", 1000, 0, 1000), "mPt", "weight")
        j91_1 = j91_1.Clone()
        h91_1.Add(j91_1)
	
	j92 = Rdf_Final.Histo1D(("j92", "Muon Eta", 70, -3.5, 3.5), "mEta", "weight")
        j92 = j92.Clone()
        h92.Add(j92)
	
	print(str(nocut)+" Events Before Cuts in "+fname+" Sample")		
	print(str(npcut)+" Events After nPho>0 in in "+fname+" Sample")		
	print(str(njcut)+" Events After nFatJet>0 in "+fname+" Sample")		
	print(str(trigcut)+" Events After Trigger Cuts in "+fname+" Sample")		
#	print(str(pcut)+" Events After Photon Cuts in "+fname+" Sample")		
	print(str(jcut)+" Events After Jet Cuts in "+fname+" Sample")		
	print(str(final)+" Events After Final Cuts in "+fname+" Sample")		
	print(str(pass_events)+" Passing Events in "+fname+" Sample")		
	print(str(fail_events)+" Failing Events in "+fname+" Sample")		
	

 	print("Total Number of Events: "+str(total_events))

	print("Cutflow Percentages: ")
	print("10% cut applied passed: "+str(ten_pass/total_events * 100)+"%")
	print("Trigger passed: "+str(trig_pass/total_events * 100)+"%")
	print("Num Pho and Num Jet passed: "+str(num_pass/total_events * 100)+"%")
#	print("Photon pT passed: "+str(ppt_pass/total_events * 100)+"%")
	if sample[3] == "QCD" or sample[3] == "GJ":
		print("Direct Prompt Photon cut: "+str(dir_prompt_pass/total_events * 100)+"%")
	print("Jet pT passed: "+str(jpt_pass/total_events * 100)+"%")
#	print("Photon Eta passed: "+str(peta_pass/total_events * 100)+"%")
	print("Jet Eta passed: "+str(jeta_pass/total_events * 100)+"%")
	print("Cut Based ID passed: "+str(pid_pass/total_events * 100)+"%")
	print("Jet ID passed: "+str(jid_pass/total_events * 100)+"%")
	print("Softdrop passed: "+str(jsoft_pass/total_events * 100)+"%")
	print("N2 passed: "+str(n2_pass/total_events * 100)+"%")
	print("Rho passed: "+str(rho_pass/total_events * 100)+"%")
#	print("DeltaR passed: "+str(dR_pass/total_events * 100)+"%")
	print("Passing Events: "+str(pass_pass/total_events * 100)+"%")
	print("Failing Events: "+str(fail_pass/total_events * 100)+"%")
	
	#print("Passing Fraction: "+str(pass_pass_weight/(pass_pass_weight+fail_pass_weight) * 100)+"%")


	h1.SetTitle("N2")
	h1.SetXTitle("N2")
	ofile.WriteObject(h1, "N2")

	h2.SetTitle("Softdrop Mass")
	h2.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2, "softdrop")

	h2_1.SetTitle("Thin Softdrop Mass")
	h2_1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2_1, "thin_softdrop")
	
	h2_2.SetTitle("Thin (Uncorrected) Softdrop Mass")
	h2_2.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2_2, "thin_uncorr_softdrop")

#	h4.SetTitle("Photon pT")
#	h4.SetXTitle("Photon pT")
#	ofile.WriteObject(h4, "photon_pt")

	h5.SetTitle("Jet pT")
	h5.SetXTitle("Jet pT")
	ofile.WriteObject(h5, "jet_pt")

	h5_1.SetTitle("Thin Jet pT")
	h5_1.SetXTitle("Jet pT")
        ofile.WriteObject(h5_1, "thin_jet_pt")

	h6.SetTitle("Jet Eta")
	h6.SetXTitle("Jet Eta")
	ofile.WriteObject(h6, "jet_eta")

	h7.SetTitle("Rho")
	h7.SetXTitle("Rho")
	ofile.WriteObject(h7, "rho")

#	h8.SetTitle("Photon Eta")
#	h8.SetXTitle("Photon Eta")
#	ofile.WriteObject(h8, "photon_eta")

	h9.SetTitle("N2DDT")
	h9.SetXTitle("N2DDT")
	ofile.WriteObject(h9, "n2ddt")
	
#	h1_presel.SetTitle("N2 Presel")
#	h1_presel.SetXTitle("N2 Presel")
#	ofile.WriteObject(h1_presel, "N2_presel")

#	h2_presel.SetTitle("Softdrop Mass Presel")
#	h2_presel.SetXTitle("Softdrop Mass Presel")
#	ofile.WriteObject(h2_presel, "softdrop_presel")

#	h4_presel.SetTitle("Photon pT Presel")
#	h4_presel.SetXTitle("Photon pT Presel")
#	ofile.WriteObject(h4_presel, "photon_pt_presel")

#	h5_presel.SetTitle("Jet pT Presel")
#	h5_presel.SetXTitle("Jet pT Presel")
#	ofile.WriteObject(h5_presel, "jet_pt_presel")

#	h5_1_presel.SetTitle("Thin Jet pT Presel")
#	h5_1_presel.SetXTitle("Jet pT Presel")
 #       ofile.WriteObject(h5_1_presel, "thin_jet_pt_presel")

#	h6_presel.SetTitle("Jet Eta Presel")
#	h6_presel.SetXTitle("Jet Eta Presel")
#	ofile.WriteObject(h6_presel, "jet_eta_presel")

#	h7_presel.SetTitle("Rho Presel")
#	h7_presel.SetXTitle("Rho Presel")
#	ofile.WriteObject(h7_presel, "rho_presel")

#	h8_presel.SetTitle("Photon Eta Presel")
#	h8_presel.SetXTitle("Photon Eta Presel")
#	ofile.WriteObject(h8_presel, "photon_eta_presel")
	
	h11.SetTitle("N2 vs. N2DDT")
	h11.SetXTitle("N2")
	h11.SetYTitle("N2DDT")
	ofile.WriteObject(h11, "n2_n2ddt")
	
	h14.SetTitle("N2 vs. Softdrop Mass")
	h14.SetXTitle("N2")
	h14.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h14, "n2_soft")
	
	h14_1.SetTitle("Softdrop Mass vs. N2")
	h14_1.SetXTitle("Softdrop Mass")
	h14_1.SetYTitle("N2")
	ofile.WriteObject(h14_1, "soft_n2")
	
	h15.SetTitle("N2DDT vs. Softdrop Mass")
	h15.SetXTitle("N2DDT")
	h15.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h15, "n2ddt_soft")

	h15_1.SetTitle("Softdrop Mass vs. N2DDT")
	h15_1.SetXTitle("Softdrop Mass")
	h15_1.SetYTitle("N2DDT")
	ofile.WriteObject(h15_1, "soft_n2ddt")

	h16.SetTitle("Rho vs. Softdrop Mass")
	h16.SetXTitle("Rho")
	h16.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h16, "rho_soft")
	
	h17.SetTitle("Passing Rho vs. Softdrop Mass")
	h17.SetXTitle("Rho")
	h17.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h17, "rho_soft_pass")
	
	h18.SetTitle("Failing Rho vs. Softdrop Mass")
	h18.SetXTitle("Rho")
	h18.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h18, "rho_soft_fail")

	h19.SetTitle("N2 vs. Jet pT")
	h19.SetXTitle("N2")
	h19.SetYTitle("Jet pT")
	ofile.WriteObject(h19, "n2_pt")
	
	h19_1.SetTitle("Jet pT vs. N2")
	h19_1.SetXTitle("Jet pT")
	h19_1.SetYTitle("N2")
	ofile.WriteObject(h19_1, "pt_n2")
	
	h20.SetTitle("N2DDT vs. Jet pT")
	h20.SetXTitle("N2DDT")
	h20.SetYTitle("Jet pT")
	ofile.WriteObject(h20, "n2ddt_pt")
	
	h20_1.SetTitle("Jet pT vs. N2DDT")
	h20_1.SetXTitle("Jet pT")
	h20_1.SetYTitle("N2DDT")
	ofile.WriteObject(h20_1, "pt_n2ddt")
	
	h21.SetTitle("Passing Jet pT vs. Softdrop Mass")
	h21.SetXTitle("Jet pT")
	h21.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h21, "jet_pt_soft_pass")
	
	h21_1.SetTitle("Total Jet pT vs. Softdrop Mass")
	h21_1.SetXTitle("Jet pT")
	h21_1.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h21_1, "jet_pt_soft_total")
	
	h23.SetTitle("Failing Jet pT vs. Softdrop Mass")
	h23.SetXTitle("Jet pT")
	h23.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h23, "jet_pt_soft_fail")
	
	h24.SetTitle("Passing Jet pT vs. RHo")
	h24.SetXTitle("Jet pT")
	h24.SetYTitle("Rho")
	ofile.WriteObject(h24, "jet_pt_rho_pass")
	
	h25.SetTitle("Failing Jet pT vs. RHo")
	h25.SetXTitle("Jet pT")
	h25.SetYTitle("Rho")
	ofile.WriteObject(h25, "jet_pt_rho_fail")


        h50.SetTitle("AK4 Jet Eta")
        h50.SetXTitle("Eta")
        ofile.WriteObject(h50, "ak4_eta")

        h51.SetTitle("AK4 Jet Phi")
        h51.SetXTitle("Phi")
        ofile.WriteObject(h51, "ak4_phi")

        h52.SetTitle("AK4 nJet")
        h52.SetXTitle("Number of Jets")
        ofile.WriteObject(h52, "ak4_njet")

        h53.SetTitle("AK4 BTag")
        h53.SetXTitle("DeepFlavB")
        ofile.WriteObject(h53, "ak4_btag")
        
	h56.SetTitle("PuppiMET pT")
        h56.SetXTitle("MET")
        ofile.WriteObject(h56, "MET")
	
	h57.SetTitle("PuppiMET pT + Muon pT")
        h57.SetXTitle("MET + Muon pT")
        ofile.WriteObject(h57, "METplusMUON")

        
#	h65.SetTitle("Eta vs. Photon pT")
#        h65.SetXTitle("Eta")
#        h65.SetYTitle("Photon pT")
#        ofile.WriteObject(h65, "eta_pho_pt")

	h80.SetXTitle("HT")
        ofile.WriteObject(h80, "HT")

	h81.SetXTitle("HT")
        ofile.WriteObject(h81, "HT_AK8")
	
	h90.SetXTitle("Jet pT")
	ofile.WriteObject(h90, "jet_pt_ak4")
	
	h91.SetXTitle("Muon pT")
	ofile.WriteObject(h91, "muon_pt")
	
	h91_1.SetXTitle("Muon pT")
	ofile.WriteObject(h91_1, "muon_pt_thin")
	
	h92.SetXTitle("Muon Eta")
	ofile.WriteObject(h92, "muon_eta")

	p1.SetTitle("Passing Softdrop Mass")
	p1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(p1, "pass_soft")

        p1_1.SetTitle("Thin Passing Softdrop Mass")
        p1_1.SetXTitle("Softdrop Mass")
        ofile.WriteObject(p1_1, "pass_soft_thin")
        
	p1_2.SetTitle("Thin (Uncorrected) Passing Softdrop Mass")
        p1_2.SetXTitle("Softdrop Mass")
        ofile.WriteObject(p1_2, "pass_soft_uncorr_thin")

#	p2.SetTitle("Passing Photon pT")
#	p2.SetXTitle("Photon pT")
#	ofile.WriteObject(p2, "pass_photon_pt")

	p3.SetTitle("Passing Jet pT")
	p3.SetXTitle("Jet pT")
	ofile.WriteObject(p3, "pass_jet_pt")

	p4.SetTitle("Passing Rho")
	p4.SetXTitle("Rho")
	ofile.WriteObject(p4, "pass_rho")

#	p5.SetTitle("Passing Photon Eta")
#	p5.SetXTitle("Photon Eta")
#	ofile.WriteObject(p5, "pass_photon_eta")

	p6.SetTitle("Passing Jet Eta")
	p6.SetXTitle("Jet Eta")
	ofile.WriteObject(p6, "pass_jet_eta")

	f1.SetTitle("Failing Softdrop Mass")
	f1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(f1, "fail_soft")

        f1_1.SetTitle("Thin Failing Softdrop Mass")
        f1_1.SetXTitle("Softdrop Mass")
        ofile.WriteObject(f1_1, "fail_soft_thin")
        
	f1_2.SetTitle("Thin (Uncorrected) Failing Softdrop Mass")
        f1_2.SetXTitle("Softdrop Mass")
        ofile.WriteObject(f1_2, "fail_soft_uncorr_thin")

#	f2.SetTitle("Failing Photon pT")
#	f2.SetXTitle("Photon pT")
#	ofile.WriteObject(f2, "fail_photon_pt")

	f3.SetTitle("Failing Jet pT")
	f3.SetXTitle("Jet pT")
	ofile.WriteObject(f3, "fail_jet_pt")

	f4.SetTitle("Failing Rho")
	f4.SetXTitle("Rho")
	ofile.WriteObject(f4, "fail_rho")

#	f5.SetTitle("Failing Photon Eta")
#	f5.SetXTitle("Photon Eta")
#	ofile.WriteObject(f5, "fail_photon_eta")

	f6.SetTitle("Failing Jet Eta")
	f6.SetXTitle("Jet Eta")
	ofile.WriteObject(f6, "fail_jet_eta")


	weighting = float(sample[1])
	#No cut, 10% cut, nphoton cut, njet cut, photon pT cut, jet pT cut, photon eta cut, jet eta cut, photon ID cut, Jet ID cut, Softdrop cut, Trigger cut, N2 cut, rho cut, dR cut, final, passing, failing
	#cut_vals = TVectorD(0, 17, nocut*weighting, npcut*weighting, njcut*weighting, ppt_pass*weighting, jpt_pass*weighting, peta_pass*weighting, jeta_pass*weighting, pid_pass*weighting, jid_pass*weighting, jsoft_pass*weighting, trig_pass*weighting, n2_pass*weighting, rho_pass*weighting, dR_pass*weighting, final*weighting, pass_pass*weighting, fail_pass*weighting)
#	cut_vals = TVectorF(0, 16)
#	cut_vals[0] = nocut*weighting
#	cut_vals[1] = npcut*weighting
#	cut_vals[2] = njcut*weighting
#	cut_vals[3] = ppt_pass*weighting
#	cut_vals[4] = jpt_pass*weighting
#	cut_vals[5] = peta_pass*weighting
#	cut_vals[6] = jeta_pass*weighting
#	cut_vals[7] = pid_pass*weighting
#	cut_vals[8] = jid_pass*weighting
#	cut_vals[9] = jsoft_pass*weighting
#	cut_vals[10] = trig_pass*weighting
#	cut_vals[11] = n2_pass*weighting
#	cut_vals[12] = rho_pass*weighting
#	cut_vals[13] = dR_pass*weighting
#	cut_vals[14] = final*weighting
#	cut_vals[15] = pass_pass*weighting
#	cut_vals[16] = fail_pass*weighting
#	ofile.WriteObject(cut_vals, "cut_vals")

	cut_vals = TH1F("cut_vals", "Cut Values", 25, 0, 25)
	cut_vals.SetBinContent(0,nocut*weighting)
	cut_vals.SetBinContent(1,ten_pass*weighting)
	cut_vals.SetBinContent(2,npcut*weighting)
	cut_vals.SetBinContent(3,njcut*weighting)
	cut_vals.SetBinContent(4,ppt_pass*weighting)
	cut_vals.SetBinContent(5,jpt_pass*weighting)
	cut_vals.SetBinContent(6,peta_pass*weighting)
	cut_vals.SetBinContent(7,jeta_pass*weighting)
	cut_vals.SetBinContent(8,pid_pass*weighting)
	cut_vals.SetBinContent(9,jid_pass*weighting)
	cut_vals.SetBinContent(10,jsoft_pass*weighting)
	cut_vals.SetBinContent(11,trig_pass*weighting)
	cut_vals.SetBinContent(12,n2_pass*weighting)
	cut_vals.SetBinContent(13,rho_pass*weighting)
	cut_vals.SetBinContent(14,dR_pass*weighting)
	cut_vals.SetBinContent(15,final*weighting)
	cut_vals.SetBinContent(16,pass_pass*weighting)
	cut_vals.SetBinContent(17,fail_pass*weighting)
	cut_vals.SetBinContent(18,dir_prompt_pass*weighting)
	cut_vals.SetBinContent(19,final)
	cut_vals.SetBinContent(20,pass_pass)
	cut_vals.SetBinContent(21,fail_pass)
	cut_vals.SetBinContent(22,nocut)
	
	
	ofile.Write()
