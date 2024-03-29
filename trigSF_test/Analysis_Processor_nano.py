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



def DataPro(sample, fname, cut_hist, percentage=20):

	gROOT.SetBatch(True)

	ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/trigSF_test/output/RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()


	rho_bins = cut_hist.GetNbinsX()
	pt_bins = cut_hist.GetNbinsY()

		

	h1 = TH1F("h1", "N2", 50, 0, 0.5)
	h2 = TH1F("h2", "Softdrop Mass", 40, 0, 200)
	h2_1 = TH1F("h2_1", "Thin Softdrop Mass", 100, 0, 200)
	h2_2 = TH1F("h2_2", "Thin (Uncorrected) Softdrop Mass", 100, 0, 200)
	h4 = TH1F("h4", "Photon pT", 100, 0, 2000)
	h5 = TH1F("h5", "Jet pT", 40, 0, 2000)
        h5_1 = TH1F("h5_1", "Thin Jet pT", 2000, 0, 2000)
	h6 = TH1F("h6", "Jet Eta", 70, -3.5, 3.5)
	h7 = TH1F("h7", "Rho", 28, -8, -1)
	h8 = TH1F("h8", "Photon Eta", 70, -3.5, 3.5)
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

        ROOT.gInterpreter.Declare("Double_t widebins4[16] = {0, 120, 130, 145, 160, 180, 200, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
        h29_w = TH2F("jet_pt_soft_pass_wide4", "Passing Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200)
        h30_w = TH2F("jet_pt_soft_total_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200)
        h31_w = TH2F("jet_pt_soft_fail_wide4", "Failing Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200)

        h32_w = TH2F("jet_pt_soft_pass_wide4_wide", "Wide Passing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        h33_w = TH2F("jet_pt_soft_total_wide4_wide", "Wide Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)
        h34_w = TH2F("jet_pt_soft_fail_wide4_wide", "Wide Failing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200)


        h35_w = TH2F("jet_pt_rho_pass_wide4_thin", "Passing Jet pT vs. Rho", 15, widebins4, 28, -8, -1)
        h36_w = TH2F("jet_pt_rho_total_wide4_thin", "Total Jet pT vs. Rho", 15, widebins4, 28, -8, -1)
        h37_w = TH2F("jet_pt_rho_fail_wide4_thin", "Failing Jet pT vs. Rho", 15, widebins4, 28, -8, -1)

        ROOT.gInterpreter.Declare("Double_t widebins5[20] = {0, 120, 130, 140, 150, 160, 170, 180, 190, 200, 225, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
      	h38_w = TH2F("jet_pt_soft_pass_wide5_wide", "Passing Jet pT vs. Softdrop Mass", 19, widebins5, 40, 0, 200)
        h39_w = TH2F("jet_pt_soft_total_wide5_wide", "Total Jet pT vs. Softdrop Mass", 19, widebins5, 40, 0, 200)
        h40_w = TH2F("jet_pt_soft_fail_wide5_wide", "Failing Jet pT vs. Softdrop Mass", 19, widebins5, 40, 0, 200)
        
	ROOT.gInterpreter.Declare("Double_t widebins6[18] = {0, 120, 130, 140, 155, 170, 185, 200, 220, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")
      	h41_w = TH2F("jet_pt_soft_pass_wide6_wide", "Passing Jet pT vs. Softdrop Mass", 17, widebins6, 40, 0, 200)
        h42_w = TH2F("jet_pt_soft_total_wide6_wide", "Total Jet pT vs. Softdrop Mass", 17, widebins6, 40, 0, 200)
        h43_w = TH2F("jet_pt_soft_fail_wide6_wide", "Failing Jet pT vs. Softdrop Mass", 17, widebins6, 40, 0, 200)
	
	ROOT.gInterpreter.Declare("Double_t widebins7[11] = {0, 120, 140, 170, 220, 300, 400, 550, 700, 1200, 2000};")
      	h44_w = TH2F("jet_pt_soft_pass_wide7_wide", "Passing Jet pT vs. Softdrop Mass", 10, widebins7, 40, 0, 200)
        h45_w = TH2F("jet_pt_soft_total_wide7_wide", "Total Jet pT vs. Softdrop Mass", 10, widebins7, 40, 0, 200)
        h46_w = TH2F("jet_pt_soft_fail_wide7_wide", "Failing Jet pT vs. Softdrop Mass", 10, widebins7, 40, 0, 200)
	ROOT.gInterpreter.Declare("Double_t widebins8[9] = {0, 120, 170, 220, 300, 400, 700, 1200, 2000};")
      	h47_w = TH2F("jet_pt_soft_pass_wide8_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins8, 40, 0, 200)
        h48_w = TH2F("jet_pt_soft_total_wide8_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins8, 40, 0, 200)
        h49_w = TH2F("jet_pt_soft_fail_wide8_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins8, 40, 0, 200)
	ROOT.gInterpreter.Declare("Double_t widebins9[13] = {0, 120, 145, 170, 195, 220, 250, 300, 400, 500, 700, 1200, 2000};")
      	h50_w = TH2F("jet_pt_soft_pass_wide9_wide", "Passing Jet pT vs. Softdrop Mass", 12, widebins9, 40, 0, 200)
        h51_w = TH2F("jet_pt_soft_total_wide9_wide", "Total Jet pT vs. Softdrop Mass", 12, widebins9, 40, 0, 200)
        h52_w = TH2F("jet_pt_soft_fail_wide9_wide", "Failing Jet pT vs. Softdrop Mass", 12, widebins9, 40, 0, 200)
	
	ROOT.gInterpreter.Declare("Double_t widebins10[9] = {0, 120, 170, 220, 300, 400, 500, 1200, 2000};")
      	h53_w = TH2F("jet_pt_soft_pass_wide10_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins10, 40, 0, 200)
        h54_w = TH2F("jet_pt_soft_total_wide10_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins10, 40, 0, 200)
        h55_w = TH2F("jet_pt_soft_fail_wide10_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins10, 40, 0, 200)
	
	ROOT.gInterpreter.Declare("Double_t widebins11[11] = {0, 120, 145, 170, 195, 220, 255, 360, 500, 1000, 2000};")
      	h56_w = TH2F("jet_pt_soft_pass_wide11_wide", "Passing Jet pT vs. Softdrop Mass", 10, widebins11, 40, 0, 200)
        h57_w = TH2F("jet_pt_soft_total_wide11_wide", "Total Jet pT vs. Softdrop Mass", 10, widebins11, 40, 0, 200)
        h58_w = TH2F("jet_pt_soft_fail_wide11_wide", "Failing Jet pT vs. Softdrop Mass", 10, widebins11, 40, 0, 200)

        h50 = TH1F("ak4_eta", "AK4 Jet Eta", 70, -3.5, 3.5)
        h51 = TH1F("ak4_phi", "AK4 Jet Phi", 80, -4, 4)
        h52 = TH1F("ak4_njet", "AK4 nJet", 25, 0, 25)
        h53 = TH1F("ak4_btag", "AK4 BTag", 200, -1, 1)

        h54 = TH1F("METPT", "MET pT", 200, 0, 200)
        h55 = TH1F("MET_Et", "MET ET", 200, 0, 200)
        h56 = TH1F("PuppiMETPT", "PuppiMET pT", 200, 0, 200)
        h57 = TH1F("PuppiMET_Et", "PuppiMET ET", 200, 0, 200)


        #With PUPPI MET cut
        h58 = TH1F("ak4_eta_met", "AK4 Jet Eta with PUPPI MET cut", 70, -3.5, 3.5)
        h59 = TH1F("ak4_phi_met", "AK4 Jet Phi with PUPPI MET cut", 80, -4, 4)
        h60 = TH1F("ak4_njet_met", "AK4 nJet with PUPPI MET cut", 25, 0, 25)
        h61 = TH1F("ak4_btag_met", "AK4 BTag with PUPPI MET cut", 200, -1, 1)
	
	h65 = TH2F("eta_pho_pt", "Eta vs. Photon pT", 70, -3.5, 3.5, 100, 0, 2000)

#	h70 = TH1F("run", "Run Number", 20000, 310000, 330000)
#	h71 = TH1F("event", "Event", 100000, 0, 1000000000)
#	h72 = TH1F("lumiBlock", "Luminosity Block", 1000, 0, 1000)

	#Photon pT Spike
#	h70_1 = TH1F("run_spike", "Run Number in Photon pT Spike", 20000, 310000, 330000)
#	h71_1 = TH1F("event_spike", "Event in Photon pT Spike", 100000, 0, 1000000000)
#	h72_1 = TH1F("lumiBlock_spike", "Luminosity Block in Photon pT Spike", 1000, 0, 1000)
	
#	h75 = TH1F("tau32", "Tau32", 150, 0, 1.5)

	h80 = TH1F("HT", "AK4 HT", 1000, 0, 5000)
	h81 = TH1F("HT_AK8", "AK8 HT", 1000, 0, 5000)
	
	h90 = TH1F("h90", "AK4 Jet pT", 200, 0, 2000)

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

	#Photon ID SF (Testing)
#	pho_SF_bins = np.array([120, 125, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000])
#	ROOT.gInterpreter.Declare("Double_t pho_bins[28] = {120, 125, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 260, 280, 300, 340, 380, 420, 460, 500, 580, 660, 740, 820, 900, 1000};")
#	pho_SF_content = np.array([0.932,0.953,0.963,0.963,0.956,0.984,0.951,0.962,0.967,0.990,0.972,0.985,0.991,0.990,0.991,0.995,0.992,0.996,0.990,0.994,1.0,1.0,0.987,1.0,1.0,1.0,1.0])
#	photonID_SF = TH1F("phoID_SF", "Photon ID SF", 27, pho_bins)
#	for b,content in enumerate(pho_SF_content):
#		print("Setting phoID_SF Bin #"+str(b+1)+" to value: "+str(content))
#		photonID_SF.SetBinContent(b+1, content)

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

	
	
	if sample[3] == "data": #Take 10% of Data
                Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0")
                ten_pass += float(Rdf_noCut.Count().GetValue())
	if sample[2] == 1: 
		Rdf_noCut = Rdf_noCut.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 >0.0)")
	elif sample[2] == 2:
		Rdf_noCut = Rdf_noCut.Filter("(HLT_Photon200 >0.0)")

	trig_pass += float(Rdf_noCut.Count().GetValue())

	Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
	npcut += float(Rdf_PreSel.Count().GetValue())

	Rdf_PreSel = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")
	njcut += float(Rdf_PreSel.Count().GetValue())
	num_pass += float(Rdf_PreSel.Count().GetValue())

	Rdf_cflow = Rdf_PreSel.Filter("PPT(Photon_pt, nPhoton)")
	ppt_pass += float(Rdf_cflow.Count().GetValue())
	#Direct Prompt Photon CutFlow
	if sample[3] == "GJ":
		Rdf_cflow = Rdf_cflow.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
		dir_prompt_pass += float(Rdf_cflow.Count().GetValue())
	if sample[3] == "QCD":
		Rdf_cflow = Rdf_cflow.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
		dir_prompt_pass += float(Rdf_cflow.Count().GetValue())


	Rdf_cflow = Rdf_cflow.Filter("JPT(selectedPatJetsAK8PFPuppi_pt_nom, nselectedPatJetsAK8PFPuppi)")
	jpt_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("PETA(Photon_pt, Photon_eta, nPhoton)")
	peta_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JETA(selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, nselectedPatJetsAK8PFPuppi)")
	jeta_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("PID(Photon_pt, Photon_eta, Photon_cutBased, nPhoton)")
	pid_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JID(selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId, nselectedPatJetsAK8PFPuppi)")
	jid_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JSOFT(selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId,selectedPatJetsAK8PFPuppi_msoftdrop_raw, nselectedPatJetsAK8PFPuppi)")
	jsoft_pass += float(Rdf_cflow.Count().GetValue())
       
		
	Rdf_cflow = Rdf_cflow.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_msoftdrop_raw, selectedPatJetsAK8PFPuppi_jetId)")
	Rdf_cflow = Rdf_cflow.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

#	Rdf_cflow = Rdf_cflow.Filter("selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
	Rdf_cflow = Rdf_cflow.Filter("selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
	n2_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Define("Rho", "rho(selectedPatJetsAK8PFPuppi_pt_nom[jIndex], selectedPatJetsAK8PFPuppi_msoftdrop_raw[jIndex])")
	Rdf_cflow = Rdf_cflow.Filter("Rho > -7 && Rho < -2")
		
	rho_pass += float(Rdf_cflow.Count().GetValue())


	
	#ROOT.gInterpreter.Declare('#include "Help.h"')
	Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_msoftdrop_raw, selectedPatJetsAK8PFPuppi_jetId)")
	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")
	
	#Direct Prompt Filter
	if sample[3] == "GJ":
		Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	if sample[3] == "QCD":
		Rdf_PreSel = Rdf_PreSel.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")
	#Trigger Filter
	if sample[2] == 1: 
		Rdf_PreSel = Rdf_PreSel.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 >0.0)")
	elif sample[2] == 2:
		Rdf_PreSel = Rdf_PreSel.Filter("(HLT_Photon200 >0.0)")

	trigcut += float(Rdf_PreSel.Count().GetValue())

	Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	pcut += float(Rdf.Count().GetValue())
	
		
	Rdf = Rdf.Filter("jIndex >= 0")
	jcut += float(Rdf.Count().GetValue())
	
	
	#PreSel Cuts
#	Rdf_PreSel = Rdf_PreSel.Filter("pIndex >= 0")
#	Rdf_PreSel = Rdf_PreSel.Filter("jIndex >= 0")
	
        #PreSel Values defined
#        Rdf_PreSel = Rdf_PreSel.Define("jM_uncorr", "selectedPatJetsAK8PFPuppi_msoftdrop_raw[jIndex]")
 #       Rdf_PreSel = Rdf_PreSel.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
  #      Rdf_PreSel = Rdf_PreSel.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
   #     Rdf_PreSel = Rdf_PreSel.Define("jPt", "selectedPatJetsAK8PFPuppi_pt_nom[jIndex]")
    #    Rdf_PreSel = Rdf_PreSel.Define("pPt", "Photon_pt[pIndex]")
     #   Rdf_PreSel = Rdf_PreSel.Define("pEta", "Photon_eta[pIndex]")
      #  Rdf_PreSel = Rdf_PreSel.Define("pPhi", "Photon_phi[pIndex]")
#        Rdf_PreSel = Rdf_PreSel.Define("N2", "selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
#        Rdf_PreSel = Rdf_PreSel.Define("N2", "selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
 #       Rdf_PreSel = Rdf_PreSel.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
  #      Rdf_PreSel = Rdf_PreSel.Define("Rho", "rho(jPt, jM)")
#	Rdf_PreSel = Rdf_PreSel.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
 #       if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
  #              Rdf_PreSel = Rdf_PreSel.Define("xs_lumi", sample[1])
   #             Rdf_PreSel = Rdf_PreSel.Define("weight", "xs_lumi*puWeight")
    #    elif sample[3] == "data":
     #           Rdf_PreSel = Rdf_PreSel.Define("weight", sample[1])
#	Rdf_PreSel = Rdf_PreSel.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2")




#	Rdf = Rdf.Define("jM_uncorr", "selectedPatJetsAK8PFPuppi_msoftdrop_raw[jIndex]")
	Rdf = Rdf.Define("jM_uncorr", "selectedPatJetsAK8PFPuppi_msoftdrop_raw[jIndex]*selectedPatJetsAK8PFPuppi_corr_JER[jIndex]")
	Rdf = Rdf.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
	Rdf = Rdf.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
	Rdf = Rdf.Define("jPt", "selectedPatJetsAK8PFPuppi_pt_nom[jIndex]")
	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
#	Rdf = Rdf.Define("N2", "selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
	Rdf = Rdf.Define("N2", "selectedPatJetsAK8PFPuppi_n2b1[jIndex]")
	Rdf = Rdf.Define("jID", "selectedPatJetsAK8PFPuppi_jetId[jIndex]")
	Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
	Rdf = Rdf.Define("n2ddt", "ddt(jPt, jM, N2)")

	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")

	Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
        Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")

        Rdf = Rdf.Define("nj4", "nJet")
        Rdf = Rdf.Define("ak4_nomatch", "ak4_match(nj4, Jet_eta, Jet_phi, jEta, jPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that do NOT match the boosted AK8 jet sorted by btag score

        Rdf = Rdf.Define("j4eta", "ak4_ret(ak4_nomatch, Jet_eta)[0]")
        Rdf = Rdf.Define("j4phi", "ak4_ret(ak4_nomatch, Jet_phi)[0]")
        Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_nomatch, Jet_btagDeepFlavB)[0]")

        Rdf = Rdf.Define("METpt", "MET_pt")
        Rdf = Rdf.Define("MET_Et", "MET_sumEt")
        Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")
        Rdf = Rdf.Define("PuppiMET_Et", "PuppiMET_sumEt")
        
#	Rdf = Rdf.Define("tau32", "selectedPatJetsAK8PFPuppi_NjettinessAK8Puppi_tau3[jIndex]/selectedPatJetsAK8PFPuppi_NjettinessAK8Puppi_tau2[jIndex]")
	Rdf = Rdf.Define("jHT", "HT(Jet_pt, Jet_eta)")
	Rdf = Rdf.Define("jHT_AK8", "HT_AK8(selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta)")
	
	Rdf = Rdf.Define("jPt_AK4", "Jet_pt[0]")
        
	#For Photon pT Spike Testing
	Rdf = Rdf.Define("Run", "run")
        Rdf = Rdf.Define("Event", "event")
        Rdf = Rdf.Define("LumiBlock", "luminosityBlock")
	
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
                Rdf = Rdf.Define("xs_lumi", sample[1])
		print("test1")
		Rdf = Rdf.Define("photonID_SF", "phoID_SF(pPt)")
		print("test2")
                Rdf = Rdf.Define("weight", "xs_lumi*puWeight*photonID_SF")
		print("test 2.5")
		
		#dis = Rdf.Display()
		#print(dis)
		print("test3")
		
        elif sample[3] == "data":
                Rdf = Rdf.Define("weight", sample[1])
		

	

	Rdf_Final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2")
	dR_pass += float(Rdf_Final.Count().GetValue())
        
	print("test4")

	#Plot MET before MET cut
	j54 = Rdf_Final.Histo1D(("j54", "MET pT", 200, 0, 200), "METpt", "weight")
        j54 = j54.Clone()
        h54.Add(j54)
	print("test5")
        j55 = Rdf_Final.Histo1D(("j55", "MET ET", 200, 0, 200), "MET_Et", "weight")
        j55 = j55.Clone()
        h55.Add(j55)
        j56 = Rdf_Final.Histo1D(("j56", "PuppiMET pT", 200, 0, 200), "PuppiMETpt", "weight")
        j56 = j56.Clone()
        h56.Add(j56)
        j57 = Rdf_Final.Histo1D(("j57", "PuppiMET ET", 200, 0, 200), "PuppiMET_sumEt", "weight")
        j57 = j57.Clone()
        h57.Add(j57)

        Rdf_MET = Rdf_Final.Filter("PuppiMETpt < 75") #Additional MET cut for btag testing
        Rdf_Final = Rdf_Final.Filter("PuppiMETpt < 75 && jBtag < 0.049")

        final += float(Rdf_Final.Count().GetValue())
#	print(final)	

	#Photon pT Spike
	Rdf_spike = Rdf_Final.Filter("pPt > 650 && pPt < 690")

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


	t4 = Rdf_Final.Histo1D(("t4", "Photon pT", 100, 0, 2000), "pPt", "weight")
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
	
	q2 = Rdf_Pass.Histo1D(("q2", "Passing Photon pT", 100, 0, 2000), "pPt", "weight")
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
		
	q5 = Rdf_Pass.Histo1D(("q5", "Passing Photon Eta", 70, -3.5, 3.5), "pEta", "weight")
	q5 = q5.Clone()
	q5.SetTitle("Passing Photon Eta")
	q5.SetXTitle("Photon Eta")
	p5.Add(q5)
		
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
		
	u2 = Rdf_Fail.Histo1D(("u2", "Failing Photon pT", 100, 0, 2000), "pPt", "weight")
	u2 = u2.Clone()
#		u2.Scale(1/9.0)
	u2.SetTitle("Failing Photon pT")
	u2.SetXTitle("Photon pT")
	f2.Add(u2)
		
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
		
	u5 = Rdf_Fail.Histo1D(("u5", "Failing Photon Eta", 70, -3.5, 3.5), "pEta", "weight")
	u5 = u5.Clone()
#		u5.Scale(1/9.0)
	u5.SetTitle("Failing Photon Eta")
	u5.SetXTitle("Photon Eta")
	f5.Add(u5)
		
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


        j29_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide4", "Passing Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200), "jPt", "jM", "weight")
        j29_w = j29_w.Clone()
        h29_w.Add(j29_w)

        j30_w = Rdf_Final.Histo2D(("pt_soft_tot_wide4", "Total Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200), "jPt", "jM", "weight")
        j30_w = j30_w.Clone()
        h30_w.Add(j30_w)

        j31_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide4", "Failing Jet pT vs. Softdrop Mass", 15, widebins4, 200, 0, 200), "jPt", "jM", "weight")
        j31_w = j31_w.Clone()
        h31_w.Add(j31_w)
	
        j32_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide4_wide", "Wide Passing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
        j32_w = j32_w.Clone()
        h32_w.Add(j32_w)

        j33_w = Rdf_Final.Histo2D(("pt_soft_tot_wide4_wide", "Wide Total Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
        j33_w = j33_w.Clone()
        h33_w.Add(j33_w)

        j34_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide4_wide", "Wide Failing Jet pT vs. Softdrop Mass", 15, widebins4, 40, 0, 200), "jPt", "jM", "weight")
        j34_w = j34_w.Clone()
        h34_w.Add(j34_w)

        j35_w = Rdf_Pass.Histo2D(("pt_rho_pass_wide4_thin", "Passing Jet pT vs. Rho", 15, widebins4, 28, -8, -1), "jPt", "Rho", "weight")
        j35_w = j35_w.Clone()
        h35_w.Add(j35_w)

        j36_w = Rdf_Final.Histo2D(("pt_rho_tot_wide4_thin", "Total Jet pT vs. Rho", 15, widebins4, 28, -8, -1), "jPt", "Rho", "weight")
        j36_w = j36_w.Clone()
        h36_w.Add(j36_w)

        j37_w = Rdf_Fail.Histo2D(("pt_rho_pass_wide4_thin", "Failing Jet pT vs. Rho", 15, widebins4, 28, -8, -1), "jPt", "Rho", "weight")
        j37_w = j37_w.Clone()
        h37_w.Add(j37_w)
	
        j38_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide5_wide", "Passing Jet pT vs. Softdrop Mass", 19, widebins5, 200, 0, 200), "jPt", "jM", "weight")
        j38_w = j38_w.Clone()
        h38_w.Add(j38_w)

        j39_w = Rdf_Final.Histo2D(("pt_soft_tot_wide5_wide", "Total Jet pT vs. Softdrop Mass", 19, widebins5, 200, 0, 200), "jPt", "jM", "weight")
        j39_w = j39_w.Clone()
        h39_w.Add(j39_w)

        j40_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide5_wide", "Failing Jet pT vs. Softdrop Mass", 19, widebins5, 200, 0, 200), "jPt", "jM", "weight")
        j40_w = j40_w.Clone()
        h40_w.Add(j40_w)
        
	j41_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide", "Passing Jet pT vs. Softdrop Mass", 17, widebins6, 200, 0, 200), "jPt", "jM", "weight")
        j41_w = j41_w.Clone()
        h41_w.Add(j41_w)

        j42_w = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide", "Total Jet pT vs. Softdrop Mass", 17, widebins6, 200, 0, 200), "jPt", "jM", "weight")
        j42_w = j42_w.Clone()
        h42_w.Add(j42_w)

        j43_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide", "Failing Jet pT vs. Softdrop Mass", 17, widebins6, 200, 0, 200), "jPt", "jM", "weight")
        j43_w = j43_w.Clone()
        h43_w.Add(j43_w)
        
	j44_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide7_wide", "Passing Jet pT vs. Softdrop Mass", 10, widebins7, 200, 0, 200), "jPt", "jM", "weight")
        j44_w = j44_w.Clone()
        h44_w.Add(j44_w)

        j45_w = Rdf_Final.Histo2D(("pt_soft_tot_wide7_wide", "Total Jet pT vs. Softdrop Mass", 10, widebins7, 200, 0, 200), "jPt", "jM", "weight")
        j45_w = j45_w.Clone()
        h45_w.Add(j45_w)

        j46_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide7_wide", "Failing Jet pT vs. Softdrop Mass", 10, widebins7, 200, 0, 200), "jPt", "jM", "weight")
        j46_w = j46_w.Clone()
        h46_w.Add(j46_w)
        j47_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide8_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins8, 200, 0, 200), "jPt", "jM", "weight")
        j47_w = j47_w.Clone()
        h47_w.Add(j47_w)

        j48_w = Rdf_Final.Histo2D(("pt_soft_tot_wide8_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins8, 200, 0, 200), "jPt", "jM", "weight")
        j48_w = j48_w.Clone()
        h48_w.Add(j48_w)

        j49_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide8_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins8, 200, 0, 200), "jPt", "jM", "weight")
        j49_w = j49_w.Clone()
        h49_w.Add(j49_w)
        
	j50_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide9_wide", "Passing Jet pT vs. Softdrop Mass", 12, widebins9, 200, 0, 200), "jPt", "jM", "weight")
        j50_w = j50_w.Clone()
        h50_w.Add(j50_w)

        j51_w = Rdf_Final.Histo2D(("pt_soft_tot_wide9_wide", "Total Jet pT vs. Softdrop Mass", 12, widebins9, 200, 0, 200), "jPt", "jM", "weight")
        j51_w = j51_w.Clone()
        h51_w.Add(j51_w)

        j52_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide9_wide", "Failing Jet pT vs. Softdrop Mass", 12, widebins9, 200, 0, 200), "jPt", "jM", "weight")
        j52_w = j52_w.Clone()
        h52_w.Add(j52_w)
	
	j53_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide10_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins10, 200, 0, 200), "jPt", "jM", "weight")
        j53_w = j53_w.Clone()
        h53_w.Add(j53_w)

        j54_w = Rdf_Final.Histo2D(("pt_soft_tot_wide10_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins10, 200, 0, 200), "jPt", "jM", "weight")
        j54_w = j54_w.Clone()
        h54_w.Add(j54_w)

        j55_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide10_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins10, 200, 0, 200), "jPt", "jM", "weight")
        j55_w = j55_w.Clone()
        h55_w.Add(j55_w)
	
	j56_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide11_wide", "Passing Jet pT vs. Softdrop Mass", 10, widebins11, 200, 0, 200), "jPt", "jM", "weight")
        j56_w = j56_w.Clone()
        h56_w.Add(j56_w)

        j57_w = Rdf_Final.Histo2D(("pt_soft_tot_wide11_wide", "Total Jet pT vs. Softdrop Mass", 10, widebins11, 200, 0, 200), "jPt", "jM", "weight")
        j57_w = j57_w.Clone()
        h57_w.Add(j57_w)

        j58_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide11_wide", "Failing Jet pT vs. Softdrop Mass", 10, widebins11, 200, 0, 200), "jPt", "jM", "weight")
        j58_w = j58_w.Clone()
        h58_w.Add(j58_w)

        j50 = Rdf_Final.Histo1D(("j50", "AK4 Jet Eta", 70, -3.5, 3.5), "j4eta", "weight")
        j50 = j50.Clone()
        h50.Add(j50)
        j51 = Rdf_Final.Histo1D(("j51", "AK4 Jet Phi", 80, -4, 4), "j4phi", "weight")
        j51 = j51.Clone()
        h51.Add(j51)
        j52 = Rdf_Final.Histo1D(("j52", "AK4 nJet", 25, 0, 25), "nJet", "weight")
        j52 = j52.Clone()
        h52.Add(j52)
        j53 = Rdf_Final.Histo1D(("j53", "AK4 BTag", 200, -1, 1), "jBtag", "weight")
        j53 = j53.Clone()
        h53.Add(j53)


        j58 = Rdf_MET.Histo1D(("j58", "AK4 Jet Eta with PUPPI MET cut", 70, -3.5, 3.5), "j4eta", "weight")
        j58 = j58.Clone()
        h58.Add(j58)
        j59 = Rdf_MET.Histo1D(("j59", "AK4 Jet Phi with PUPPI MET cut", 80, -4, 4), "j4phi", "weight")
        j59 = j59.Clone()
        h59.Add(j59)
        j60 = Rdf_MET.Histo1D(("j60", "AK4 nJet with PUPPI MET cut", 25, 0, 25), "nJet", "weight")
        j60 = j60.Clone()
        h60.Add(j60)
        j61 = Rdf_MET.Histo1D(("j61", "AK4 BTag with PUPPI MET cut", 200, -1, 1), "jBtag", "weight")
        j61 = j61.Clone()
        h61.Add(j61)
	
        j65 = Rdf_Final.Histo2D(("j65", "Eta vs. Photon pT", 70, -3.5, 3.5, 100, 0, 2000), "pEta", "jPt", "weight")
	j65 = j65.Clone()
	h65.Add(j65)
        
	
	
	
	
#	j70 = Rdf_Final.Histo1D(("j70", "Run Number", 20000, 310000, 330000), "Run", "weight")
#        j70 = j70.Clone()
#        h70.Add(j70)
	
#	j71 = Rdf_Final.Histo1D(("j71", "Event", 100000, 0, 1000000000), "Event", "weight")
#        j71 = j71.Clone()
#        h71.Add(j71)
	
#	j72 = Rdf_Final.Histo1D(("j72", "Luminosity Block", 1000, 0, 1000), "LumiBlock", "weight")
#        j72 = j72.Clone()
#        h72.Add(j72)
	
#	j70_1 = Rdf_spike.Histo1D(("j70_1", "Run Number in Photon pT Spike", 20000, 310000, 330000), "Run", "weight")
 #       j70_1 = j70_1.Clone()
  #      h70_1.Add(j70_1)
	
#	j71_1 = Rdf_spike.Histo1D(("j71_1", "Event in Photon pT Spike", 100000, 0, 1000000000), "Event", "weight")
 #       j71_1 = j71_1.Clone()
  #      h71_1.Add(j71_1)
	
#	j72_1 = Rdf_spike.Histo1D(("j72_1", "Luminosity Block in Photon pT Spike", 1000, 0, 1000), "LumiBlock", "weight")
 #       j72_1 = j72_1.Clone()
  #      h72_1.Add(j72_1)
	
#	j75 = Rdf_Final.Histo1D(("j75", "Tau32", 150, 0, 1.5), "tau32", "weight")
#        j75 = j75.Clone()
#        h75.Add(j75)

	j80 = Rdf_Final.Histo1D(("j80", "AK4 HT", 1000, 0, 5000), "jHT", "weight")
        j80 = j80.Clone()
        h80.Add(j80)
	
	j81 = Rdf_Final.Histo1D(("j81", "AK8 HT", 1000, 0, 5000), "jHT_AK8", "weight")
        j81 = j81.Clone()
        h81.Add(j81)
	
	j90 = Rdf_Final.Histo1D(("j90", "AK4 Jet pT", 200, 0, 2000), "jPt_AK4", "weight")
        j90 = j90.Clone()
        h90.Add(j90)
	
	print(str(nocut)+" Events Before Cuts in "+fname+" Sample")		
	print(str(npcut)+" Events After nPho>0 in in "+fname+" Sample")		
	print(str(njcut)+" Events After nselectedPatJetsAK8PFPuppi>0 in "+fname+" Sample")		
	print(str(trigcut)+" Events After Trigger Cuts in "+fname+" Sample")		
	print(str(pcut)+" Events After Photon Cuts in "+fname+" Sample")		
	print(str(jcut)+" Events After Jet Cuts in "+fname+" Sample")		
	print(str(final)+" Events After Final Cuts in "+fname+" Sample")		
	print(str(pass_events)+" Passing Events in "+fname+" Sample")		
	print(str(fail_events)+" Failing Events in "+fname+" Sample")		
	

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
	print("Passing Events: "+str(pass_pass/total_events * 100)+"%")
	print("Failing Events: "+str(fail_pass/total_events * 100)+"%")
	
#	print("Passing Fraction: "+str(pass_pass_weight/(pass_pass_weight+fail_pass_weight) * 100)+"%")


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

        h32_w.SetTitle("Wide Passing Jet pT vs. Softdrop Mass")
        h32_w.SetYTitle("Softdrop Mass")
        h32_w.SetXTitle("Jet pT")
        ofile.WriteObject(h32_w, "jet_pt_soft_pass_wide4_wide")

        h33_w.SetTitle("Wide Total Jet pT vs. Softdrop Mass")
        h33_w.SetYTitle("Softdrop Mass")
        h33_w.SetXTitle("Jet pT")
        ofile.WriteObject(h33_w, "jet_pt_soft_total_wide4_wide")

        h34_w.SetTitle("Wide Failing Jet pT vs. Softdrop Mass")
        h34_w.SetYTitle("Softdrop Mass")
        h34_w.SetXTitle("Jet pT")
        ofile.WriteObject(h34_w, "jet_pt_soft_fail_wide4_wide")

        h35_w.SetTitle("Passing Jet pT vs. Rho")
        h35_w.SetYTitle("Rho")
        h35_w.SetXTitle("Jet pT")
        ofile.WriteObject(h35_w, "jet_pt_rho_pass_wide4_thin")

        h36_w.SetTitle("Total Jet pT vs. Rho")
        h36_w.SetYTitle("Rho")
        h36_w.SetXTitle("Jet pT")
        ofile.WriteObject(h36_w, "jet_pt_rho_total_wide4_thin")

        h37_w.SetTitle("Failing Jet pT vs. Rho")
        h37_w.SetYTitle("Rho")
        h37_w.SetXTitle("Jet pT")
        ofile.WriteObject(h37_w, "jet_pt_rho_fail_wide4_thin")

        h38_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h38_w.SetYTitle("Softdrop Mass")
        h38_w.SetXTitle("Jet pT")
        ofile.WriteObject(h38_w, "jet_pt_soft_pass_wide5_wide")

        h39_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h39_w.SetYTitle("Softdrop Mass")
        h39_w.SetXTitle("Jet pT")
        ofile.WriteObject(h39_w, "jet_pt_soft_total_wide5_wide")

        h40_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h40_w.SetYTitle("Softdrop Mass")
        h40_w.SetXTitle("Jet pT")
        ofile.WriteObject(h40_w, "jet_pt_soft_fail_wide5_wide")
        
	h41_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h41_w.SetYTitle("Softdrop Mass")
        h41_w.SetXTitle("Jet pT")
        ofile.WriteObject(h41_w, "jet_pt_soft_pass_wide6_wide")

        h42_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h42_w.SetYTitle("Softdrop Mass")
        h42_w.SetXTitle("Jet pT")
        ofile.WriteObject(h42_w, "jet_pt_soft_total_wide6_wide")

        h43_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h43_w.SetYTitle("Softdrop Mass")
        h43_w.SetXTitle("Jet pT")
        ofile.WriteObject(h43_w, "jet_pt_soft_fail_wide6_wide")
        
	h44_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h44_w.SetYTitle("Softdrop Mass")
        h44_w.SetXTitle("Jet pT")
        ofile.WriteObject(h44_w, "jet_pt_soft_pass_wide7_wide")

        h45_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h45_w.SetYTitle("Softdrop Mass")
        h45_w.SetXTitle("Jet pT")
        ofile.WriteObject(h45_w, "jet_pt_soft_total_wide7_wide")

        h46_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h46_w.SetYTitle("Softdrop Mass")
        h46_w.SetXTitle("Jet pT")
        ofile.WriteObject(h46_w, "jet_pt_soft_fail_wide7_wide")
        
	h47_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h47_w.SetYTitle("Softdrop Mass")
        h47_w.SetXTitle("Jet pT")
        ofile.WriteObject(h47_w, "jet_pt_soft_pass_wide8_wide")

        h48_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h48_w.SetYTitle("Softdrop Mass")
        h48_w.SetXTitle("Jet pT")
        ofile.WriteObject(h48_w, "jet_pt_soft_total_wide8_wide")

        h49_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h49_w.SetYTitle("Softdrop Mass")
        h49_w.SetXTitle("Jet pT")
        ofile.WriteObject(h49_w, "jet_pt_soft_fail_wide8_wide")
        
	h50_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h50_w.SetYTitle("Softdrop Mass")
        h50_w.SetXTitle("Jet pT")
        ofile.WriteObject(h50_w, "jet_pt_soft_pass_wide9_wide")

        h51_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h51_w.SetYTitle("Softdrop Mass")
        h51_w.SetXTitle("Jet pT")
        ofile.WriteObject(h51_w, "jet_pt_soft_total_wide9_wide")

        h52_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h52_w.SetYTitle("Softdrop Mass")
        h52_w.SetXTitle("Jet pT")
        ofile.WriteObject(h52_w, "jet_pt_soft_fail_wide9_wide")
	
	h53_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h53_w.SetYTitle("Softdrop Mass")
        h53_w.SetXTitle("Jet pT")
        ofile.WriteObject(h53_w, "jet_pt_soft_pass_wide10_wide")

        h54_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h54_w.SetYTitle("Softdrop Mass")
        h54_w.SetXTitle("Jet pT")
        ofile.WriteObject(h54_w, "jet_pt_soft_total_wide10_wide")

        h55_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h55_w.SetYTitle("Softdrop Mass")
        h55_w.SetXTitle("Jet pT")
        ofile.WriteObject(h55_w, "jet_pt_soft_fail_wide10_wide")
	
	h56_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h56_w.SetYTitle("Softdrop Mass")
        h56_w.SetXTitle("Jet pT")
        ofile.WriteObject(h56_w, "jet_pt_soft_pass_wide11_wide")

        h57_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h57_w.SetYTitle("Softdrop Mass")
        h57_w.SetXTitle("Jet pT")
        ofile.WriteObject(h57_w, "jet_pt_soft_total_wide11_wide")

        h58_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h58_w.SetYTitle("Softdrop Mass")
        h58_w.SetXTitle("Jet pT")
        ofile.WriteObject(h58_w, "jet_pt_soft_fail_wide11_wide")

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

        h54.SetTitle("MET pT")
        h54.SetXTitle("pT")
        ofile.WriteObject(h54, "METPT")

        h55.SetTitle("MET Et")
        h55.SetXTitle("Et")
        ofile.WriteObject(h55, "MET_Et")

        h56.SetTitle("PuppiMET pT")
        h56.SetXTitle("pT")
        ofile.WriteObject(h56, "PuppiMETPT")

        h57.SetTitle("PuppiMET Et")
        h57.SetXTitle("Et")
        ofile.WriteObject(h57, "ak4_btag")

        h58.SetTitle("AK4 Jet Eta with PUPPI MET cut")
        h58.SetXTitle("Eta")
        ofile.WriteObject(h58, "ak4_eta_met")

        h59.SetTitle("AK4 Jet Phi with PUPPI MET cut")
        h59.SetXTitle("Phi")
        ofile.WriteObject(h59, "ak4_phi_met")

        h60.SetTitle("AK4 nJet with PUPPI MET cut")
        h60.SetXTitle("Number of Jets")
        ofile.WriteObject(h60, "ak4_njet_met")

        h61.SetTitle("AK4 BTag with PUPPI MET cut")
        h61.SetXTitle("DeepFlavB")
        ofile.WriteObject(h61, "ak4_btag_met")
        
	h65.SetTitle("Eta vs. Photon pT")
        h65.SetXTitle("Eta")
        h65.SetYTitle("Photon pT")
        ofile.WriteObject(h65, "eta_pho_pt")
	
#        h70.SetXTitle("Run Number")
#        ofile.WriteObject(h70, "run")
#        h71.SetXTitle("Event")
#        ofile.WriteObject(h71, "event")
#        h72.SetXTitle("Luminosity Block")
#        ofile.WriteObject(h72, "lumi")
        
#	h70_1.SetXTitle("Run Number")
#        ofile.WriteObject(h70_1, "run_spike")
#        h71_1.SetXTitle("Event")
#        ofile.WriteObject(h71_1, "event_spike")
#        h72_1.SetXTitle("Luminosity Block")
#        ofile.WriteObject(h72_1, "lumi_spike")
        
#	h75.SetXTitle("Tau32")
#        ofile.WriteObject(h75, "tau32")

	h80.SetXTitle("HT")
        ofile.WriteObject(h80, "HT")

	h81.SetXTitle("HT")
        ofile.WriteObject(h81, "HT_AK8")
	
	h90.SetXTitle("Jet pT")
	ofile.WriteObject(h90, "jet_pt_ak4")

	p1.SetTitle("Passing Softdrop Mass")
	p1.SetXTitle("Softdrop Mass")
	ofile.WriteObject(p1, "pass_soft")

        p1_1.SetTitle("Thin Passing Softdrop Mass")
        p1_1.SetXTitle("Softdrop Mass")
        ofile.WriteObject(p1_1, "pass_soft_thin")
        
	p1_2.SetTitle("Thin (Uncorrected) Passing Softdrop Mass")
        p1_2.SetXTitle("Softdrop Mass")
        ofile.WriteObject(p1_2, "pass_soft_uncorr_thin")

	p2.SetTitle("Passing Photon pT")
	p2.SetXTitle("Photon pT")
	ofile.WriteObject(p2, "pass_photon_pt")

	p3.SetTitle("Passing Jet pT")
	p3.SetXTitle("Jet pT")
	ofile.WriteObject(p3, "pass_jet_pt")

	p4.SetTitle("Passing Rho")
	p4.SetXTitle("Rho")
	ofile.WriteObject(p4, "pass_rho")

	p5.SetTitle("Passing Photon Eta")
	p5.SetXTitle("Photon Eta")
	ofile.WriteObject(p5, "pass_photon_eta")

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

	f2.SetTitle("Failing Photon pT")
	f2.SetXTitle("Photon pT")
	ofile.WriteObject(f2, "fail_photon_pt")

	f3.SetTitle("Failing Jet pT")
	f3.SetXTitle("Jet pT")
	ofile.WriteObject(f3, "fail_jet_pt")

	f4.SetTitle("Failing Rho")
	f4.SetXTitle("Rho")
	ofile.WriteObject(f4, "fail_rho")

	f5.SetTitle("Failing Photon Eta")
	f5.SetXTitle("Photon Eta")
	ofile.WriteObject(f5, "fail_photon_eta")

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
