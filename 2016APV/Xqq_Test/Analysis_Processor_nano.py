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



def DataPro(sample, fname):

	gROOT.SetBatch(True)

	ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/Xqq_Test/output/RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()



	#x1 = TH1F("x1", "ParticleNet Xqq Score", 100, 0, 1)
	x1 = TH1F("x1", "ParticleNetMD Xqq Score", 100, 0, 1)
	x1_1 = TH1F("x1_1", "ParticleNetMD Xqq/(Xqq+QCD) Score", 100, 0, 1)
	
#	x2_10 = TH1F("x2_10", "Softdrop Mass For Xqq/(Xqq+QCD) > .10", 40, 0, 200)
#	x2_15 = TH1F("x2_15", "Softdrop Mass For Xqq/(Xqq+QCD) > .15", 40, 0, 200)
#	x2_20 = TH1F("x2_20", "Softdrop Mass For Xqq/(Xqq+QCD) > .20", 40, 0, 200)
#	x2_25 = TH1F("x2_25", "Softdrop Mass For Xqq/(Xqq+QCD) > .25", 40, 0, 200)
#	x2_30 = TH1F("x2_30", "Softdrop Mass For Xqq/(Xqq+QCD) > .30", 40, 0, 200)
#	x2_35 = TH1F("x2_35", "Softdrop Mass For Xqq/(Xqq+QCD) > .35", 40, 0, 200)
#	x2_40 = TH1F("x2_40", "Softdrop Mass For Xqq/(Xqq+QCD) > .40", 40, 0, 200)
#	x2_45 = TH1F("x2_45", "Softdrop Mass For Xqq/(Xqq+QCD) > .45", 40, 0, 200)
#	x2_50 = TH1F("x2_50", "Softdrop Mass For Xqq/(Xqq+QCD) > .50", 40, 0, 200)
#	x2_55 = TH1F("x2_55", "Softdrop Mass For Xqq/(Xqq+QCD) > .55", 40, 0, 200)
#	x2_60 = TH1F("x2_60", "Softdrop Mass For Xqq/(Xqq+QCD) > .60", 40, 0, 200)
#	x2_65 = TH1F("x2_65", "Softdrop Mass For Xqq/(Xqq+QCD) > .65", 40, 0, 200)
#	x2_70 = TH1F("x2_70", "Softdrop Mass For Xqq/(Xqq+QCD) > .70", 40, 0, 200)
#	x2_75 = TH1F("x2_75", "Softdrop Mass For Xqq/(Xqq+QCD) > .75", 40, 0, 200)
	x2_80 = TH1F("x2_80", "Softdrop Mass For Xqq/(Xqq+QCD) > .80", 40, 0, 200)
	x2_85 = TH1F("x2_85", "Softdrop Mass For Xqq/(Xqq+QCD) > .85", 40, 0, 200)
	x2_90 = TH1F("x2_90", "Softdrop Mass For Xqq/(Xqq+QCD) > .90", 40, 0, 200)
	x2_91 = TH1F("x2_91", "Softdrop Mass For Xqq/(Xqq+QCD) > .91", 40, 0, 200)
	x2_92 = TH1F("x2_92", "Softdrop Mass For Xqq/(Xqq+QCD) > .92", 40, 0, 200)
	x2_93 = TH1F("x2_93", "Softdrop Mass For Xqq/(Xqq+QCD) > .93", 40, 0, 200)
	x2_94 = TH1F("x2_94", "Softdrop Mass For Xqq/(Xqq+QCD) > .94", 40, 0, 200)
	x2_95 = TH1F("x2_95", "Softdrop Mass For Xqq/(Xqq+QCD) > .95", 40, 0, 200)
	x2_96 = TH1F("x2_96", "Softdrop Mass For Xqq/(Xqq+QCD) > .96", 40, 0, 200)
	x2_97 = TH1F("x2_97", "Softdrop Mass For Xqq/(Xqq+QCD) > .97", 40, 0, 200)
	x2_98 = TH1F("x2_98", "Softdrop Mass For Xqq/(Xqq+QCD) > .98", 40, 0, 200)
	x2_99 = TH1F("x2_99", "Softdrop Mass For Xqq/(Xqq+QCD) > .99", 40, 0, 200)
	
	x3 = TH1F("x3", "ParticleNetMD QCD Score", 100, 0, 1)
	x4 = TH1F("x4", "ParticleNetMD Xcc Score", 100, 0, 1)
	x4_1 = TH1F("x4_1", "ParticleNetMD (Xcc+Xqq)/(Xcc+Xqq+QCD) Score", 100, 0, 1)
	x5 = TH1F("x5", "ParticleNetMD Xbb Score", 100, 0, 1)
	x6 = TH1F("x6", "ParticleNetMD (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) Score", 100, 0, 1)
	
#	x6_10 = TH1F("x6_10", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .10", 40, 0, 200)
#	x6_15 = TH1F("x6_15", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .15", 40, 0, 200)
#	x6_20 = TH1F("x6_20", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .20", 40, 0, 200)
#	x6_25 = TH1F("x6_25", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .25", 40, 0, 200)
#	x6_30 = TH1F("x6_30", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .30", 40, 0, 200)
#	x6_35 = TH1F("x6_35", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .35", 40, 0, 200)
#	x6_40 = TH1F("x6_40", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .40", 40, 0, 200)
#	x6_45 = TH1F("x6_45", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .45", 40, 0, 200)
#	x6_50 = TH1F("x6_50", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .50", 40, 0, 200)
#	x6_55 = TH1F("x6_55", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .55", 40, 0, 200)
#	x6_60 = TH1F("x6_60", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .60", 40, 0, 200)
#	x6_65 = TH1F("x6_65", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .65", 40, 0, 200)
#	x6_70 = TH1F("x6_70", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .70", 40, 0, 200)
#	x6_75 = TH1F("x6_75", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .75", 40, 0, 200)
	x6_80 = TH1F("x6_80", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .80", 40, 0, 200)
	x6_85 = TH1F("x6_85", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .85", 40, 0, 200)
	x6_90 = TH1F("x6_90", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .90", 40, 0, 200)
	x6_91 = TH1F("x6_91", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .91", 40, 0, 200)
	x6_92 = TH1F("x6_92", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .92", 40, 0, 200)
	x6_93 = TH1F("x6_93", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .93", 40, 0, 200)
	x6_94 = TH1F("x6_94", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .94", 40, 0, 200)
	x6_95 = TH1F("x6_95", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .95", 40, 0, 200)
	x6_96 = TH1F("x6_96", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .96", 40, 0, 200)
	x6_97 = TH1F("x6_97", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .97", 40, 0, 200)
	x6_98 = TH1F("x6_98", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .98", 40, 0, 200)
	x6_99 = TH1F("x6_99", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .99", 40, 0, 200)
		

	h2 = TH1F("h2", "Softdrop Mass", 40, 0, 200)
	h4 = TH1F("h4", "Photon pT", 50, 0, 1000)
	h5 = TH1F("h5", "Jet pT", 40, 0, 2000)
        h5_1 = TH1F("h5_1", "Thin Jet pT", 2000, 0, 2000)
	h6 = TH1F("h6", "Jet Eta", 70, -3.5, 3.5)
	h7 = TH1F("h7", "Rho", 28, -8, -1)
	h8 = TH1F("h8", "Photon Eta", 70, -3.5, 3.5)
	
	
	h16 = TH2F("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h19 = TH2F("n2_pt", "N2 vs. Jet pT", 50, 0, 0.5, 40, 0, 2000)
        h21_1 = TH2F("jet_pt_soft_total", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200)



        ROOT.gInterpreter.Declare("Double_t widebins4[16] = {0, 120, 130, 145, 160, 180, 200, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
	#Rebined to 1 GeV bin width
        #h29_w = TH2F("jet_pt_soft_pass_wide4", "Passing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        #h30_w = TH2F("jet_pt_soft_total_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        #h31_w = TH2F("jet_pt_soft_fail_wide4", "Failing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        h30_w = TH2F("jet_pt_soft_total_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200)

        h33_w = TH2F("jet_pt_soft_total_wide4_wide", "Wide Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)


        h36_w = TH2F("jet_pt_rho_total_wide4_thin", "Total Jet pT vs. Rho", 15, widebins4, 28, -8, -1)

	#2016APV pT Binning
        ROOT.gInterpreter.Declare("Double_t widebins5[8] = {0, 220, 245, 270, 300, 355, 500, 2000};")
        h39_w = TH2F("jet_pt_soft_total_wide5", "Total Jet pT vs. Softdrop Mass", 7, widebins5, 40, 0, 200)


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

	
	
	if sample[3] == "data": #Take 10% of Data
                Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0")
                ten_pass += float(Rdf_noCut.Count().GetValue())
	Rdf_noCut = Rdf_noCut.Filter("(HLT_Photon175 >0.0)")

	trig_pass += float(Rdf_noCut.Count().GetValue())

	Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
	npcut += float(Rdf_PreSel.Count().GetValue())

	Rdf_PreSel = Rdf_PreSel.Filter("nFatJet > 0.")
	njcut += float(Rdf_PreSel.Count().GetValue())
	num_pass += float(Rdf_PreSel.Count().GetValue())

#	Rdf_cflow = Rdf_PreSel.Filter("PPT(Photon_pt, nPhoton)")
#	ppt_pass += float(Rdf_cflow.Count().GetValue())
	#Direct Prompt Photon CutFlow
#	if sample[3] == "GJ":
#		Rdf_cflow = Rdf_cflow.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
#		dir_prompt_pass += float(Rdf_cflow.Count().GetValue())
#	if sample[3] == "QCD":
#		Rdf_cflow = Rdf_cflow.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
#		dir_prompt_pass += float(Rdf_cflow.Count().GetValue())


#	Rdf_cflow = Rdf_cflow.Filter("JPT(FatJet_pt_nom, nFatJet)")
#	jpt_pass += float(Rdf_cflow.Count().GetValue())
#
#	Rdf_cflow = Rdf_cflow.Filter("PETA(Photon_pt, Photon_eta, nPhoton)")
#	peta_pass += float(Rdf_cflow.Count().GetValue())

#	Rdf_cflow = Rdf_cflow.Filter("JETA(FatJet_pt_nom, FatJet_eta, nFatJet)")
#	jeta_pass += float(Rdf_cflow.Count().GetValue())
#
#	Rdf_cflow = Rdf_cflow.Filter("PID(Photon_pt, Photon_eta, Photon_cutBased, nPhoton)")
#	pid_pass += float(Rdf_cflow.Count().GetValue())
#
#	Rdf_cflow = Rdf_cflow.Filter("JID(FatJet_pt_nom, FatJet_eta, FatJet_jetId, nFatJet)")
#	jid_pass += float(Rdf_cflow.Count().GetValue())

#	Rdf_cflow = Rdf_cflow.Filter("JSOFT(FatJet_pt_nom, FatJet_eta, FatJet_jetId,FatJet_msoftdrop_raw, nFatJet)")
#	jsoft_pass += float(Rdf_cflow.Count().GetValue())
       
		
#	Rdf_cflow = Rdf_cflow.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
#	Rdf_cflow = Rdf_cflow.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

#	Rdf_cflow = Rdf_cflow.Filter("FatJet_n2b1[jIndex]")
#	n2_pass += float(Rdf_cflow.Count().GetValue())

#	Rdf_cflow = Rdf_cflow.Define("Rho", "rho(FatJet_pt_nom[jIndex], FatJet_msoftdrop_raw[jIndex])")
#	Rdf_cflow = Rdf_cflow.Filter("Rho > -7 && Rho < -2")
		
#	rho_pass += float(Rdf_cflow.Count().GetValue())


	
	#ROOT.gInterpreter.Declare('#include "Help.h"')
	Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")
	
	#Direct Prompt Filter
	if sample[3] == "GJ":
		Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	if sample[3] == "QCD":
		Rdf_PreSel = Rdf_PreSel.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	#Trigger Filter
	Rdf_PreSel = Rdf_PreSel.Filter("(HLT_Photon175 >0.0)")

	trigcut += float(Rdf_PreSel.Count().GetValue())

	Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	pcut += float(Rdf.Count().GetValue())
	
		
	Rdf = Rdf.Filter("jIndex >= 0")
	jcut += float(Rdf.Count().GetValue())
	
	
	Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]")
	Rdf = Rdf.Define("jEta", "FatJet_eta[jIndex]")
	Rdf = Rdf.Define("jPhi", "FatJet_phi[jIndex]")
	Rdf = Rdf.Define("jPt", "FatJet_pt_nom[jIndex]")
	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
	Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
	Rdf = Rdf.Define("N2", "FatJet_n2b1[jIndex]")
	Rdf = Rdf.Define("jID", "FatJet_jetId[jIndex]")
	Rdf = Rdf.Define("Xqq", "FatJet_particleNetMD_Xqq[jIndex]")
	Rdf = Rdf.Define("QCD", "FatJet_particleNetMD_QCD[jIndex]")
	Rdf = Rdf.Define("Xcc", "FatJet_particleNetMD_Xcc[jIndex]")
	Rdf = Rdf.Define("Xbb", "FatJet_particleNetMD_Xbb[jIndex]")
	Rdf = Rdf.Define("Xqq_QCD", "Xqq/(Xqq+QCD)")
	Rdf = Rdf.Define("Xcc_QCD", "(Xqq+Xcc)/(Xqq+QCD+Xcc)")
	Rdf = Rdf.Define("AllQQ", "(Xqq+Xcc+Xbb)/(Xqq+QCD+Xcc+Xbb)")
	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")

	Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
        Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")

        Rdf = Rdf.Define("nj4", "nJet")
        Rdf = Rdf.Define("ak4_nomatch", "ak4_match(nj4, Jet_eta, Jet_phi, jEta, jPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that do NOT match the boosted AK8 jet sorted by btag score

        Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_nomatch, Jet_btagDeepFlavB)[0]")

        Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")
        Rdf = Rdf.Define("PuppiMET_Et", "PuppiMET_sumEt")
	
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
                Rdf = Rdf.Define("xs_lumi", sample[1])
                Rdf = Rdf.Define("weight", "xs_lumi*puWeight")
        elif sample[3] == "data":
                Rdf = Rdf.Define("weight", sample[1])

	

	Rdf_Final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2")
	dR_pass += float(Rdf_Final.Count().GetValue())

        Rdf_MET = Rdf_Final.Filter("PuppiMETpt < 75") #Additional MET cut for btag testing
        Rdf_Final = Rdf_Final.Filter("PuppiMETpt < 75 && jBtag < 0.0480")

        final += float(Rdf_Final.Count().GetValue())
#	print(final)	
	
	xt1 = Rdf_Final.Histo1D(("xt1", "Particle Net Xqq Score", 100, 0, 1), "Xqq", "weight")
	xt1 = xt1.Clone()
	xt1.SetTitle("Particle Net Xqq Score")
	xt1.SetXTitle("Xqq Score")
	x1.Add(xt1)

	xt1_1 = Rdf_Final.Histo1D(("xt1_1", "Particle Net Xqq/(Xqq+QCD) Score", 100, 0, 1), "Xqq_QCD", "weight")
	xt1_1 = xt1_1.Clone()
	xt1_1.SetTitle("Particle Net Xqq/(Xqq+QCD) Score")
	xt1_1.SetXTitle("Xqq/(Xqq+QCD) Score")
	x1_1.Add(xt1_1)
	
	xt3 = Rdf_Final.Histo1D(("xt3", "Particle Net QCD Score", 100, 0, 1), "QCD", "weight")
	xt3 = xt3.Clone()
	xt3.SetTitle("Particle Net QCD Score")
	xt3.SetXTitle("QCD Score")
	x3.Add(xt3)
	
	xt4 = Rdf_Final.Histo1D(("xt4", "Particle Net Xcc Score", 100, 0, 1), "Xcc", "weight")
	xt4 = xt4.Clone()
	xt4.SetTitle("Particle Net Xcc Score")
	xt4.SetXTitle("Xcc Score")
	x4.Add(xt4)
	
	xt4_1 = Rdf_Final.Histo1D(("xt4_1", "Particle Net (Xqq+Xcc)/(Xqq+QCD) Score", 100, 0, 1), "Xcc_QCD", "weight")
	xt4_1 = xt4_1.Clone()
	xt4_1.SetTitle("Particle Net (Xqq+Xcc)/(Xqq+QCD) Score")
	xt4_1.SetXTitle("Xqq/(Xqq+QCD) Score")
	x4_1.Add(xt4_1)
	
	xt5 = Rdf_Final.Histo1D(("xt5", "Particle Net Xbb Score", 100, 0, 1), "Xbb", "weight")
	xt5 = xt5.Clone()
	xt5.SetTitle("Particle Net Xbb Score")
	xt5.SetXTitle("Xbb Score")
	x5.Add(xt5)
	
	xt6 = Rdf_Final.Histo1D(("xt6", "Particle Net (Xqq+Xcc+Xbb)/(Xcc+Xbb+Xqq+QCD) Score", 100, 0, 1), "AllQQ", "weight")
	xt6 = xt6.Clone()
	xt6.SetTitle("Particle Net (Xqq+Xcc+Xbb)/(Xcc+Xbb+Xqq+QCD) Score")
	xt6.SetXTitle("Xqq/(Xqq+QCD) Score")
	x6.Add(xt6)

#	Rdf_Xqq10 = Rdf_Final.Filter("Xqq_QCD > .10")
#	Rdf_Xqq15 = Rdf_Final.Filter("Xqq_QCD > .15")
#	Rdf_Xqq20 = Rdf_Final.Filter("Xqq_QCD > .20")
#	Rdf_Xqq25 = Rdf_Final.Filter("Xqq_QCD > .25")
#	Rdf_Xqq30 = Rdf_Final.Filter("Xqq_QCD > .30")
#	Rdf_Xqq35 = Rdf_Final.Filter("Xqq_QCD > .35")
#	Rdf_Xqq40 = Rdf_Final.Filter("Xqq_QCD > .40")
#	Rdf_Xqq45 = Rdf_Final.Filter("Xqq_QCD > .45")
#	Rdf_Xqq50 = Rdf_Final.Filter("Xqq_QCD > .50")
#	Rdf_Xqq55 = Rdf_Final.Filter("Xqq_QCD > .55")
#	Rdf_Xqq60 = Rdf_Final.Filter("Xqq_QCD > .60")
#	Rdf_Xqq65 = Rdf_Final.Filter("Xqq_QCD > .65")
#	Rdf_Xqq70 = Rdf_Final.Filter("Xqq_QCD > .70")
#	Rdf_Xqq75 = Rdf_Final.Filter("Xqq_QCD > .75")
	Rdf_Xqq80 = Rdf_Final.Filter("Xqq_QCD > .80")
	Rdf_Xqq85 = Rdf_Final.Filter("Xqq_QCD > .85")
	Rdf_Xqq90 = Rdf_Final.Filter("Xqq_QCD > .90")
	Rdf_Xqq91 = Rdf_Final.Filter("Xqq_QCD > .91")
	Rdf_Xqq92 = Rdf_Final.Filter("Xqq_QCD > .92")
	Rdf_Xqq93 = Rdf_Final.Filter("Xqq_QCD > .93")
	Rdf_Xqq94 = Rdf_Final.Filter("Xqq_QCD > .94")
	Rdf_Xqq95 = Rdf_Final.Filter("Xqq_QCD > .95")
	Rdf_Xqq96 = Rdf_Final.Filter("Xqq_QCD > .96")
	Rdf_Xqq97 = Rdf_Final.Filter("Xqq_QCD > .97")
	Rdf_Xqq98 = Rdf_Final.Filter("Xqq_QCD > .98")
	Rdf_Xqq99 = Rdf_Final.Filter("Xqq_QCD > .99")
	
	Xqq80 = float(Rdf_Xqq80.Count().GetValue())
	Xqq85 = float(Rdf_Xqq85.Count().GetValue())
	Xqq90 = float(Rdf_Xqq90.Count().GetValue())
	Xqq91 = float(Rdf_Xqq91.Count().GetValue())
	Xqq92 = float(Rdf_Xqq92.Count().GetValue())
	Xqq93 = float(Rdf_Xqq93.Count().GetValue())
	Xqq94 = float(Rdf_Xqq94.Count().GetValue())
	Xqq95 = float(Rdf_Xqq95.Count().GetValue())
	Xqq96 = float(Rdf_Xqq96.Count().GetValue())
	Xqq97 = float(Rdf_Xqq97.Count().GetValue())
	Xqq98 = float(Rdf_Xqq98.Count().GetValue())
	Xqq99 = float(Rdf_Xqq99.Count().GetValue())
	
#	Rdf_AllQQ10 = Rdf_Final.Filter("AllQQ > .10")
#	Rdf_AllQQ15 = Rdf_Final.Filter("AllQQ > .15")
#	Rdf_AllQQ20 = Rdf_Final.Filter("AllQQ > .20")
#	Rdf_AllQQ25 = Rdf_Final.Filter("AllQQ > .25")
#	Rdf_AllQQ30 = Rdf_Final.Filter("AllQQ > .30")
#	Rdf_AllQQ35 = Rdf_Final.Filter("AllQQ > .35")
#	Rdf_AllQQ40 = Rdf_Final.Filter("AllQQ > .40")
#	Rdf_AllQQ45 = Rdf_Final.Filter("AllQQ > .45")
#	Rdf_AllQQ50 = Rdf_Final.Filter("AllQQ > .50")
#	Rdf_AllQQ55 = Rdf_Final.Filter("AllQQ > .55")
#	Rdf_AllQQ60 = Rdf_Final.Filter("AllQQ > .60")
#	Rdf_AllQQ65 = Rdf_Final.Filter("AllQQ > .65")
#	Rdf_AllQQ70 = Rdf_Final.Filter("AllQQ > .70")
#	Rdf_AllQQ75 = Rdf_Final.Filter("AllQQ > .75")
	Rdf_AllQQ80 = Rdf_Final.Filter("AllQQ > .80")
	Rdf_AllQQ85 = Rdf_Final.Filter("AllQQ > .85")
	Rdf_AllQQ90 = Rdf_Final.Filter("AllQQ > .90")
	Rdf_AllQQ91 = Rdf_Final.Filter("AllQQ > .91")
	Rdf_AllQQ92 = Rdf_Final.Filter("AllQQ > .92")
	Rdf_AllQQ93 = Rdf_Final.Filter("AllQQ > .93")
	Rdf_AllQQ94 = Rdf_Final.Filter("AllQQ > .94")
	Rdf_AllQQ95 = Rdf_Final.Filter("AllQQ > .95")
	Rdf_AllQQ96 = Rdf_Final.Filter("AllQQ > .96")
	Rdf_AllQQ97 = Rdf_Final.Filter("AllQQ > .97")
	Rdf_AllQQ98 = Rdf_Final.Filter("AllQQ > .98")
	Rdf_AllQQ99 = Rdf_Final.Filter("AllQQ > .99")
	
	AllQQ80 = float(Rdf_AllQQ80.Count().GetValue())
	AllQQ85 = float(Rdf_AllQQ85.Count().GetValue())
	AllQQ90 = float(Rdf_AllQQ90.Count().GetValue())
	AllQQ91 = float(Rdf_AllQQ91.Count().GetValue())
	AllQQ92 = float(Rdf_AllQQ92.Count().GetValue())
	AllQQ93 = float(Rdf_AllQQ93.Count().GetValue())
	AllQQ94 = float(Rdf_AllQQ94.Count().GetValue())
	AllQQ95 = float(Rdf_AllQQ95.Count().GetValue())
	AllQQ96 = float(Rdf_AllQQ96.Count().GetValue())
	AllQQ97 = float(Rdf_AllQQ97.Count().GetValue())
	AllQQ98 = float(Rdf_AllQQ98.Count().GetValue())
	AllQQ99 = float(Rdf_AllQQ99.Count().GetValue())

#	xt2_10 = Rdf_Xqq10.Histo1D(("xt2_10", "Softdrop Mass For Xqq/(Xqq+QCD) > .10", 40, 0, 200), "jM", "weight")
#	xt2_10 = xt2_10.Clone()
#	xt2_10.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .10")
#	xt2_10.SetXTitle("Softdrop Mass")
#	x2_10.Add(xt2_10)

#	xt2_15 = Rdf_Xqq15.Histo1D(("xt2_15", "Softdrop Mass For Xqq/(Xqq+QCD) > .15", 40, 0, 200), "jM", "weight")
#	xt2_15 = xt2_15.Clone()
#	xt2_15.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .15")
#	xt2_15.SetXTitle("Softdrop Mass")
#	x2_15.Add(xt2_15)

#	xt2_20 = Rdf_Xqq20.Histo1D(("xt2_20", "Softdrop Mass For Xqq/(Xqq+QCD) > .20", 40, 0, 200), "jM", "weight")
#	xt2_20 = xt2_20.Clone()
#	xt2_20.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .20")
#	xt2_20.SetXTitle("Softdrop Mass")
#	x2_20.Add(xt2_20)

#	xt2_25 = Rdf_Xqq25.Histo1D(("xt2_25", "Softdrop Mass For Xqq/(Xqq+QCD) > .25", 40, 0, 200), "jM", "weight")
#	xt2_25 = xt2_25.Clone()
#	xt2_25.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .25")
#	xt2_25.SetXTitle("Softdrop Mass")
#	x2_25.Add(xt2_25)

#	xt2_30 = Rdf_Xqq30.Histo1D(("xt2_30", "Softdrop Mass For Xqq/(Xqq+QCD) > .30", 40, 0, 200), "jM", "weight")
#	xt2_30 = xt2_30.Clone()
#	xt2_30.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .30")
#	xt2_30.SetXTitle("Softdrop Mass")
#	x2_30.Add(xt2_30)

#	xt2_35 = Rdf_Xqq35.Histo1D(("xt2_35", "Softdrop Mass For Xqq/(Xqq+QCD) > .35", 40, 0, 200), "jM", "weight")
#	xt2_35 = xt2_35.Clone()
#	xt2_35.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .35")
#	xt2_35.SetXTitle("Softdrop Mass")
#	x2_35.Add(xt2_35)

#	xt2_40 = Rdf_Xqq40.Histo1D(("xt2_40", "Softdrop Mass For Xqq/(Xqq+QCD) > .40", 40, 0, 200), "jM", "weight")
#	xt2_40 = xt2_40.Clone()
#	xt2_40.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .40")
#	xt2_40.SetXTitle("Softdrop Mass")
#	x2_40.Add(xt2_40)

#	xt2_45 = Rdf_Xqq45.Histo1D(("xt2_45", "Softdrop Mass For Xqq/(Xqq+QCD) > .45", 40, 0, 200), "jM", "weight")
#	xt2_45 = xt2_45.Clone()
#	xt2_45.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .45")
#	xt2_45.SetXTitle("Softdrop Mass")
#	x2_45.Add(xt2_45)

#	xt2_50 = Rdf_Xqq50.Histo1D(("xt2_50", "Softdrop Mass For Xqq/(Xqq+QCD) > .50", 40, 0, 200), "jM", "weight")
#	xt2_50 = xt2_50.Clone()
#	xt2_50.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .50")
#	xt2_50.SetXTitle("Softdrop Mass")
#	x2_50.Add(xt2_50)

#	xt2_55 = Rdf_Xqq55.Histo1D(("xt2_55", "Softdrop Mass For Xqq/(Xqq+QCD) > .55", 40, 0, 200), "jM", "weight")
#	xt2_55 = xt2_55.Clone()
#	xt2_55.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .55")
#	xt2_55.SetXTitle("Softdrop Mass")
#	x2_55.Add(xt2_55)

#	xt2_60 = Rdf_Xqq60.Histo1D(("xt2_60", "Softdrop Mass For Xqq/(Xqq+QCD) > .60", 40, 0, 200), "jM", "weight")
#	xt2_60 = xt2_60.Clone()
#	xt2_60.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .60")
#	xt2_60.SetXTitle("Softdrop Mass")
#	x2_60.Add(xt2_60)

#	xt2_65 = Rdf_Xqq65.Histo1D(("xt2_65", "Softdrop Mass For Xqq/(Xqq+QCD) > .65", 40, 0, 200), "jM", "weight")
#	xt2_65 = xt2_65.Clone()
#	xt2_65.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .65")
#	xt2_65.SetXTitle("Softdrop Mass")
#	x2_65.Add(xt2_65)

#	xt2_70 = Rdf_Xqq70.Histo1D(("xt2_70", "Softdrop Mass For Xqq/(Xqq+QCD) > .70", 40, 0, 200), "jM", "weight")
#	xt2_70 = xt2_70.Clone()
#	xt2_70.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .70")
#	xt2_70.SetXTitle("Softdrop Mass")
#	x2_70.Add(xt2_70)

#	xt2_75 = Rdf_Xqq75.Histo1D(("xt2_75", "Softdrop Mass For Xqq/(Xqq+QCD) > .75", 40, 0, 200), "jM", "weight")
#	xt2_75 = xt2_75.Clone()
#	xt2_75.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .75")
#	xt2_75.SetXTitle("Softdrop Mass")
#	x2_75.Add(xt2_75)

	xt2_80 = Rdf_Xqq80.Histo1D(("xt2_80", "Softdrop Mass For Xqq/(Xqq+QCD) > .80", 40, 0, 200), "jM", "weight")
	xt2_80 = xt2_80.Clone()
	xt2_80.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .80")
	xt2_80.SetXTitle("Softdrop Mass")
	x2_80.Add(xt2_80)

	xt2_85 = Rdf_Xqq85.Histo1D(("xt2_85", "Softdrop Mass For Xqq/(Xqq+QCD) > .85", 40, 0, 200), "jM", "weight")
	xt2_85 = xt2_85.Clone()
	xt2_85.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .85")
	xt2_85.SetXTitle("Softdrop Mass")
	x2_85.Add(xt2_85)

	xt2_90 = Rdf_Xqq90.Histo1D(("xt2_90", "Softdrop Mass For Xqq/(Xqq+QCD) > .90", 40, 0, 200), "jM", "weight")
	xt2_90 = xt2_90.Clone()
	xt2_90.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .90")
	xt2_90.SetXTitle("Softdrop Mass")
	x2_90.Add(xt2_90)
	
	xt2_91 = Rdf_Xqq91.Histo1D(("xt2_91", "Softdrop Mass For Xqq/(Xqq+QCD) > .91", 40, 0, 200), "jM", "weight")
	xt2_91 = xt2_91.Clone()
	xt2_91.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .91")
	xt2_91.SetXTitle("Softdrop Mass")
	x2_91.Add(xt2_91)
	
	xt2_92 = Rdf_Xqq92.Histo1D(("xt2_92", "Softdrop Mass For Xqq/(Xqq+QCD) > .92", 40, 0, 200), "jM", "weight")
	xt2_92 = xt2_92.Clone()
	xt2_92.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .92")
	xt2_92.SetXTitle("Softdrop Mass")
	x2_92.Add(xt2_92)
	
	xt2_93 = Rdf_Xqq93.Histo1D(("xt2_93", "Softdrop Mass For Xqq/(Xqq+QCD) > .93", 40, 0, 200), "jM", "weight")
	xt2_93 = xt2_93.Clone()
	xt2_93.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .93")
	xt2_93.SetXTitle("Softdrop Mass")
	x2_93.Add(xt2_93)
	
	xt2_94 = Rdf_Xqq94.Histo1D(("xt2_94", "Softdrop Mass For Xqq/(Xqq+QCD) > .94", 40, 0, 200), "jM", "weight")
	xt2_94 = xt2_94.Clone()
	xt2_94.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .94")
	xt2_94.SetXTitle("Softdrop Mass")
	x2_94.Add(xt2_94)
	
	xt2_95 = Rdf_Xqq95.Histo1D(("xt2_95", "Softdrop Mass For Xqq/(Xqq+QCD) > .95", 40, 0, 200), "jM", "weight")
	xt2_95 = xt2_95.Clone()
	xt2_95.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .95")
	xt2_95.SetXTitle("Softdrop Mass")
	x2_95.Add(xt2_95)
	
	xt2_96 = Rdf_Xqq96.Histo1D(("xt2_96", "Softdrop Mass For Xqq/(Xqq+QCD) > .96", 40, 0, 200), "jM", "weight")
	xt2_96 = xt2_96.Clone()
	xt2_96.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .96")
	xt2_96.SetXTitle("Softdrop Mass")
	x2_96.Add(xt2_96)
	
	xt2_97 = Rdf_Xqq97.Histo1D(("xt2_97", "Softdrop Mass For Xqq/(Xqq+QCD) > .97", 40, 0, 200), "jM", "weight")
	xt2_97 = xt2_97.Clone()
	xt2_97.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .97")
	xt2_97.SetXTitle("Softdrop Mass")
	x2_97.Add(xt2_97)
	
	xt2_98 = Rdf_Xqq98.Histo1D(("xt2_98", "Softdrop Mass For Xqq/(Xqq+QCD) > .98", 40, 0, 200), "jM", "weight")
	xt2_98 = xt2_98.Clone()
	xt2_98.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .98")
	xt2_98.SetXTitle("Softdrop Mass")
	x2_98.Add(xt2_98)
	
	xt2_99 = Rdf_Xqq99.Histo1D(("xt2_99", "Softdrop Mass For Xqq/(Xqq+QCD) > .99", 40, 0, 200), "jM", "weight")
	xt2_99 = xt2_99.Clone()
	xt2_99.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .99")
	xt2_99.SetXTitle("Softdrop Mass")
	x2_99.Add(xt2_99)
	
#	xt6_10 = Rdf_AllQQ10.Histo1D(("xt6_10", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .10", 40, 0, 200), "jM", "weight")
#	xt6_10 = xt6_10.Clone()
#	xt6_10.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .10")
#	xt6_10.SetXTitle("Softdrop Mass")
#	x6_10.Add(xt6_10)

#	xt6_15 = Rdf_AllQQ15.Histo1D(("xt6_15", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .15", 40, 0, 200), "jM", "weight")
#	xt6_15 = xt6_15.Clone()
#	xt6_15.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .15")
#	xt6_15.SetXTitle("Softdrop Mass")
#	x6_15.Add(xt6_15)

#	xt6_20 = Rdf_AllQQ20.Histo1D(("xt6_20", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .20", 40, 0, 200), "jM", "weight")
#	xt6_20 = xt6_20.Clone()
#	xt6_20.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .20")
#	xt6_20.SetXTitle("Softdrop Mass")
#	x6_20.Add(xt6_20)

#	xt6_25 = Rdf_AllQQ25.Histo1D(("xt6_25", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .25", 40, 0, 200), "jM", "weight")
#	xt6_25 = xt6_25.Clone()
#	xt6_25.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .25")
#	xt6_25.SetXTitle("Softdrop Mass")
#	x6_25.Add(xt6_25)

#	xt6_30 = Rdf_AllQQ30.Histo1D(("xt6_30", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .30", 40, 0, 200), "jM", "weight")
#	xt6_30 = xt6_30.Clone()
#	xt6_30.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .30")
#	xt6_30.SetXTitle("Softdrop Mass")
#	x6_30.Add(xt6_30)

#	xt6_35 = Rdf_AllQQ35.Histo1D(("xt6_35", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .35", 40, 0, 200), "jM", "weight")
#	xt6_35 = xt6_35.Clone()
#	xt6_35.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .35")
#	xt6_35.SetXTitle("Softdrop Mass")
#	x6_35.Add(xt6_35)

#	xt6_40 = Rdf_AllQQ40.Histo1D(("xt6_40", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .40", 40, 0, 200), "jM", "weight")
#	xt6_40 = xt6_40.Clone()
#	xt6_40.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .40")
#	xt6_40.SetXTitle("Softdrop Mass")
#	x6_40.Add(xt6_40)

#	xt6_45 = Rdf_AllQQ45.Histo1D(("xt6_45", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .45", 40, 0, 200), "jM", "weight")
#	xt6_45 = xt6_45.Clone()
#	xt6_45.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .45")
#	xt6_45.SetXTitle("Softdrop Mass")
#	x6_45.Add(xt6_45)

#	xt6_50 = Rdf_AllQQ50.Histo1D(("xt6_50", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .50", 40, 0, 200), "jM", "weight")
#	xt6_50 = xt6_50.Clone()
#	xt6_50.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .50")
#	xt6_50.SetXTitle("Softdrop Mass")
#	x6_50.Add(xt6_50)

#	xt6_55 = Rdf_AllQQ55.Histo1D(("xt6_55", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .55", 40, 0, 200), "jM", "weight")
#	xt6_55 = xt6_55.Clone()
#	xt6_55.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .55")
#	xt6_55.SetXTitle("Softdrop Mass")
#	x6_55.Add(xt6_55)

#	xt6_60 = Rdf_AllQQ60.Histo1D(("xt6_60", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .60", 40, 0, 200), "jM", "weight")
#	xt6_60 = xt6_60.Clone()
#	xt6_60.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .60")
#	xt6_60.SetXTitle("Softdrop Mass")
#	x6_60.Add(xt6_60)

#	xt6_65 = Rdf_AllQQ65.Histo1D(("xt6_65", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .65", 40, 0, 200), "jM", "weight")
#	xt6_65 = xt6_65.Clone()
#	xt6_65.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .65")
#	xt6_65.SetXTitle("Softdrop Mass")
#	x6_65.Add(xt6_65)

#	xt6_70 = Rdf_AllQQ70.Histo1D(("xt6_70", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .70", 40, 0, 200), "jM", "weight")
#	xt6_70 = xt6_70.Clone()
#	xt6_70.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .70")
#	xt6_70.SetXTitle("Softdrop Mass")
#	x6_70.Add(xt6_70)

#	xt6_75 = Rdf_AllQQ75.Histo1D(("xt6_75", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .75", 40, 0, 200), "jM", "weight")
#	xt6_75 = xt6_75.Clone()
#	xt6_75.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .75")
#	xt6_75.SetXTitle("Softdrop Mass")
#	x6_75.Add(xt6_75)

	xt6_80 = Rdf_AllQQ80.Histo1D(("xt6_80", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .80", 40, 0, 200), "jM", "weight")
	xt6_80 = xt6_80.Clone()
	xt6_80.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .80")
	xt6_80.SetXTitle("Softdrop Mass")
	x6_80.Add(xt6_80)

	xt6_85 = Rdf_AllQQ85.Histo1D(("xt6_85", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .85", 40, 0, 200), "jM", "weight")
	xt6_85 = xt6_85.Clone()
	xt6_85.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .85")
	xt6_85.SetXTitle("Softdrop Mass")
	x6_85.Add(xt6_85)

	xt6_90 = Rdf_AllQQ90.Histo1D(("xt6_90", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .90", 40, 0, 200), "jM", "weight")
	xt6_90 = xt6_90.Clone()
	xt6_90.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .90")
	xt6_90.SetXTitle("Softdrop Mass")
	x6_90.Add(xt6_90)
	
	xt6_91 = Rdf_AllQQ91.Histo1D(("xt6_91", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .91", 40, 0, 200), "jM", "weight")
	xt6_91 = xt6_91.Clone()
	xt6_91.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .91")
	xt6_91.SetXTitle("Softdrop Mass")
	x6_91.Add(xt6_91)
	
	xt6_92 = Rdf_AllQQ92.Histo1D(("xt6_92", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .92", 40, 0, 200), "jM", "weight")
	xt6_92 = xt6_92.Clone()
	xt6_92.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .92")
	xt6_92.SetXTitle("Softdrop Mass")
	x6_92.Add(xt6_92)
	
	xt6_93 = Rdf_AllQQ93.Histo1D(("xt6_93", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .93", 40, 0, 200), "jM", "weight")
	xt6_93 = xt6_93.Clone()
	xt6_93.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .93")
	xt6_93.SetXTitle("Softdrop Mass")
	x6_93.Add(xt6_93)
	
	xt6_94 = Rdf_AllQQ94.Histo1D(("xt6_94", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .94", 40, 0, 200), "jM", "weight")
	xt6_94 = xt6_94.Clone()
	xt6_94.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .94")
	xt6_94.SetXTitle("Softdrop Mass")
	x6_94.Add(xt6_94)
	
	xt6_95 = Rdf_AllQQ95.Histo1D(("xt6_95", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .95", 40, 0, 200), "jM", "weight")
	xt6_95 = xt6_95.Clone()
	xt6_95.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .95")
	xt6_95.SetXTitle("Softdrop Mass")
	x6_95.Add(xt6_95)

	xt6_96 = Rdf_AllQQ96.Histo1D(("xt6_96", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .96", 40, 0, 200), "jM", "weight")
	xt6_96 = xt6_96.Clone()
	xt6_96.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .96")
	xt6_96.SetXTitle("Softdrop Mass")
	x6_96.Add(xt6_96)
	
	xt6_97 = Rdf_AllQQ97.Histo1D(("xt6_97", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .97", 40, 0, 200), "jM", "weight")
	xt6_97 = xt6_97.Clone()
	xt6_97.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .97")
	xt6_97.SetXTitle("Softdrop Mass")
	x6_97.Add(xt6_97)
	
	xt6_98 = Rdf_AllQQ98.Histo1D(("xt6_98", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .98", 40, 0, 200), "jM", "weight")
	xt6_98 = xt6_98.Clone()
	xt6_98.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .98")
	xt6_98.SetXTitle("Softdrop Mass")
	x6_98.Add(xt6_98)
	
	xt6_99 = Rdf_AllQQ99.Histo1D(("xt6_99", "Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .99", 40, 0, 200), "jM", "weight")
	xt6_99 = xt6_99.Clone()
	xt6_99.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .99")
	xt6_99.SetXTitle("Softdrop Mass")
	x6_99.Add(xt6_99)
	
	t2 = Rdf_Final.Histo1D(("t2", "Softdrop Mass", 40, 0, 200), "jM", "weight")
	t2 = t2.Clone()
	t2.SetTitle("Softdrop Mass")
	t2.SetXTitle("Softdrop Mass")
	h2.Add(t2)


	t4 = Rdf_Final.Histo1D(("t4", "Photon pT", 50, 0, 1000), "pPt", "weight")
	t4 = t4.Clone()
	t4.SetTitle("Photon pT")
	t4.SetXTitle("pT")
	h4.Add(t4)
		
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

	t8 = Rdf_Final.Histo1D(("t8", "Photon Eta", 70, -3.5, -3.5), "pEta", "weight")
	t8 = t8.Clone()
	t8.SetTitle("Photon Eta")
	t8.SetXTitle("Eta")
	h8.Add(t8)
		
		
#	j14 = Rdf_Final.Histo2D(("n2_soft", "N2 vs. Softdrop Mass", 50, 0, 0.5, 40, 0, 200), "N2", "jM", "weight")
#	j14 = j14.Clone()
#	h14.Add(j14)


	j16 = Rdf_Final.Histo2D(("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200), "Rho", "jM", "weight")
	j16 = j16.Clone()
	h16.Add(j16)
	

	j19 = Rdf_Final.Histo2D(("n2_pt", "N2 vs. Jet pT", 50, 0, 0.5, 40, 0, 2000), "N2", "jPt", "weight")
	j19 = j19.Clone()
	h19.Add(j19)


        j21_1 = Rdf_Final.Histo2D(("pt_soft_tot", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "weight")
        j21_1 = j21_1.Clone()
        h21_1.Add(j21_1)


        j30_w = Rdf_Final.Histo2D(("pt_soft_tot_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200), "jPt", "jM", "weight")
        j30_w = j30_w.Clone()
        h30_w.Add(j30_w)

        j33_w = Rdf_Final.Histo2D(("pt_soft_tot_wide4_wide", "Wide Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
        j33_w = j33_w.Clone()
        h33_w.Add(j33_w)


        j36_w = Rdf_Final.Histo2D(("pt_rho_tot_wide4_thin", "Total Jet pT vs. Rho", 15, widebins4, 28, -8, -1), "jPt", "Rho", "weight")
        j36_w = j36_w.Clone()
        h36_w.Add(j36_w)


        j39_w = Rdf_Final.Histo2D(("pt_soft_tot_wide5", "Total Jet pT vs. Softdrop Mass", 7, widebins5, 40, 0, 200), "jPt", "jM", "weight")
        j39_w = j39_w.Clone()
        h39_w.Add(j39_w)

#        j56 = Rdf_Final.Histo1D(("j56", "PuppiMET pT", 200, 0, 200), "PuppiMETpt", "weight")
#        j56 = j56.Clone()
#        h56.Add(j56)
#        j57 = Rdf_Final.Histo1D(("j57", "PuppiMET ET", 200, 0, 200), "PuppiMET_sumEt", "weight")
#        j57 = j57.Clone()
#        h57.Add(j57)

		
	print(str(nocut)+" Events Before Cuts in "+fname+" Sample")		
	print(str(npcut)+" Events After nPho>0 in in "+fname+" Sample")		
	print(str(njcut)+" Events After nFatJet>0 in "+fname+" Sample")		
	print(str(trigcut)+" Events After Trigger Cuts in "+fname+" Sample")		
	print(str(pcut)+" Events After Photon Cuts in "+fname+" Sample")		
	print(str(jcut)+" Events After Jet Cuts in "+fname+" Sample")		
	print(str(final)+" Events After Final Cuts in "+fname+" Sample")		
	

 	print("Total Number of Events: "+str(total_events))

	print("Cutflow Percentages: ")
	print("10% cut applied passed: "+str(ten_pass/total_events * 100)+"%")
	print("Trigger passed: "+str(trig_pass/total_events * 100)+"%")
	print("Num Pho and Num Jet passed: "+str(num_pass/total_events * 100)+"%")
	print("Photon pT passed: "+str(ppt_pass/total_events * 100)+"%")
	if sample[3] == "QCD" or sample[3] == "GJ":
		print("Direct Prompt Photon cut: "+str(dir_prompt_pass/total_events * 100)+"%")
	print("Jet pT passed: "+str(jpt_pass/total_events * 100)+"%")
	print("Photon Eta passed: "+str(peta_pass/total_events * 100)+"%")
	print("Jet Eta passed: "+str(jeta_pass/total_events * 100)+"%")
	print("Cut Based ID passed: "+str(pid_pass/total_events * 100)+"%")
	print("Jet ID passed: "+str(jid_pass/total_events * 100)+"%")
	print("Softdrop passed: "+str(jsoft_pass/total_events * 100)+"%")
	print("N2 passed: "+str(n2_pass/total_events * 100)+"%")
	print("Rho passed: "+str(rho_pass/total_events * 100)+"%")
	print("DeltaR passed: "+str(dR_pass/total_events * 100)+"%")
	

#	x1.SetTitle("ParticleNet Xqq Score")
#	x1.SetXTitle("Xqq Score")
#	ofile.WriteObject(x1, "Xqq")
	
#	x2_10.SetTitle("Softdrop Mass For Xqq > .10")
#	x2_10.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_10, "softdrop_xqq10")

#	x2_15.SetTitle("Softdrop Mass For Xqq > .15")
#	x2_15.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_15, "softdrop_xqq15")

#	x2_20.SetTitle("Softdrop Mass For Xqq > .20")
#	x2_20.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_20, "softdrop_xqq20")

#	x2_25.SetTitle("Softdrop Mass For Xqq > .25")
#	x2_25.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_25, "softdrop_xqq25")

#	x2_30.SetTitle("Softdrop Mass For Xqq > .30")
#	x2_30.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_30, "softdrop_xqq30")

#	x2_35.SetTitle("Softdrop Mass For Xqq > .35")
#	x2_35.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_35, "softdrop_xqq35")

#	x2_40.SetTitle("Softdrop Mass For Xqq > .40")
#	x2_40.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_40, "softdrop_xqq40")

#	x2_45.SetTitle("Softdrop Mass For Xqq > .45")
#	x2_45.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_45, "softdrop_xqq45")

#	x2_50.SetTitle("Softdrop Mass For Xqq > .50")
#	x2_50.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_50, "softdrop_xqq50")
	
	x1.SetTitle("ParticleNetMD Xqq Score")
	x1.SetXTitle("Xqq Score")
	ofile.WriteObject(x1, "Xqq")
	
	x1_1.SetTitle("ParticleNetMD Xqq/(Xqq+QCD) Score")
	x1_1.SetXTitle("Xqq/(Xqq+QCD) Score")
	ofile.WriteObject(x1_1, "Xqq_QCD")
	
	x3.SetTitle("ParticleNetMD QCD Score")
	x3.SetXTitle("QCD Score")
	ofile.WriteObject(x3, "QCD")
	
	x4.SetTitle("ParticleNetMD Xcc Score")
	x4.SetXTitle("Xcc Score")
	ofile.WriteObject(x4, "Xcc")
	
	x4_1.SetTitle("ParticleNetMD (Xqq+Xcc)/(Xqq+QCD) Score")
	x4_1.SetXTitle("(Xqq+Xcc)/(Xqq+QCD) Score")
	ofile.WriteObject(x4_1, "Xcc_QCD")
	
	x5.SetTitle("ParticleNetMD Xbb Score")
	x5.SetXTitle("Xbb Score")
	ofile.WriteObject(x5, "Xbb")
	
	x6.SetTitle("ParticleNetMD (Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD) Score")
	x6.SetXTitle("(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD) Score")
	ofile.WriteObject(x6, "AllQQ")
	
#	x2_10.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .10")
#	x2_10.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_10, "softdrop_xqq10")

#	x2_15.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .15")
#	x2_15.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_15, "softdrop_xqq15")

#	x2_20.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .20")
#	x2_20.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_20, "softdrop_xqq20")

#	x2_25.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .25")
#	x2_25.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_25, "softdrop_xqq25")

#	x2_30.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .30")
#	x2_30.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_30, "softdrop_xqq30")

#	x2_35.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .35")
#	x2_35.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_35, "softdrop_xqq35")

#	x2_40.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .40")
#	x2_40.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_40, "softdrop_xqq40")

#	x2_45.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .45")
#	x2_45.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_45, "softdrop_xqq45")

#	x2_50.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .50")
#	x2_50.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_50, "softdrop_xqq50")

#	x2_55.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .55")
#	x2_55.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_55, "softdrop_xqq55")

#	x2_60.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .60")
#	x2_60.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_60, "softdrop_xqq60")

#	x2_65.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .65")
#	x2_65.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_65, "softdrop_xqq65")

#	x2_70.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .70")
#	x2_70.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_70, "softdrop_xqq70")

#	x2_75.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .75")
#	x2_75.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x2_75, "softdrop_xqq75")

	x2_80.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .80")
	x2_80.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_80, "softdrop_xqq80")

	x2_85.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .85")
	x2_85.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_85, "softdrop_xqq85")

	x2_90.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .90")
	x2_90.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_90, "softdrop_xqq90")
	
	x2_91.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .91")
	x2_91.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_91, "softdrop_xqq91")
	
	x2_92.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .92")
	x2_92.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_92, "softdrop_xqq92")
	
	x2_93.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .93")
	x2_93.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_93, "softdrop_xqq93")
	
	x2_94.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .94")
	x2_94.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_94, "softdrop_xqq94")
	
	x2_95.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .95")
	x2_95.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_95, "softdrop_xqq95")
	
	x2_96.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .96")
	x2_96.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_96, "softdrop_xqq96")
	
	x2_97.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .97")
	x2_97.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_97, "softdrop_xqq97")
	
	x2_98.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .98")
	x2_98.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_98, "softdrop_xqq98")
	
	x2_99.SetTitle("Softdrop Mass For Xqq/(Xqq+QCD) > .99")
	x2_99.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x2_99, "softdrop_xqq99")
	
#	x6_10.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .10")
#	x6_10.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_10, "softdrop_AllQQ10")

#	x6_15.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .15")
#	x6_15.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_15, "softdrop_AllQQ15")

#	x6_20.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .20")
#	x6_20.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_20, "softdrop_AllQQ20")

#	x6_25.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .25")
#	x6_25.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_25, "softdrop_AllQQ25")

#	x6_30.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .30")
#	x6_30.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_30, "softdrop_AllQQ30")

#	x6_35.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .35")
#	x6_35.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_35, "softdrop_AllQQ35")

#	x6_40.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .40")
#	x6_40.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_40, "softdrop_AllQQ40")

#	x6_45.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .45")
#	x6_45.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_45, "softdrop_AllQQ45")

#	x6_50.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .50")
#	x6_50.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_50, "softdrop_AllQQ50")

#	x6_55.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .55")
#	x6_55.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_55, "softdrop_AllQQ55")

#	x6_60.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .60")
#	x6_60.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_60, "softdrop_AllQQ60")

#	x6_65.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .65")
#	x6_65.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_65, "softdrop_AllQQ65")

#	x6_70.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .70")
#	x6_70.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_70, "softdrop_AllQQ70")

#	x6_75.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .75")
#	x6_75.SetXTitle("Softdrop Mass")
#	ofile.WriteObject(x6_75, "softdrop_AllQQ75")

	x6_80.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .80")
	x6_80.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_80, "softdrop_AllQQ80")

	x6_85.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .85")
	x6_85.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_85, "softdrop_AllQQ85")

	x6_90.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .90")
	x6_90.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_90, "softdrop_AllQQ90")

	x6_91.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .91")
	x6_91.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_91, "softdrop_AllQQ91")

	x6_92.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .92")
	x6_92.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_92, "softdrop_AllQQ92")

	x6_93.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .93")
	x6_93.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_93, "softdrop_AllQQ93")

	x6_94.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .94")
	x6_94.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_94, "softdrop_AllQQ94")
	
	x6_95.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .95")
	x6_95.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_95, "softdrop_AllQQ95")

	x6_96.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .96")
	x6_96.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_96, "softdrop_AllQQ96")

	x6_97.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .97")
	x6_97.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_97, "softdrop_AllQQ97")

	x6_98.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .98")
	x6_98.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_98, "softdrop_AllQQ98")

	x6_99.SetTitle("Softdrop Mass For (Xcc+Xqq+Xbb)/(Xcc+Xqq+QCD+Xbb) > .99")
	x6_99.SetXTitle("Softdrop Mass")
	ofile.WriteObject(x6_99, "softdrop_AllQQ99")


	h2.SetTitle("Softdrop Mass")
	h2.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2, "softdrop")

	h4.SetTitle("Photon pT")
	h4.SetXTitle("Photon pT")
	ofile.WriteObject(h4, "photon_pt")

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

	h8.SetTitle("Photon Eta")
	h8.SetXTitle("Photon Eta")
	ofile.WriteObject(h8, "photon_eta")

	
#	h14.SetTitle("N2 vs. Softdrop Mass")
#	h14.SetXTitle("N2")
#	h14.SetYTitle("Softdrop Mass")
#	ofile.WriteObject(h14, "n2_soft")
	

	h16.SetTitle("Rho vs. Softdrop Mass")
	h16.SetXTitle("Rho")
	h16.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h16, "rho_soft")
	

	h19.SetTitle("N2 vs. Jet pT")
	h19.SetXTitle("N2")
	h19.SetYTitle("Jet pT")
	ofile.WriteObject(h19, "n2_pt")
	
	
	h21_1.SetTitle("Total Jet pT vs. Softdrop Mass")
	h21_1.SetXTitle("Jet pT")
	h21_1.SetYTitle("Softdrop Mass")
	ofile.WriteObject(h21_1, "jet_pt_soft_total")
	

        h30_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h30_w.SetYTitle("Softdrop Mass")
        h30_w.SetXTitle("Jet pT")
        ofile.WriteObject(h30_w, "jet_pt_soft_total_wide4")

        h33_w.SetTitle("Wide Total Jet pT vs. Softdrop Mass")
        h33_w.SetYTitle("Softdrop Mass")
        h33_w.SetXTitle("Jet pT")
        ofile.WriteObject(h33_w, "jet_pt_soft_total_wide4_wide")

        h36_w.SetTitle("Total Jet pT vs. Rho")
        h36_w.SetYTitle("Rho")
        h36_w.SetXTitle("Jet pT")
        ofile.WriteObject(h36_w, "jet_pt_rho_total_wide4_thin")


        h39_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h39_w.SetYTitle("Softdrop Mass")
        h39_w.SetXTitle("Jet pT")
        ofile.WriteObject(h39_w, "jet_pt_soft_total_wide5")

#        h56.SetTitle("PuppiMET pT")
#        h56.SetXTitle("pT")
#        ofile.WriteObject(h56, "PuppiMETPT")

#        h57.SetTitle("PuppiMET Et")
#        h57.SetXTitle("Et")
#        ofile.WriteObject(h57, "ak4_btag")



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

	cut_vals = TH1F("cut_vals", "Cut Values", 45, 0, 45)
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
	cut_vals.SetBinContent(18,dir_prompt_pass*weighting)
	cut_vals.SetBinContent(20,Xqq80*weighting)
	cut_vals.SetBinContent(21,Xqq85*weighting)
	cut_vals.SetBinContent(22,Xqq90*weighting)
	cut_vals.SetBinContent(23,Xqq91*weighting)
	cut_vals.SetBinContent(24,Xqq92*weighting)
	cut_vals.SetBinContent(25,Xqq93*weighting)
	cut_vals.SetBinContent(26,Xqq94*weighting)
	cut_vals.SetBinContent(27,Xqq95*weighting)
	cut_vals.SetBinContent(28,Xqq96*weighting)
	cut_vals.SetBinContent(29,Xqq97*weighting)
	cut_vals.SetBinContent(30,Xqq98*weighting)
	cut_vals.SetBinContent(31,Xqq99*weighting)
	cut_vals.SetBinContent(32,AllQQ80*weighting)
	cut_vals.SetBinContent(33,AllQQ85*weighting)
	cut_vals.SetBinContent(34,AllQQ90*weighting)
	cut_vals.SetBinContent(35,AllQQ91*weighting)
	cut_vals.SetBinContent(36,AllQQ92*weighting)
	cut_vals.SetBinContent(37,AllQQ93*weighting)
	cut_vals.SetBinContent(38,AllQQ94*weighting)
	cut_vals.SetBinContent(39,AllQQ95*weighting)
	cut_vals.SetBinContent(40,AllQQ96*weighting)
	cut_vals.SetBinContent(41,AllQQ97*weighting)
	cut_vals.SetBinContent(42,AllQQ98*weighting)
	cut_vals.SetBinContent(43,AllQQ99*weighting)
	
	
	ofile.Write()
