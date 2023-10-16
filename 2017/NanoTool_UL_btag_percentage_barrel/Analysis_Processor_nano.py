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

	ofile = ROOT.TFile("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/output/RData_" + fname + ".root", "RECREATE")
	ofile.cd()

#	ROOT.ROOT.EnableImplicitMT()


	rho_bins = cut_hist.GetNbinsX()
	pt_bins = cut_hist.GetNbinsY()

		

	h1 = TH1F("h1", "N2", 50, 0, 0.5)
	h2 = TH1F("h2", "Softdrop Mass", 40, 0, 200)
        h2_1 = TH1F("h2_1", "Thin Softdrop Mass", 200, 0, 200)
        h2_2 = TH1F("h2_2", "Thin (Uncorrected) Softdrop Mass", 200, 0, 200)
	h4 = TH1F("h4", "Photon pT", 100, 0, 2000)
	h5 = TH1F("h5", "Jet pT", 40, 0, 2000)
        h5_1 = TH1F("h5_1", "Thin Jet pT", 400, 0, 2000)
	h6 = TH1F("h6", "Jet Eta", 70, -3.5, 3.5)
	h7 = TH1F("h7", "Rho", 28, -8, -1)
	h8 = TH1F("h8", "Photon Eta", 70, -3.5, 3.5)
	h9 = TH1F("h9", "N2DDT", 100, -.5, .5)
	
	h11 = TH2F("n2_n2ddt", "N2 vs. N2DDT", 50, 0, 0.5, 100, -.5, .5)
	h14 = TH2F("n2_soft", "N2 vs. Softdrop Mass", 100, 0, 1, 40, 0, 200)
	h14_1 = TH2F("soft_n2", "Softdrop Mass vs. N2", 40, 0, 200, 100, 0, 1)
	h15 = TH2F("n2ddt_soft", "N2DDT vs. Softdrop Mass", 100, -.5, .5, 40, 0, 200)
	h15_1 = TH2F("soft_n2ddt", "Softdrop Mass vs. N2DDT", 40, 0, 200, 100, -.5, .5)
	
	h16 = TH2F("rho_soft", "Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h17 = TH2F("rho_soft_pass", "Passing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h18 = TH2F("rho_soft_fail", "Failing Rho vs. Softdrop Mass", 28, -8, -1, 40, 0, 200)
	h19 = TH2F("n2_pt", "N2 vs. Jet pT", 100, 0, 1.0, 400, 0, 2000)
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

	#2017 pT Binning
        ROOT.gInterpreter.Declare("Double_t widebins5[7] = {0, 220, 255, 290, 360, 1000, 2000};")
      	h38_w = TH2F("jet_pt_soft_pass_wide5_wide", "Passing Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200)
        h39_w = TH2F("jet_pt_soft_total_wide5_wide", "Total Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200)
        h40_w = TH2F("jet_pt_soft_fail_wide5_wide", "Failing Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200)
        
	ROOT.gInterpreter.Declare("Double_t widebins6[8] = {0, 220, 230, 255, 290, 360, 1000, 2000};")
	h41_w = TH2F("jet_pt_soft_pass_wide6_wide", "Passing Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200)
        h42_w = TH2F("jet_pt_soft_total_wide6_wide", "Total Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200)
        h43_w = TH2F("jet_pt_soft_fail_wide6_wide", "Failing Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200)
        
	ROOT.gInterpreter.Declare("Double_t widebins7[8] = {0, 220, 255, 290, 360, 500, 1000, 2000};")
      	h44_w = TH2F("jet_pt_soft_pass_wide7_wide", "Passing Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200)
        h45_w = TH2F("jet_pt_soft_total_wide7_wide", "Total Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200)
        h46_w = TH2F("jet_pt_soft_fail_wide7_wide", "Failing Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200)

	h47 = TH1F("h47", "Number of Good Reconstructed Primary Verticies", 70, 0, 70)

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
	
	h80 = TH1F("HT", "AK4 HT", 1000, 0, 5000)
	h81 = TH1F("HT_AK8", "AK8 HT", 1000, 0, 5000)
	
	h90 = TH1F("h90", "AK4 Jet pT", 200, 0, 2000)

	p1 = TH1F("p1", "passing softdrop mass", 40, 0, 200)
        p1_1 = TH1F("p1_1", "thin passing softdrop mass", 200, 0, 200)
	p1_2 = TH1F("p1_2", "thin (uncorrected) passing softdrop mass", 200, 0, 200)
	p2 = TH1F("p2", "passing photon pt", 50, 0, 1000)
	p3 = TH1F("p3", "passing jet pt", 40, 0, 2000)
        p3_1 = TH1F("p3_1", "Thin Passing Jet pT", 400, 0, 2000)
	p4 = TH1F("p4", "passing rho", 28, -8, -1)
	p5 = TH1F("p5", "passing photon eta", 70, -3.5, 3.5)
	p6 = TH1F("p6", "passing jet eta", 70, -3.5, 3.5)

	f1 = TH1F("f1", "failing softdrop mass", 40, 0, 200)
        f1_1 = TH1F("f1_1", "thin failing softdrop mass", 200, 0, 200)
	f1_2 = TH1F("f1_2", "thin failing (uncorrected) softdrop mass", 200, 0, 200)
	f2 = TH1F("f2", "failing photon pt", 100, 0, 2000)
	f3 = TH1F("f3", "failing jet pt", 40, 0, 2000)
        f3_1 = TH1F("f3_1", "Thin Failing Jet pT", 400, 0, 2000)
	f4 = TH1F("f4", "failing rho", 28, -8, -1)
	f5 = TH1F("f5", "failing photon eta", 70, -3.5, 3.5)
	f6 = TH1F("f6", "failing jet eta", 70, -3.5, 3.5)
	
	# Systematics Histograms
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
		h2_puUp = TH1F("h2_puUp", "Softdrop Mass PileUp Up", 40, 0, 200)
        	h2_1_puUp = TH1F("h2_1_puUp", "Thin Softdrop Mass PileUp Up", 200, 0, 200)
        	h2_2_puUp = TH1F("h2_2_puUp", "Thin (Uncorrected) Softdrop Mass PileUp Up", 200, 0, 200)
		h5_puUp = TH1F("h5_puUp", "Jet pT PileUp Up", 40, 0, 2000)
        	h5_1_puUp = TH1F("h5_1_puUp", "Thin Jet pT PileUp Up", 400, 0, 2000)
		h6_puUp = TH1F("h6_puUp", "Number of Good Reconstructed Primary Verticies PileUp Up", 70, 0, 70)
		h2_puDown = TH1F("h2_puDown", "Softdrop Mass PileUp Down", 40, 0, 200)
        	h2_1_puDown = TH1F("h2_1_puDown", "Thin Softdrop Mass PileUp Down", 200, 0, 200)
        	h2_2_puDown = TH1F("h2_2_puDown", "Thin (Uncorrected) Softdrop Mass PileUp Down", 200, 0, 200)
		h5_puDown = TH1F("h5_puDown", "Jet pT PileUp Down", 40, 0, 2000)
        	h5_1_puDown = TH1F("h5_1_puDown", "Thin Jet pT PileUp Down", 400, 0, 2000)
		h6_puDown = TH1F("h6_puDown", "Number of Good Reconstructed Primary Verticies PileUp Down", 70, 0, 70)
		
		h2_jerUp = TH1F("h2_jerUp", "Softdrop Mass JER Up", 40, 0, 200)
        	h2_1_jerUp = TH1F("h2_1_jerUp", "Thin Softdrop Mass JER Up", 200, 0, 200)
        	h2_2_jerUp = TH1F("h2_2_jerUp", "Thin (Uncorrected) Softdrop Mass JER Up", 200, 0, 200)
		h5_jerUp = TH1F("h5_jerUp", "Jet pT JER Up", 40, 0, 2000)
        	h5_1_jerUp = TH1F("h5_1_jerUp", "Thin Jet pT JER Up", 400, 0, 2000)
		h2_jerDown = TH1F("h2_jerDown", "Softdrop Mass JER Down", 40, 0, 200)
        	h2_1_jerDown = TH1F("h2_1_jerDown", "Thin Softdrop Mass JER Down", 200, 0, 200)
        	h2_2_jerDown = TH1F("h2_2_jerDown", "Thin (Uncorrected) Softdrop Mass JER Down", 200, 0, 200)
		h5_jerDown = TH1F("h5_jerDown", "Jet pT JER Down", 40, 0, 2000)
        	h5_1_jerDown = TH1F("h5_1_jerDown", "Thin Jet pT JER Down", 400, 0, 2000)

		h2_jesUp = TH1F("h2_jesUp", "Softdrop Mass JES Up", 40, 0, 200)
        	h2_1_jesUp = TH1F("h2_1_jesUp", "Thin Softdrop Mass JES Up", 200, 0, 200)
        	h2_2_jesUp = TH1F("h2_2_jesUp", "Thin (Uncorrected) Softdrop Mass JES Up", 200, 0, 200)
		h5_jesUp = TH1F("h5_jesUp", "Jet pT JES Up", 40, 0, 2000)
        	h5_1_jesUp = TH1F("h5_1_jesUp", "Thin Jet pT JES Up", 400, 0, 2000)
		h2_jesDown = TH1F("h2_jesDown", "Softdrop Mass JES Down", 40, 0, 200)
        	h2_1_jesDown = TH1F("h2_1_jesDown", "Thin Softdrop Mass JES Down", 200, 0, 200)
        	h2_2_jesDown = TH1F("h2_2_jesDown", "Thin (Uncorrected) Softdrop Mass JES Down", 200, 0, 200)
		h5_jesDown = TH1F("h5_jesDown", "Jet pT JES Down", 40, 0, 2000)
        	h5_1_jesDown = TH1F("h5_1_jesDown", "Thin Jet pT JES Down", 400, 0, 2000)

		p1_puUp = TH1F("p1_puUp", "passing softdrop mass PileUp Up", 40, 0, 200)
	        p1_1_puUp = TH1F("p1_1_puUp", "thin passing softdrop mass PileUp Up", 200, 0, 200)
		p1_2_puUp = TH1F("p1_2_puUp", "thin (uncorrected) passing softdrop mass PileUp Up", 200, 0, 200)
		p3_puUp = TH1F("p3_puUp", "passing jet pt PileUp Up", 40, 0, 2000)
	        p3_1_puUp = TH1F("p3_1_puUp", "Thin Passing Jet pT PileUp Up", 400, 0, 2000)
		f1_puUp = TH1F("f1_puUp", "failing softdrop mass PileUp Up", 40, 0, 200)
	        f1_1_puUp = TH1F("f1_1_puUp", "failing softdrop mass PileUp Up", 200, 0, 200)
		f1_2_puUp = TH1F("f1_2_puUp", "failing (uncorrected) softdrop mass PileUp Up", 200, 0, 200)
		f3_puUp = TH1F("f3_puUp", "failing jet pt PileUp Up", 40, 0, 2000)
	        f3_1_puUp = TH1F("f3_1_puUp", "Thin Failinging Jet pT PileUp Up", 400, 0, 2000)
		p1_puDown = TH1F("p1_puDown", "passing softdrop mass PileUp Down", 40, 0, 200)
	        p1_1_puDown = TH1F("p1_1_puDown", "thin passing softdrop mass PileUp Down", 200, 0, 200)
		p1_2_puDown = TH1F("p1_2_puDown", "thin (uncorrected) passing softdrop mass PileUp Down", 200, 0, 200)
		p3_puDown = TH1F("p3_puDown", "passing jet pt PileUp Down", 40, 0, 2000)
	        p3_1_puDown = TH1F("p3_1_puDown", "Thin Passing Jet pT PileUp Down", 400, 0, 2000)
		f1_puDown = TH1F("f1_puDown", "failing softdrop mass PileUp Down", 40, 0, 200)
	        f1_1_puDown = TH1F("f1_1_puDown", "failing softdrop mass PileUp Down", 200, 0, 200)
		f1_2_puDown = TH1F("f1_2_puDown", "failing (uncorrected) softdrop mass PileUp Down", 200, 0, 200)
		f3_puDown = TH1F("f3_puDown", "failing jet pt PileUp Down", 40, 0, 2000)
	        f3_1_puDown = TH1F("f3_1_puDown", "Thin Failinging Jet pT PileUp Down", 400, 0, 2000)

		p1_jerUp = TH1F("p1_jerUp", "passing softdrop mass JER Up", 40, 0, 200)
	        p1_1_jerUp = TH1F("p1_1_jerUp", "thin passing softdrop mass JER Up", 200, 0, 200)
		p1_2_jerUp = TH1F("p1_2_jerUp", "thin (uncorrected) passing softdrop mass JER Up", 200, 0, 200)
		p3_jerUp = TH1F("p3_jerUp", "passing jet pt JER Up", 40, 0, 2000)
	        p3_1_jerUp = TH1F("p3_1_jerUp", "Thin Passing Jet pT JER Up", 400, 0, 2000)
		f1_jerUp = TH1F("f1_jerUp", "failing softdrop mass JER Up", 40, 0, 200)
	        f1_1_jerUp = TH1F("f1_1_jerUp", "failing softdrop mass JER Up", 200, 0, 200)
		f1_2_jerUp = TH1F("f1_2_jerUp", "failing (uncorrected) softdrop mass JER Up", 200, 0, 200)
		f3_jerUp = TH1F("f3_jerUp", "failing jet pt JER Up", 40, 0, 2000)
	        f3_1_jerUp = TH1F("f3_1_jerUp", "Thin Failinging Jet pT JER Up", 400, 0, 2000)
		p1_jerDown = TH1F("p1_jerDown", "passing softdrop mass JER Down", 40, 0, 200)
	        p1_1_jerDown = TH1F("p1_1_jerDown", "thin passing softdrop mass JER Down", 200, 0, 200)
		p1_2_jerDown = TH1F("p1_2_jerDown", "thin (uncorrected) passing softdrop mass JER Down", 200, 0, 200)
		p3_jerDown = TH1F("p3_jerDown", "passing jet pt JER Down", 40, 0, 2000)
	        p3_1_jerDown = TH1F("p3_1_jerDown", "Thin Passing Jet pT JER Down", 400, 0, 2000)
		f1_jerDown = TH1F("f1_jerDown", "failing softdrop mass JER Down", 40, 0, 200)
	        f1_1_jerDown = TH1F("f1_1_jerDown", "failing softdrop mass JER Down", 200, 0, 200)
		f1_2_jerDown = TH1F("f1_2_jerDown", "failing (uncorrected) softdrop mass JER Down", 200, 0, 200)
		f3_jerDown = TH1F("f3_jerDown", "failing jet pt JER Down", 40, 0, 2000)
	        f3_1_jerDown = TH1F("f3_1_jerDown", "Thin Failinging Jet pT JER Down", 400, 0, 2000)

		p1_jesUp = TH1F("p1_jesUp", "passing softdrop mass JES Up", 40, 0, 200)
	        p1_1_jesUp = TH1F("p1_1_jesUp", "thin passing softdrop mass JES Up", 200, 0, 200)
		p1_2_jesUp = TH1F("p1_2_jesUp", "thin (uncorrected) passing softdrop mass JES Up", 200, 0, 200)
		p3_jesUp = TH1F("p3_jesUp", "passing jet pt JES Up", 40, 0, 2000)
	        p3_1_jesUp = TH1F("p3_1_jesUp", "Thin Passing Jet pT JES Up", 400, 0, 2000)
		f1_jesUp = TH1F("f1_jesUp", "failing softdrop mass JES Up", 40, 0, 200)
	        f1_1_jesUp = TH1F("f1_1_jesUp", "failing softdrop mass JES Up", 200, 0, 200)
		f1_2_jesUp = TH1F("f1_2_jesUp", "failing (uncorrected) softdrop mass JES Up", 200, 0, 200)
		f3_jesUp = TH1F("f3_jesUp", "failing jet pt JES Up", 40, 0, 2000)
	        f3_1_jesUp = TH1F("f3_1_jesUp", "Thin Failinging Jet pT JES Up", 400, 0, 2000)
		p1_jesDown = TH1F("p1_jesDown", "passing softdrop mass JES Down", 40, 0, 200)
	        p1_1_jesDown = TH1F("p1_1_jesDown", "thin passing softdrop mass JES Down", 200, 0, 200)
		p1_2_jesDown = TH1F("p1_2_jesDown", "thin (uncorrected) passing softdrop mass JES Down", 200, 0, 200)
		p3_jesDown = TH1F("p3_jesDown", "passing jet pt JES Down", 40, 0, 2000)
	        p3_1_jesDown = TH1F("p3_1_jesDown", "Thin Passing Jet pT JES Down", 400, 0, 2000)
		f1_jesDown = TH1F("f1_jesDown", "failing softdrop mass JES Down", 40, 0, 200)
	        f1_1_jesDown = TH1F("f1_1_jesDown", "failing softdrop mass JES Down", 200, 0, 200)
		f1_2_jesDown = TH1F("f1_2_jesDown", "failing (uncorrected) softdrop mass JES Down", 200, 0, 200)
		f3_jesDown = TH1F("f3_jesDown", "failing jet pt JES Down", 40, 0, 2000)
	        f3_1_jesDown = TH1F("f3_1_jesDown", "Thin Failinging Jet pT JES Down", 400, 0, 2000)


		h41_w_puUp = TH2F("jet_pt_soft_pass_wide6_wide_puUp", "Passing Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200)
        	h42_w_puUp = TH2F("jet_pt_soft_total_wide6_wide_puUp", "Total Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200)
        	h43_w_puUp = TH2F("jet_pt_soft_fail_wide6_wide_puUp", "Failing Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200)
		h41_w_puDown = TH2F("jet_pt_soft_pass_wide6_wide_puDown", "Passing Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200)
        	h42_w_puDown = TH2F("jet_pt_soft_total_wide6_wide_puDown", "Total Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200)
        	h43_w_puDown = TH2F("jet_pt_soft_fail_wide6_wide_puDown", "Failing Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200)
		
		h41_w_jerUp = TH2F("jet_pt_soft_pass_wide6_wide_jerUp", "Passing Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200)
        	h42_w_jerUp = TH2F("jet_pt_soft_total_wide6_wide_jerUp", "Total Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200)
        	h43_w_jerUp = TH2F("jet_pt_soft_fail_wide6_wide_jerUp", "Failing Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200)
		h41_w_jerDown = TH2F("jet_pt_soft_pass_wide6_wide_jerDown", "Passing Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200)
        	h42_w_jerDown = TH2F("jet_pt_soft_total_wide6_wide_jerDown", "Total Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200)
        	h43_w_jerDown = TH2F("jet_pt_soft_fail_wide6_wide_jerDown", "Failing Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200)
		
		h41_w_jesUp = TH2F("jet_pt_soft_pass_wide6_wide_jesUp", "Passing Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200)
        	h42_w_jesUp = TH2F("jet_pt_soft_total_wide6_wide_jesUp", "Total Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200)
        	h43_w_jesUp = TH2F("jet_pt_soft_fail_wide6_wide_jesUp", "Failing Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200)
		h41_w_jesDown = TH2F("jet_pt_soft_pass_wide6_wide_jesDown", "Passing Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200)
        	h42_w_jesDown = TH2F("jet_pt_soft_total_wide6_wide_jesDown", "Total Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200)
        	h43_w_jesDown = TH2F("jet_pt_soft_fail_wide6_wide_jesDown", "Failing Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200)
		
		
	nocut = 0
	npcut = 0
	njcut = 0
	pcut = 0
	jcut = 0
	nsubcut = 0

	#trigcut = 0

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

	Rdf_noCut = RDF(Chain)
	nocut += float(Rdf_noCut.Count().GetValue())
	total_events += float(Rdf_noCut.Count().GetValue())

	
	
	if sample[3] == "data": #Take 10% of Data
                Rdf_noCut = Rdf_noCut.Filter("rdfentry_ % 10 == 0", "10% of Data Cut")
                ten_pass += float(Rdf_noCut.Count().GetValue())
	Rdf_noCut = Rdf_noCut.Filter("(HLT_Photon200 >0.0)", "Trigger Cut")

	trig_pass += float(Rdf_noCut.Count().GetValue())

	Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.", "Number of Photons Cut")
	npcut += float(Rdf_PreSel.Count().GetValue())

	Rdf_PreSel = Rdf_PreSel.Filter("nFatJet > 0.", "Number of Jets Cut")
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


	Rdf_cflow = Rdf_cflow.Filter("JPT(FatJet_pt_nom, nFatJet)")
	jpt_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("PETA(Photon_pt, Photon_eta, nPhoton)")
	peta_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JETA(FatJet_pt_nom, FatJet_eta, nFatJet)")
	jeta_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("PID(Photon_pt, Photon_eta, Photon_cutBased, nPhoton)")
	pid_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JID(FatJet_pt_nom, FatJet_eta, FatJet_jetId, nFatJet)")
	jid_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JSOFT(FatJet_pt_nom, FatJet_eta, FatJet_jetId,FatJet_msoftdrop_raw, nFatJet)")
	jsoft_pass += float(Rdf_cflow.Count().GetValue())
       
		
	Rdf_cflow = Rdf_cflow.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
	Rdf_cflow = Rdf_cflow.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

	Rdf_cflow = Rdf_cflow.Filter("FatJet_n2b1[jIndex]")
	n2_pass += float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Define("Rho", "rho(FatJet_pt_nom[jIndex], FatJet_msoftdrop_raw[jIndex])")
	Rdf_cflow = Rdf_cflow.Filter("Rho > -7 && Rho < -2")
		
	rho_pass += float(Rdf_cflow.Count().GetValue())


	
	#ROOT.gInterpreter.Declare('#include "Help.h"')
	Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")
	
	#Direct Prompt Filter
	if sample[3] == "GJ":
		Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)", "Direct Prompt Photon Required")
	if sample[3] == "QCD":
		Rdf_PreSel = Rdf_PreSel.Filter("!dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)", "Direct Prompt Photon Rejected")

	#Trigger Filter
	Rdf_PreSel = Rdf_PreSel.Filter("(HLT_Photon200 >0.0)")

#	trigcut += float(Rdf_PreSel.Count().GetValue())

	Rdf = Rdf_PreSel.Filter("pIndex >= 0", "Photon Cuts")
	pcut += float(Rdf.Count().GetValue())
	
		
	Rdf = Rdf.Filter("jIndex >= 0", "Jet Cuts")
	jcut += float(Rdf.Count().GetValue())

	if sample[3] == "data":
		Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]")
	else:
		Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]*FatJet_corr_JER[jIndex]")

#	print("Test1")	
#        print(float(Rdf.Count().GetValue()))
	Rdf = Rdf.Define("jEta", "FatJet_eta[jIndex]")
	Rdf = Rdf.Define("jPhi", "FatJet_phi[jIndex]")
	Rdf = Rdf.Define("jPt", "FatJet_pt_nom[jIndex]")
	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
	Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
	Rdf = Rdf.Define("N2", "FatJet_n2b1[jIndex]")
	Rdf = Rdf.Define("jID", "FatJet_jetId[jIndex]")
	Rdf = Rdf.Define("n2ddt", "ddt(jPt, jM, N2)")

	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")

	Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
        Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")

	Rdf = Rdf.Define("PV_Good", "PV_npvsGood")
        Rdf = Rdf.Define("nj4", "nJet")
        Rdf = Rdf.Define("ak4_nomatch", "ak4_match(nj4, Jet_eta, Jet_phi, jEta, jPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that do NOT match the boosted AK8 jet sorted by btag score

        Rdf = Rdf.Define("j4eta", "ak4_ret(ak4_nomatch, Jet_eta)[0]")
        Rdf = Rdf.Define("j4phi", "ak4_ret(ak4_nomatch, Jet_phi)[0]")
        Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_nomatch, Jet_btagDeepFlavB)[0]")

        Rdf = Rdf.Define("METpt", "MET_pt")
        Rdf = Rdf.Define("MET_Et", "MET_sumEt")
        Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")
        Rdf = Rdf.Define("PuppiMET_Et", "PuppiMET_sumEt")
	Rdf = Rdf.Define("jHT", "HT(Jet_pt, Jet_eta)")
	Rdf = Rdf.Define("jHT_AK8", "HT_AK8(FatJet_pt_nom, FatJet_eta)")
	Rdf = Rdf.Define("jPt_AK4", "Jet_pt[0]")

#	print("Test2")	
#        print(float(Rdf.Count().GetValue()))
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
                Rdf = Rdf.Define("xs_lumi", sample[1])
                Rdf = Rdf.Define("weight", "xs_lumi*puWeight")
		# Pileup Systematic Weights
                Rdf = Rdf.Define("weight_Up", "xs_lumi*puWeightUp")
                Rdf = Rdf.Define("weight_Down", "xs_lumi*puWeightDown")
        elif sample[3] == "data":
                Rdf = Rdf.Define("weight", sample[1])


	
	
	Rdf_Final = Rdf.Filter("N2 >= 0.0", "N2>0 Cut")
	Rdf_Final = Rdf_Final.Filter("Rho > -7 && Rho < -2", "Rho Cut")
	Rdf_Final = Rdf_Final.Filter("dR >= 2.2", "dR Cut")
	dR_pass += float(Rdf_Final.Count().GetValue())

        Rdf_MET = Rdf_Final.Filter("PuppiMETpt < 75") #Additional MET cut for btag testing
        Rdf_Final = Rdf_Final.Filter("PuppiMETpt < 75 && jBtag < 0.0532", "TTBar Veto")

        final += float(Rdf_Final.Count().GetValue())
#	print(final)	


	# Systematics
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
		Rdf_Final = Rdf_Final.Define("jPt_jerUp", "FatJet_pt_jerUp[jIndex]")
		Rdf_Final = Rdf_Final.Define("jPt_jerDown", "FatJet_pt_jerDown[jIndex]")
		Rdf_Final = Rdf_Final.Define("jM_uncorr_jerUp", "jM_uncorr * (jPt_jerUp / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_uncorr_jerDown", "jM_uncorr * (jPt_jerDown / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_jerUp", "jM * (jPt_jerUp / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_jerDown", "jM * (jPt_jerDown / jPt)")
	
		# JES Correlated Factors
		jes_mass_comment = '''
		Rdf_Final = Rdf_Final.Define("jM_jesAbsBiasUp", "pow(((FatJet_msoftdrop_jesAbsoluteMPFBiasUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesAbsScaleUp", "pow(((FatJet_msoftdrop_jesAbsoluteScaleUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesFlavQCDUp", "pow(((FatJet_msoftdrop_jesFlavorQCDUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesFragUp", "pow(((FatJet_msoftdrop_jesFragmentationUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPileDataMCUp", "pow(((FatJet_msoftdrop_jesPileUpDataMCUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtBBUp", "pow(((FatJet_msoftdrop_jesPileUpPtBBUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtEC1Up", "pow(((FatJet_msoftdrop_jesPileUpPtEC1Up[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtEC2Up", "pow(((FatJet_msoftdrop_jesPileUpPtEC2Up[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtHFUp", "pow(((FatJet_msoftdrop_jesPileUpPtHFUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtRefUp", "pow(((FatJet_msoftdrop_jesPileUpPtRefUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelFSRUp", "pow(((FatJet_msoftdrop_jesRelativeFSRUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelJERHFUp", "pow(((FatJet_msoftdrop_jesRelativeJERHFUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelPtBBUp", "pow(((FatJet_msoftdrop_jesRelativePtBBUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelPtHFUp", "pow(((FatJet_msoftdrop_jesRelativePtHFUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelBalUp", "pow(((FatJet_msoftdrop_jesRelativeBalUp[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPionECALUp", "pow(((FatJet_msoftdrop_jesSinglePionECALUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPionHCALUp", "pow(((FatJet_msoftdrop_jesSinglePionHCALUp[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		'''
		Rdf_Final = Rdf_Final.Define("jPt_jesAbsBiasUp", "pow(((FatJet_pt_jesAbsoluteMPFBiasUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesAbsScaleUp", "pow(((FatJet_pt_jesAbsoluteScaleUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesFlavQCDUp", "pow(((FatJet_pt_jesFlavorQCDUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesFragUp", "pow(((FatJet_pt_jesFragmentationUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPileDataMCUp", "pow(((FatJet_pt_jesPileUpDataMCUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtBBUp", "pow(((FatJet_pt_jesPileUpPtBBUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtEC1Up", "pow(((FatJet_pt_jesPileUpPtEC1Up[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtEC2Up", "pow(((FatJet_pt_jesPileUpPtEC2Up[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtHFUp", "pow(((FatJet_pt_jesPileUpPtHFUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtRefUp", "pow(((FatJet_pt_jesPileUpPtRefUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelFSRUp", "pow(((FatJet_pt_jesRelativeFSRUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelJERHFUp", "pow(((FatJet_pt_jesRelativeJERHFUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelPtBBUp", "pow(((FatJet_pt_jesRelativePtBBUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelPtHFUp", "pow(((FatJet_pt_jesRelativePtHFUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelBalUp", "pow(((FatJet_pt_jesRelativeBalUp[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPionECALUp", "pow(((FatJet_pt_jesSinglePionECALUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPionHCALUp", "pow(((FatJet_pt_jesSinglePionHCALUp[jIndex] - jPt)/(1.0 * jPt)),2)")
		
		jes_mass_comment2 = '''

		Rdf_Final = Rdf_Final.Define("jM_jesAbsBiasDown", "pow(((FatJet_msoftdrop_jesAbsoluteMPFBiasDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesAbsScaleDown", "pow(((FatJet_msoftdrop_jesAbsoluteScaleDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesFlavQCDDown", "pow(((FatJet_msoftdrop_jesFlavorQCDDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesFragDown", "pow(((FatJet_msoftdrop_jesFragmentationDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPileDataMCDown", "pow(((FatJet_msoftdrop_jesPileUpDataMCDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtBBDown", "pow(((FatJet_msoftdrop_jesPileUpPtBBDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtEC1Down", "pow(((FatJet_msoftdrop_jesPileUpPtEC1Down[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtEC2Down", "pow(((FatJet_msoftdrop_jesPileUpPtEC2Down[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtHFDown", "pow(((FatJet_msoftdrop_jesPileUpPtHFDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPilePtRefDown", "pow(((FatJet_msoftdrop_jesPileUpPtRefDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelFSRDown", "pow(((FatJet_msoftdrop_jesRelativeFSRDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelJERHFDown", "pow(((FatJet_msoftdrop_jesRelativeJERHFDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelPtBBDown", "pow(((FatJet_msoftdrop_jesRelativePtBBDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelPtHFDown", "pow(((FatJet_msoftdrop_jesRelativePtHFDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesRelBalDown", "pow(((FatJet_msoftdrop_jesRelativeBalDown[jIndex] - jM_uncorr)/(2.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPionECALDown", "pow(((FatJet_msoftdrop_jesSinglePionECALDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		Rdf_Final = Rdf_Final.Define("jM_jesPionHCALDown", "pow(((FatJet_msoftdrop_jesSinglePionHCALDown[jIndex] - jM_uncorr)/(1.0 * jM_uncorr)),2)")
		'''

		Rdf_Final = Rdf_Final.Define("jPt_jesAbsBiasDown", "pow(((FatJet_pt_jesAbsoluteMPFBiasDown[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesAbsScaleDown", "pow(((FatJet_pt_jesAbsoluteScaleDown[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesFlavQCDDown", "pow(((FatJet_pt_jesFlavorQCDDown[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesFragDown", "pow(((FatJet_pt_jesFragmentationDown[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPileDataMCDown", "pow(((FatJet_pt_jesPileUpDataMCDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtBBDown", "pow(((FatJet_pt_jesPileUpPtBBDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtEC1Down", "pow(((FatJet_pt_jesPileUpPtEC1Down[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtEC2Down", "pow(((FatJet_pt_jesPileUpPtEC2Down[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtHFDown", "pow(((FatJet_pt_jesPileUpPtHFDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPilePtRefDown", "pow(((FatJet_pt_jesPileUpPtRefDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelFSRDown", "pow(((FatJet_pt_jesRelativeFSRDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelJERHFDown", "pow(((FatJet_pt_jesRelativeJERHFDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelPtBBDown", "pow(((FatJet_pt_jesRelativePtBBDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelPtHFDown", "pow(((FatJet_pt_jesRelativePtHFDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesRelBalDown", "pow(((FatJet_pt_jesRelativeBalDown[jIndex] - jPt)/(2.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPionECALDown", "pow(((FatJet_pt_jesSinglePionECALDown[jIndex] - jPt)/(1.0 * jPt)),2)")
		Rdf_Final = Rdf_Final.Define("jPt_jesPionHCALDown", "pow(((FatJet_pt_jesSinglePionHCALDown[jIndex] - jPt)/(1.0 * jPt)),2)")


#		Rdf_Final = Rdf_Final.Define("jM_jesUp_Delta", "jM_jesAbsBiasUp+jM_jesAbsScaleUp+jM_jesFlavQCDUp+jM_jesFragUp+jM_jesPileDataMCUp+jM_jesPilePtBBUp+jM_jesPilePtEC1Up+jM_jesPilePtEC2Up+jM_jesPilePtHFUp+jM_jesPilePtRefUp+jM_jesRelFSRUp+jM_jesRelJERHFUp+jM_jesRelPtBBUp+jM_jesRelPtHFUp+jM_jesRelBalUp+jM_jesPionECALUp+jM_jesPionHCALUp")
		Rdf_Final = Rdf_Final.Define("jPt_jesUp_Delta", "jPt_jesAbsBiasUp+jPt_jesAbsScaleUp+jPt_jesFlavQCDUp+jPt_jesFragUp+jPt_jesPileDataMCUp+jPt_jesPilePtBBUp+jPt_jesPilePtEC1Up+jPt_jesPilePtEC2Up+jPt_jesPilePtHFUp+jPt_jesPilePtRefUp+jPt_jesRelFSRUp+jPt_jesRelJERHFUp+jPt_jesRelPtBBUp+jPt_jesRelPtHFUp+jPt_jesRelBalUp+jPt_jesPionECALUp+jPt_jesPionHCALUp")
#		Rdf_Final = Rdf_Final.Define("jM_jesDown_Delta", "jM_jesAbsBiasDown+jM_jesAbsScaleDown+jM_jesFlavQCDDown+jM_jesFragDown+jM_jesPileDataMCDown+jM_jesPilePtBBDown+jM_jesPilePtEC1Down+jM_jesPilePtEC2Down+jM_jesPilePtHFDown+jM_jesPilePtRefDown+jM_jesRelFSRDown+jM_jesRelJERHFDown+jM_jesRelPtBBDown+jM_jesRelPtHFDown+jM_jesRelBalDown+jM_jesPionECALDown+jM_jesPionHCALDown")
		Rdf_Final = Rdf_Final.Define("jPt_jesDown_Delta", "jPt_jesAbsBiasDown+jPt_jesAbsScaleDown+jPt_jesFlavQCDDown+jPt_jesFragDown+jPt_jesPileDataMCDown+jPt_jesPilePtBBDown+jPt_jesPilePtEC1Down+jPt_jesPilePtEC2Down+jPt_jesPilePtHFDown+jPt_jesPilePtRefDown+jPt_jesRelFSRDown+jPt_jesRelJERHFDown+jPt_jesRelPtBBDown+jPt_jesRelPtHFDown+jPt_jesRelBalDown+jPt_jesPionECALDown+jPt_jesPionHCALDown")
	

		Rdf_Final = Rdf_Final.Define("jPt_jesUp", "jPt * (1.0 + sqrt(jPt_jesUp_Delta))")
		Rdf_Final = Rdf_Final.Define("jPt_jesDown", "jPt * (1.0 - sqrt(jPt_jesDown_Delta))")
		
#		Rdf_Final = Rdf_Final.Define("jM_uncorr_jesUp", "jM_uncorr * (1.0 + sqrt(jM_jesUp_Delta))")
#		Rdf_Final = Rdf_Final.Define("jM_jesUp", "jM_uncorr_jesUp*JMC_corr(jM_uncorr_jesUp,jPt_jesUp,jEta)")
#		Rdf_Final = Rdf_Final.Define("jM_uncorr_jesDown", "jM_uncorr * (1.0 - sqrt(jM_jesDown_Delta))")
#		Rdf_Final = Rdf_Final.Define("jM_jesDown", "jM_uncorr_jesDown*JMC_corr(jM_uncorr_jesDown,jPt_jesDown,jEta)")

		Rdf_Final = Rdf_Final.Define("jM_uncorr_jesUp", "jM_uncorr * (jPt_jesUp / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_jesUp", "jM * (jPt_jesUp / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_uncorr_jesDown", "jM_uncorr * (jPt_jesDown / jPt)")
		Rdf_Final = Rdf_Final.Define("jM_jesDown", "jM * (jPt_jesDown / jPt)")



	Rdf_Pass = Rdf_Final.Filter("n2ddt<0", "N2DDT Passing Cut")
	pass_events += float(Rdf_Pass.Count().GetValue())
	pass_pass += float(Rdf_Pass.Count().GetValue())
	pass_pass_weight += float(Rdf_Pass.Count().GetValue())*float(sample[1])


	Rdf_Fail = Rdf_Final.Filter("n2ddt>0", "N2DDT Failing Cut")
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

        t2_1 = Rdf_Final.Histo1D(("t2_1", "Thin Softdrop Mass", 200, 0, 200), "jM", "weight")
        t2_1 = t2_1.Clone()
        t2_1.SetTitle("Thin Softdrop Mass")
        t2_1.SetXTitle("Softdrop Mass")
        h2_1.Add(t2_1)

        t2_2 = Rdf_Final.Histo1D(("t2_2", "Thin (Uncorrected) Softdrop Mass", 200, 0, 200), "jM_uncorr", "weight")
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

        t5_1 = Rdf_Final.Histo1D(("t5_1", "Thin Jet pT", 400, 0, 2000), "jPt", "weight")
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
	
	q1 = Rdf_Pass.Histo1D(("q1", "Passing Softdrop Mass", 40, 0, 200), "jM", "weight")
	q1 = q1.Clone()
	q1.SetTitle("Passing Softdrop Mass")
	q1.SetXTitle("Softdrop Mass")
	p1.Add(q1)
	
        q1_1 = Rdf_Pass.Histo1D(("q1_1", "Thin Passing Softdrop Mass", 200, 0, 200), "jM", "weight")
        q1_1 = q1_1.Clone()
        q1_1.SetTitle("Passing Softdrop Mass")
        q1_1.SetXTitle("Softdrop Mass")
        p1_1.Add(q1_1)

        q1_2 = Rdf_Pass.Histo1D(("q1_2", "Thin (Uncorrected) Passing Softdrop Mass", 200, 0, 200), "jM_uncorr", "weight")
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
	
	q3_1 = Rdf_Pass.Histo1D(("q3_1", "THin Passing Jet pT", 400, 0, 2000), "jPt", "weight")
	q3_1 = q3_1.Clone()
	q3_1.SetTitle("Thin Passing Jet pT")
	q3_1.SetXTitle("Jet pT")
	p3_1.Add(q3_1)
		
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
	u1.SetTitle("Failing Softdrop Mass")
	u1.SetXTitle("Softdrop Mass")
	f1.Add(u1)

        u1_1 = Rdf_Fail.Histo1D(("u1_1", "Failing Softdrop Mass", 200, 0, 200), "jM", "weight")
        u1_1 = u1_1.Clone()
        u1_1.SetTitle("Failing Softdrop Mass")
        u1_1.SetXTitle("Softdrop Mass")
        f1_1.Add(u1_1)
	
        u1_2 = Rdf_Fail.Histo1D(("u1_2", "Thin (Uncorrected) Failing Softdrop Mass", 200, 0, 200), "jM_uncorr", "weight")
        u1_2 = u1_2.Clone()
        u1_2.SetTitle("Thin (Uncorrected) Failing Softdrop Mass")
        u1_2.SetXTitle("Softdrop Mass")
        f1_2.Add(u1_2)
	
	u2 = Rdf_Fail.Histo1D(("u2", "Failing Photon pT", 100, 0, 2000), "pPt", "weight")
	u2 = u2.Clone()
	u2.SetTitle("Failing Photon pT")
	u2.SetXTitle("Photon pT")
	f2.Add(u2)
		
	u3 = Rdf_Fail.Histo1D(("u3", "Failing Jet pT", 40, 0, 2000), "jPt", "weight")
	u3 = u3.Clone()
	u3.SetTitle("Failing Jet pT")
	u3.SetXTitle("Jet pT")
	f3.Add(u3)
	
	u3_1 = Rdf_Fail.Histo1D(("u3_1", "Thin Failing Jet pT", 400, 0, 2000), "jPt", "weight")
	u3_1 = u3_1.Clone()
	u3_1.SetTitle("Thin Failing Jet pT")
	u3_1.SetXTitle("Jet pT")
	f3_1.Add(u3_1)
		
	u4 = Rdf_Fail.Histo1D(("u4", "Failing Rho", 28, -8, -1), "Rho", "weight")
	u4 = u4.Clone()
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
		
	j20_1 = Rdf_Final.Histo2D(("pt_n2ddt", "Jet pT vs. N2DDT", 40, 0, 2000, 100, -.5, .5), "jPt", "n2ddt", "weight")
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
	
        j38_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide5_wide", "Passing Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200), "jPt", "jM", "weight")
        j38_w = j38_w.Clone()
        h38_w.Add(j38_w)

        j39_w = Rdf_Final.Histo2D(("pt_soft_tot_wide5_wide", "Total Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200), "jPt", "jM", "weight")
        j39_w = j39_w.Clone()
        h39_w.Add(j39_w)

        j40_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide5_wide", "Failing Jet pT vs. Softdrop Mass", 6, widebins5, 40, 0, 200), "jPt", "jM", "weight")
        j40_w = j40_w.Clone()
        h40_w.Add(j40_w)
        
	j41_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide", "Passing Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight")
        j41_w = j41_w.Clone()
        h41_w.Add(j41_w)

        j42_w = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide", "Total Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight")
        j42_w = j42_w.Clone()
        h42_w.Add(j42_w)

        j43_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide", "Failing Jet pT vs. Softdrop Mass", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight")
        j43_w = j43_w.Clone()
        h43_w.Add(j43_w)

        j44_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide7_wide", "Passing Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200), "jPt", "jM", "weight")
        j44_w = j44_w.Clone()
        h44_w.Add(j44_w)

        j45_w = Rdf_Final.Histo2D(("pt_soft_tot_wide7_wide", "Total Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200), "jPt", "jM", "weight")
        j45_w = j45_w.Clone()
        h45_w.Add(j45_w)

        j46_w = Rdf_Fail.Histo2D(("pt_soft_pass_wide7_wide", "Failing Jet pT vs. Softdrop Mass", 7, widebins7, 40, 0, 200), "jPt", "jM", "weight")
        j46_w = j46_w.Clone()
        h46_w.Add(j46_w)

	j47 = Rdf_Final.Histo1D(("j47", "Number of Good Reconstructed Primary Verticies", 70, 0, 70), "PV_Good", "weight")
	j47 = j47.Clone()
	h47.Add(j47)

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

        j54 = Rdf_Final.Histo1D(("j54", "MET pT", 200, 0, 200), "METpt", "weight")
        j54 = j54.Clone()
        h54.Add(j54)
        j55 = Rdf_Final.Histo1D(("j55", "MET ET", 200, 0, 200), "MET_Et", "weight")
        j55 = j55.Clone()
        h55.Add(j55)
        j56 = Rdf_Final.Histo1D(("j56", "PuppiMET pT", 200, 0, 200), "PuppiMETpt", "weight")
        j56 = j56.Clone()
        h56.Add(j56)
        j57 = Rdf_Final.Histo1D(("j57", "PuppiMET ET", 200, 0, 200), "PuppiMET_sumEt", "weight")
        j57 = j57.Clone()
        h57.Add(j57)

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
	
	j80 = Rdf_Final.Histo1D(("j80", "AK4 HT", 1000, 0, 5000), "jHT", "weight")
        j80 = j80.Clone()
        h80.Add(j80)
	
	j81 = Rdf_Final.Histo1D(("j81", "AK8 HT", 1000, 0, 5000), "jHT_AK8", "weight")
        j81 = j81.Clone()
        h81.Add(j81)
	
	j90 = Rdf_Final.Histo1D(("j90", "AK4 Jet pT", 200, 0, 2000), "jPt_AK4", "weight")
        j90 = j90.Clone()
        h90.Add(j90)
	
	# Systematics Histograms
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
		t2_puUp = Rdf_Final.Histo1D(("t2_puUp", "Softdrop Mass PileUp Up", 40, 0, 200), "jM", "weight_Up")
		t2_puUp = t2_puUp.Clone()
		t2_puUp.SetTitle("Softdrop Mass PileUp Up")
		t2_puUp.SetXTitle("Softdrop Mass")
		h2_puUp.Add(t2_puUp)

        	t2_1_puUp = Rdf_Final.Histo1D(("t2_1_puUp", "Thin Softdrop Mass PileUp Up", 200, 0, 200), "jM", "weight_Up")
        	t2_1_puUp = t2_1_puUp.Clone()
        	t2_1_puUp.SetTitle("Thin Softdrop Mass PileUp Up")
        	t2_1_puUp.SetXTitle("Softdrop Mass")
        	h2_1_puUp.Add(t2_1_puUp)

        	t2_2_puUp = Rdf_Final.Histo1D(("t2_2_puUp", "Thin (Uncorrected) Softdrop Mass PileUp Up", 200, 0, 200), "jM_uncorr", "weight_Up")
        	t2_2_puUp = t2_2_puUp.Clone()
        	t2_2_puUp.SetTitle("Thin (Uncorrected) Softdrop Mass PileUp Up")
        	t2_2_puUp.SetXTitle("Softdrop Mass")
        	h2_2_puUp.Add(t2_2_puUp)
		
		t5_puUp = Rdf_Final.Histo1D(("t5_puUp", "Jet pT PileUp Up", 40, 0, 2000), "jPt", "weight_Up")
		t5_puUp = t5_puUp.Clone()
		t5_puUp.SetTitle("Jet pT PileUp Up")
		t5_puUp.SetXTitle("pT")
		h5_puUp.Add(t5_puUp)

        	t5_1_puUp = Rdf_Final.Histo1D(("t5_1_puUp", "Thin Jet pT PileUp Up", 400, 0, 2000), "jPt", "weight_Up")
        	t5_1_puUp = t5_1_puUp.Clone()
        	t5_1_puUp.SetTitle("Thin Jet pT PileUp Up")
        	t5_1_puUp.SetXTitle("pT")
        	h5_1_puUp.Add(t5_1_puUp)

		t6_puUp = Rdf_Final.Histo1D(("t6_puUp", "Number of Good Reconstructed Primary Verticies PileUp Up", 70, 0, 70), "PV_Good", "weight_Up")
		t6_puUp = t6_puUp.Clone()
		h6_puUp.Add(t6_puUp)

		t2_puDown = Rdf_Final.Histo1D(("t2_puDown", "Softdrop Mass PileUp Down", 40, 0, 200), "jM", "weight_Down")
		t2_puDown = t2_puDown.Clone()
		t2_puDown.SetTitle("Softdrop Mass PileUp Down")
		t2_puDown.SetXTitle("Softdrop Mass")
		h2_puDown.Add(t2_puDown)

        	t2_1_puDown = Rdf_Final.Histo1D(("t2_1_puDown", "Thin Softdrop Mass PileUp Down", 200, 0, 200), "jM", "weight_Down")
        	t2_1_puDown = t2_1_puDown.Clone()
        	t2_1_puDown.SetTitle("Thin Softdrop Mass PileUp Down")
        	t2_1_puDown.SetXTitle("Softdrop Mass")
        	h2_1_puDown.Add(t2_1_puDown)

        	t2_2_puDown = Rdf_Final.Histo1D(("t2_2_puDown", "Thin (Uncorrected) Softdrop Mass PileUp Down", 200, 0, 200), "jM_uncorr", "weight_Down")
        	t2_2_puDown = t2_2_puDown.Clone()
        	t2_2_puDown.SetTitle("Thin (Uncorrected) Softdrop Mass PileUp Down")
        	t2_2_puDown.SetXTitle("Softdrop Mass")
        	h2_2_puDown.Add(t2_2_puDown)
		
		t5_puDown = Rdf_Final.Histo1D(("t5_puDown", "Jet pT PileUp Down", 40, 0, 2000), "jPt", "weight_Down")
		t5_puDown = t5_puDown.Clone()
		t5_puDown.SetTitle("Jet pT PileUp Down")
		t5_puDown.SetXTitle("pT")
		h5_puDown.Add(t5_puDown)

        	t5_1_puDown = Rdf_Final.Histo1D(("t5_1_puDown", "Thin Jet pT PileUp Down", 400, 0, 2000), "jPt", "weight_Down")
        	t5_1_puDown = t5_1_puDown.Clone()
        	t5_1_puDown.SetTitle("Thin Jet pT PileUp Down")
        	t5_1_puDown.SetXTitle("pT")
        	h5_1_puDown.Add(t5_1_puDown)
		
		t6_puDown = Rdf_Final.Histo1D(("t6_puDown", "Number of Good Reconstructed Primary Verticies PileUp Down", 70, 0, 70), "PV_Good", "weight_Down")
		t6_puDown = t6_puDown.Clone()
		h6_puDown.Add(t6_puDown)
		
		t2_jerUp = Rdf_Final.Histo1D(("t2_jerUp", "Softdrop Mass JER Up", 40, 0, 200), "jM_jerUp", "weight")
		t2_jerUp = t2_jerUp.Clone()
		t2_jerUp.SetTitle("Softdrop Mass JER Up")
		t2_jerUp.SetXTitle("Softdrop Mass")
		h2_jerUp.Add(t2_jerUp)

        	t2_1_jerUp = Rdf_Final.Histo1D(("t2_1_jerUp", "Thin Softdrop Mass JER Up", 200, 0, 200), "jM_jerUp", "weight")
        	t2_1_jerUp = t2_1_jerUp.Clone()
        	t2_1_jerUp.SetTitle("Thin Softdrop Mass JER Up")
        	t2_1_jerUp.SetXTitle("Softdrop Mass")
        	h2_1_jerUp.Add(t2_1_jerUp)

        	t2_2_jerUp = Rdf_Final.Histo1D(("t2_2_jerUp", "Thin (Uncorrected) Softdrop Mass JER Up", 200, 0, 200), "jM_uncorr_jerUp", "weight")
        	t2_2_jerUp = t2_2_jerUp.Clone()
        	t2_2_jerUp.SetTitle("Thin (Uncorrected) Softdrop Mass JER Up")
        	t2_2_jerUp.SetXTitle("Softdrop Mass")
        	h2_2_jerUp.Add(t2_2_jerUp)
		
		t5_jerUp = Rdf_Final.Histo1D(("t5_jerUp", "Jet pT JER Up", 40, 0, 2000), "jPt_jerUp", "weight")
		t5_jerUp = t5_jerUp.Clone()
		t5_jerUp.SetTitle("Jet pT JER Up")
		t5_jerUp.SetXTitle("pT")
		h5_jerUp.Add(t5_jerUp)

        	t5_1_jerUp = Rdf_Final.Histo1D(("t5_1_jerUp", "Thin Jet pT JER Up", 400, 0, 2000), "jPt_jerUp", "weight")
        	t5_1_jerUp = t5_1_jerUp.Clone()
        	t5_1_jerUp.SetTitle("Thin Jet pT JER Up")
        	t5_1_jerUp.SetXTitle("pT")
        	h5_1_jerUp.Add(t5_1_jerUp)

		t2_jerDown = Rdf_Final.Histo1D(("t2_jerDown", "Softdrop Mass JER Down", 40, 0, 200), "jM_jerDown", "weight")
		t2_jerDown = t2_jerDown.Clone()
		t2_jerDown.SetTitle("Softdrop Mass JER Down")
		t2_jerDown.SetXTitle("Softdrop Mass")
		h2_jerDown.Add(t2_jerDown)

        	t2_1_jerDown = Rdf_Final.Histo1D(("t2_1_jerDown", "Thin Softdrop Mass JER Down", 200, 0, 200), "jM_jerDown", "weight")
        	t2_1_jerDown = t2_1_jerDown.Clone()
        	t2_1_jerDown.SetTitle("Thin Softdrop Mass JER Down")
        	t2_1_jerDown.SetXTitle("Softdrop Mass")
        	h2_1_jerDown.Add(t2_1_jerDown)

        	t2_2_jerDown = Rdf_Final.Histo1D(("t2_2_jerDown", "Thin (Uncorrected) Softdrop Mass JER Down", 200, 0, 200), "jM_uncorr_jerDown", "weight")
        	t2_2_jerDown = t2_2_jerDown.Clone()
        	t2_2_jerDown.SetTitle("Thin (Uncorrected) Softdrop Mass JER Down")
        	t2_2_jerDown.SetXTitle("Softdrop Mass")
        	h2_2_jerDown.Add(t2_2_jerDown)
		
		t5_jerDown = Rdf_Final.Histo1D(("t5_jerDown", "Jet pT JER Down", 40, 0, 2000), "jPt_jerDown", "weight")
		t5_jerDown = t5_jerDown.Clone()
		t5_jerDown.SetTitle("Jet pT JER Down")
		t5_jerDown.SetXTitle("pT")
		h5_jerDown.Add(t5_jerDown)

        	t5_1_jerDown = Rdf_Final.Histo1D(("t5_1_jerDown", "Thin Jet pT JER Down", 400, 0, 2000), "jPt_jerDown", "weight")
        	t5_1_jerDown = t5_1_jerDown.Clone()
        	t5_1_jerDown.SetTitle("Thin Jet pT JER Down")
        	t5_1_jerDown.SetXTitle("pT")
        	h5_1_jerDown.Add(t5_1_jerDown)
		
		
		t2_jesUp = Rdf_Final.Histo1D(("t2_jesUp", "Softdrop Mass JES Up", 40, 0, 200), "jM_jesUp", "weight")
		t2_jesUp = t2_jesUp.Clone()
		t2_jesUp.SetTitle("Softdrop Mass JES Up")
		t2_jesUp.SetXTitle("Softdrop Mass")
		h2_jesUp.Add(t2_jesUp)

        	t2_1_jesUp = Rdf_Final.Histo1D(("t2_1_jesUp", "Thin Softdrop Mass JES Up", 200, 0, 200), "jM_jesUp", "weight")
        	t2_1_jesUp = t2_1_jesUp.Clone()
        	t2_1_jesUp.SetTitle("Thin Softdrop Mass JES Up")
        	t2_1_jesUp.SetXTitle("Softdrop Mass")
        	h2_1_jesUp.Add(t2_1_jesUp)

        	t2_2_jesUp = Rdf_Final.Histo1D(("t2_2_jesUp", "Thin (Uncorrected) Softdrop Mass JES Up", 200, 0, 200), "jM_uncorr_jesUp", "weight")
        	t2_2_jesUp = t2_2_jesUp.Clone()
        	t2_2_jesUp.SetTitle("Thin (Uncorrected) Softdrop Mass JES Up")
        	t2_2_jesUp.SetXTitle("Softdrop Mass")
        	h2_2_jesUp.Add(t2_2_jesUp)
		
		t5_jesUp = Rdf_Final.Histo1D(("t5_jesUp", "Jet pT JES Up", 40, 0, 2000), "jPt_jesUp", "weight")
		t5_jesUp = t5_jesUp.Clone()
		t5_jesUp.SetTitle("Jet pT JES Up")
		t5_jesUp.SetXTitle("pT")
		h5_jesUp.Add(t5_jesUp)

        	t5_1_jesUp = Rdf_Final.Histo1D(("t5_1_jesUp", "Thin Jet pT JES Up", 400, 0, 2000), "jPt_jesUp", "weight")
        	t5_1_jesUp = t5_1_jesUp.Clone()
        	t5_1_jesUp.SetTitle("Thin Jet pT JES Up")
        	t5_1_jesUp.SetXTitle("pT")
        	h5_1_jesUp.Add(t5_1_jesUp)

		t2_jesDown = Rdf_Final.Histo1D(("t2_jesDown", "Softdrop Mass JES Down", 40, 0, 200), "jM_jesDown", "weight")
		t2_jesDown = t2_jesDown.Clone()
		t2_jesDown.SetTitle("Softdrop Mass JES Down")
		t2_jesDown.SetXTitle("Softdrop Mass")
		h2_jesDown.Add(t2_jesDown)

        	t2_1_jesDown = Rdf_Final.Histo1D(("t2_1_jesDown", "Thin Softdrop Mass JES Down", 200, 0, 200), "jM_jesDown", "weight")
        	t2_1_jesDown = t2_1_jesDown.Clone()
        	t2_1_jesDown.SetTitle("Thin Softdrop Mass JES Down")
        	t2_1_jesDown.SetXTitle("Softdrop Mass")
        	h2_1_jesDown.Add(t2_1_jesDown)

        	t2_2_jesDown = Rdf_Final.Histo1D(("t2_2_jesDown", "Thin (Uncorrected) Softdrop Mass JES Down", 200, 0, 200), "jM_uncorr_jesDown", "weight")
        	t2_2_jesDown = t2_2_jesDown.Clone()
        	t2_2_jesDown.SetTitle("Thin (Uncorrected) Softdrop Mass JES Down")
        	t2_2_jesDown.SetXTitle("Softdrop Mass")
        	h2_2_jesDown.Add(t2_2_jesDown)
		
		t5_jesDown = Rdf_Final.Histo1D(("t5_jesDown", "Jet pT JES Down", 40, 0, 2000), "jPt_jesDown", "weight")
		t5_jesDown = t5_jesDown.Clone()
		t5_jesDown.SetTitle("Jet pT JES Down")
		t5_jesDown.SetXTitle("pT")
		h5_jesDown.Add(t5_jesDown)

        	t5_1_jesDown = Rdf_Final.Histo1D(("t5_1_jesDown", "Thin Jet pT JES Down", 400, 0, 2000), "jPt_jesDown", "weight")
        	t5_1_jesDown = t5_1_jesDown.Clone()
        	t5_1_jesDown.SetTitle("Thin Jet pT JES Down")
        	t5_1_jesDown.SetXTitle("pT")
        	h5_1_jesDown.Add(t5_1_jesDown)
		
		
		q1_puUp = Rdf_Pass.Histo1D(("q1_puUp", "Passing Softdrop Mass PileUp Up", 40, 0, 200), "jM", "weight_Up")
		q1_puUp = q1_puUp.Clone()
		q1_puUp.SetTitle("Passing Softdrop Mass PileUp Up")
		q1_puUp.SetXTitle("Softdrop Mass")
		p1_puUp.Add(q1_puUp)
	
	        q1_1_puUp = Rdf_Pass.Histo1D(("q1_1_puUp", "Thin Passing Softdrop Mass PileUp Up", 200, 0, 200), "jM", "weight_Up")
	        q1_1_puUp = q1_1_puUp.Clone()
	        q1_1_puUp.SetTitle("Passing Softdrop Mass PileUp Up")
       		q1_1_puUp.SetXTitle("Softdrop Mass")
        	p1_1_puUp.Add(q1_1_puUp)

        	q1_2_puUp = Rdf_Pass.Histo1D(("q1_2_puUp", "Thin (Uncorrected) Passing Softdrop Mass PileUp Up", 200, 0, 200), "jM_uncorr", "weight_Up")
        	q1_2_puUp = q1_2_puUp.Clone()
        	q1_2_puUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass PileUp Up")
        	q1_2_puUp.SetXTitle("Softdrop Mass")
        	p1_2_puUp.Add(q1_2_puUp)
		
		q3_puUp = Rdf_Pass.Histo1D(("q3_puUp", "Passing Jet pT PileUp Up", 40, 0, 2000), "jPt", "weight_Up")
		q3_puUp = q3_puUp.Clone()
		q3_puUp.SetTitle("Passing Jet pT")
		q3_puUp.SetXTitle("Jet pT")
		p3_puUp.Add(q3_puUp)
	
		q3_1_puUp = Rdf_Pass.Histo1D(("q3_1_puUp", "Thin Passing Jet pT PileUp Up", 400, 0, 2000), "jPt", "weight_Up")
		q3_1_puUp = q3_1_puUp.Clone()
		q3_1_puUp.SetTitle("Thin Passing Jet pT PileUp Up")
		q3_1_puUp.SetXTitle("Jet pT")
		p3_1_puUp.Add(q3_1_puUp)
		
		u1_puUp = Rdf_Fail.Histo1D(("u1_puUp", "Failing Softdrop Mass PileUp Up", 40, 0, 200), "jM", "weight_Up")
		u1_puUp = u1_puUp.Clone()
		u1_puUp.SetTitle("Failing Softdrop Mass PileUp Up")
		u1_puUp.SetXTitle("Softdrop Mass PileUp Up")
		f1_puUp.Add(u1_puUp)

	        u1_1_puUp = Rdf_Fail.Histo1D(("u1_1_puUp", "Failing Softdrop Mass PileUp Up", 200, 0, 200), "jM", "weight_Up")
	        u1_1_puUp = u1_1_puUp.Clone()
	        u1_1_puUp.SetTitle("Failing Softdrop Mass PileUp Up")
	        u1_1_puUp.SetXTitle("Softdrop Mass")
	        f1_1_puUp.Add(u1_1_puUp)
	
	        u1_2_puUp = Rdf_Fail.Histo1D(("u1_2_puUp", "Thin (Uncorrected) Failing Softdrop Mass PileUp Up", 200, 0, 200), "jM_uncorr", "weight_Up")
	        u1_2_puUp = u1_2_puUp.Clone()
	        u1_2_puUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass PileUp Up")
	        u1_2_puUp.SetXTitle("Softdrop Mass")
	        f1_2_puUp.Add(u1_2_puUp)

		u3_puUp = Rdf_Fail.Histo1D(("u3_puUp", "Failing Jet pT PileUp Up", 40, 0, 2000), "jPt", "weight_Up")
		u3_puUp = u3_puUp.Clone()
		u3_puUp.SetTitle("Failing Jet pT PileUp Up")
		u3_puUp.SetXTitle("Jet pT")
		f3_puUp.Add(u3_puUp)
	
		u3_1_puUp = Rdf_Fail.Histo1D(("u3_1_puUp", "Thin Failing Jet pT PileUp Up", 400, 0, 2000), "jPt", "weight_Up")
		u3_1_puUp = u3_1_puUp.Clone()
		u3_1_puUp.SetTitle("Thin Failing Jet pT PileUp Up")
		u3_1_puUp.SetXTitle("Jet pT")
		f3_1_puUp.Add(u3_1_puUp)


		q1_puDown = Rdf_Pass.Histo1D(("q1_puDown", "Passing Softdrop Mass PileUp Down", 40, 0, 200), "jM", "weight_Down")
		q1_puDown = q1_puDown.Clone()
		q1_puDown.SetTitle("Passing Softdrop Mass PileUp Down")
		q1_puDown.SetXTitle("Softdrop Mass")
		p1_puDown.Add(q1_puDown)
	
	        q1_1_puDown = Rdf_Pass.Histo1D(("q1_1_puDown", "Thin Passing Softdrop Mass PileUp Down", 200, 0, 200), "jM", "weight_Down")
	        q1_1_puDown = q1_1_puDown.Clone()
	        q1_1_puDown.SetTitle("Passing Softdrop Mass PileUp Down")
       		q1_1_puDown.SetXTitle("Softdrop Mass")
        	p1_1_puDown.Add(q1_1_puDown)

        	q1_2_puDown = Rdf_Pass.Histo1D(("q1_2_puDown", "Thin (Uncorrected) Passing Softdrop Mass PileUp Down", 200, 0, 200), "jM_uncorr", "weight_Down")
        	q1_2_puDown = q1_2_puDown.Clone()
        	q1_2_puDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass PileUp Down")
        	q1_2_puDown.SetXTitle("Softdrop Mass")
        	p1_2_puDown.Add(q1_2_puDown)
		
		q3_puDown = Rdf_Pass.Histo1D(("q3_puDown", "Passing Jet pT PileUp Down", 40, 0, 2000), "jPt", "weight_Down")
		q3_puDown = q3_puDown.Clone()
		q3_puDown.SetTitle("Passing Jet pT")
		q3_puDown.SetXTitle("Jet pT")
		p3_puDown.Add(q3_puDown)
	
		q3_1_puDown = Rdf_Pass.Histo1D(("q3_1_puDown", "Thin Passing Jet pT PileUp Down", 400, 0, 2000), "jPt", "weight_Down")
		q3_1_puDown = q3_1_puDown.Clone()
		q3_1_puDown.SetTitle("Thin Passing Jet pT PileUp Down")
		q3_1_puDown.SetXTitle("Jet pT")
		p3_1_puDown.Add(q3_1_puDown)
		
		u1_puDown = Rdf_Fail.Histo1D(("u1_puDown", "Failing Softdrop Mass PileUp Down", 40, 0, 200), "jM", "weight_Down")
		u1_puDown = u1_puDown.Clone()
		u1_puDown.SetTitle("Failing Softdrop Mass PileUp Down")
		u1_puDown.SetXTitle("Softdrop Mass PileUp Down")
		f1_puDown.Add(u1_puDown)

	        u1_1_puDown = Rdf_Fail.Histo1D(("u1_1_puDown", "Failing Softdrop Mass PileUp Down", 200, 0, 200), "jM", "weight_Down")
	        u1_1_puDown = u1_1_puDown.Clone()
	        u1_1_puDown.SetTitle("Failing Softdrop Mass PileUp Down")
	        u1_1_puDown.SetXTitle("Softdrop Mass")
	        f1_1_puDown.Add(u1_1_puDown)
	
	        u1_2_puDown = Rdf_Fail.Histo1D(("u1_2_puDown", "Thin (Uncorrected) Failing Softdrop Mass PileUp Down", 200, 0, 200), "jM_uncorr", "weight_Down")
	        u1_2_puDown = u1_2_puDown.Clone()
	        u1_2_puDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass PileUp Down")
	        u1_2_puDown.SetXTitle("Softdrop Mass")
	        f1_2_puDown.Add(u1_2_puDown)

		u3_puDown = Rdf_Fail.Histo1D(("u3_puDown", "Failing Jet pT PileUp Down", 40, 0, 2000), "jPt", "weight_Down")
		u3_puDown = u3_puDown.Clone()
		u3_puDown.SetTitle("Failing Jet pT PileUp Down")
		u3_puDown.SetXTitle("Jet pT")
		f3_puDown.Add(u3_puDown)
	
		u3_1_puDown = Rdf_Fail.Histo1D(("u3_1_puDown", "Thin Failing Jet pT PileUp Down", 400, 0, 2000), "jPt", "weight_Down")
		u3_1_puDown = u3_1_puDown.Clone()
		u3_1_puDown.SetTitle("Thin Failing Jet pT PileUp Down")
		u3_1_puDown.SetXTitle("Jet pT")
		f3_1_puDown.Add(u3_1_puDown)


		q1_jerUp = Rdf_Pass.Histo1D(("q1_jerUp", "Passing Softdrop Mass JER Up", 40, 0, 200), "jM_jerUp", "weight")
		q1_jerUp = q1_jerUp.Clone()
		q1_jerUp.SetTitle("Passing Softdrop Mass JER Up")
		q1_jerUp.SetXTitle("Softdrop Mass")
		p1_jerUp.Add(q1_jerUp)
	
	        q1_1_jerUp = Rdf_Pass.Histo1D(("q1_1_jerUp", "Thin Passing Softdrop Mass JER Up", 200, 0, 200), "jM_jerUp", "weight")
	        q1_1_jerUp = q1_1_jerUp.Clone()
	        q1_1_jerUp.SetTitle("Passing Softdrop Mass JER Up")
       		q1_1_jerUp.SetXTitle("Softdrop Mass")
        	p1_1_jerUp.Add(q1_1_jerUp)

        	q1_2_jerUp = Rdf_Pass.Histo1D(("q1_2_jerUp", "Thin (Uncorrected) Passing Softdrop Mass JER Up", 200, 0, 200), "jM_uncorr_jerUp", "weight")
        	q1_2_jerUp = q1_2_jerUp.Clone()
        	q1_2_jerUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Up")
        	q1_2_jerUp.SetXTitle("Softdrop Mass")
        	p1_2_jerUp.Add(q1_2_jerUp)
		
		q3_jerUp = Rdf_Pass.Histo1D(("q3_jerUp", "Passing Jet pT JER Up", 40, 0, 2000), "jPt_jerUp", "weight")
		q3_jerUp = q3_jerUp.Clone()
		q3_jerUp.SetTitle("Passing Jet pT")
		q3_jerUp.SetXTitle("Jet pT")
		p3_jerUp.Add(q3_jerUp)
	
		q3_1_jerUp = Rdf_Pass.Histo1D(("q3_1_jerUp", "Thin Passing Jet pT JER Up", 400, 0, 2000), "jPt_jerUp", "weight")
		q3_1_jerUp = q3_1_jerUp.Clone()
		q3_1_jerUp.SetTitle("Thin Passing Jet pT JER Up")
		q3_1_jerUp.SetXTitle("Jet pT")
		p3_1_jerUp.Add(q3_1_jerUp)
		
		u1_jerUp = Rdf_Fail.Histo1D(("u1_jerUp", "Failing Softdrop Mass JER Up", 40, 0, 200), "jM_jerUp", "weight")
		u1_jerUp = u1_jerUp.Clone()
		u1_jerUp.SetTitle("Failing Softdrop Mass JER Up")
		u1_jerUp.SetXTitle("Softdrop Mass JER Up")
		f1_jerUp.Add(u1_jerUp)

	        u1_1_jerUp = Rdf_Fail.Histo1D(("u1_1_jerUp", "Failing Softdrop Mass JER Up", 200, 0, 200), "jM_jerUp", "weight")
	        u1_1_jerUp = u1_1_jerUp.Clone()
	        u1_1_jerUp.SetTitle("Failing Softdrop Mass JER Up")
	        u1_1_jerUp.SetXTitle("Softdrop Mass")
	        f1_1_jerUp.Add(u1_1_jerUp)
	
	        u1_2_jerUp = Rdf_Fail.Histo1D(("u1_2_jerUp", "Thin (Uncorrected) Failing Softdrop Mass JER Up", 200, 0, 200), "jM_uncorr_jerUp", "weight")
	        u1_2_jerUp = u1_2_jerUp.Clone()
	        u1_2_jerUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Up")
	        u1_2_jerUp.SetXTitle("Softdrop Mass")
	        f1_2_jerUp.Add(u1_2_jerUp)

		u3_jerUp = Rdf_Fail.Histo1D(("u3_jerUp", "Failing Jet pT JER Up", 40, 0, 2000), "jPt_jerUp", "weight")
		u3_jerUp = u3_jerUp.Clone()
		u3_jerUp.SetTitle("Failing Jet pT JER Up")
		u3_jerUp.SetXTitle("Jet pT")
		f3_jerUp.Add(u3_jerUp)
	
		u3_1_jerUp = Rdf_Fail.Histo1D(("u3_1_jerUp", "Thin Failing Jet pT JER Up", 400, 0, 2000), "jPt_jerUp", "weight")
		u3_1_jerUp = u3_1_jerUp.Clone()
		u3_1_jerUp.SetTitle("Thin Failing Jet pT JER Up")
		u3_1_jerUp.SetXTitle("Jet pT")
		f3_1_jerUp.Add(u3_1_jerUp)


		q1_jerDown = Rdf_Pass.Histo1D(("q1_jerDown", "Passing Softdrop Mass JER Down", 40, 0, 200), "jM_jerDown", "weight")
		q1_jerDown = q1_jerDown.Clone()
		q1_jerDown.SetTitle("Passing Softdrop Mass JER Down")
		q1_jerDown.SetXTitle("Softdrop Mass")
		p1_jerDown.Add(q1_jerDown)
	
	        q1_1_jerDown = Rdf_Pass.Histo1D(("q1_1_jerDown", "Thin Passing Softdrop Mass JER Down", 200, 0, 200), "jM_jerDown", "weight")
	        q1_1_jerDown = q1_1_jerDown.Clone()
	        q1_1_jerDown.SetTitle("Passing Softdrop Mass JER Down")
       		q1_1_jerDown.SetXTitle("Softdrop Mass")
        	p1_1_jerDown.Add(q1_1_jerDown)

        	q1_2_jerDown = Rdf_Pass.Histo1D(("q1_2_jerDown", "Thin (Uncorrected) Passing Softdrop Mass JER Down", 200, 0, 200), "jM_uncorr_jerDown", "weight")
        	q1_2_jerDown = q1_2_jerDown.Clone()
        	q1_2_jerDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Down")
        	q1_2_jerDown.SetXTitle("Softdrop Mass")
        	p1_2_jerDown.Add(q1_2_jerDown)
		
		q3_jerDown = Rdf_Pass.Histo1D(("q3_jerDown", "Passing Jet pT JER Down", 40, 0, 2000), "jPt_jerDown", "weight")
		q3_jerDown = q3_jerDown.Clone()
		q3_jerDown.SetTitle("Passing Jet pT")
		q3_jerDown.SetXTitle("Jet pT")
		p3_jerDown.Add(q3_jerDown)
	
		q3_1_jerDown = Rdf_Pass.Histo1D(("q3_1_jerDown", "Thin Passing Jet pT JER Down", 400, 0, 2000), "jPt_jerDown", "weight")
		q3_1_jerDown = q3_1_jerDown.Clone()
		q3_1_jerDown.SetTitle("Thin Passing Jet pT JER Down")
		q3_1_jerDown.SetXTitle("Jet pT")
		p3_1_jerDown.Add(q3_1_jerDown)
		
		u1_jerDown = Rdf_Fail.Histo1D(("u1_jerDown", "Failing Softdrop Mass JER Down", 40, 0, 200), "jM_jerDown", "weight")
		u1_jerDown = u1_jerDown.Clone()
		u1_jerDown.SetTitle("Failing Softdrop Mass JER Down")
		u1_jerDown.SetXTitle("Softdrop Mass JER Down")
		f1_jerDown.Add(u1_jerDown)

	        u1_1_jerDown = Rdf_Fail.Histo1D(("u1_1_jerDown", "Failing Softdrop Mass JER Down", 200, 0, 200), "jM_jerDown", "weight")
	        u1_1_jerDown = u1_1_jerDown.Clone()
	        u1_1_jerDown.SetTitle("Failing Softdrop Mass JER Down")
	        u1_1_jerDown.SetXTitle("Softdrop Mass")
	        f1_1_jerDown.Add(u1_1_jerDown)
	
	        u1_2_jerDown = Rdf_Fail.Histo1D(("u1_2_jerDown", "Thin (Uncorrected) Failing Softdrop Mass JER Down", 200, 0, 200), "jM_uncorr_jerDown", "weight")
	        u1_2_jerDown = u1_2_jerDown.Clone()
	        u1_2_jerDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Down")
	        u1_2_jerDown.SetXTitle("Softdrop Mass")
	        f1_2_jerDown.Add(u1_2_jerDown)

		u3_jerDown = Rdf_Fail.Histo1D(("u3_jerDown", "Failing Jet pT JER Down", 40, 0, 2000), "jPt_jerDown", "weight")
		u3_jerDown = u3_jerDown.Clone()
		u3_jerDown.SetTitle("Failing Jet pT JER Down")
		u3_jerDown.SetXTitle("Jet pT")
		f3_jerDown.Add(u3_jerDown)
	
		u3_1_jerDown = Rdf_Fail.Histo1D(("u3_1_jerDown", "Thin Failing Jet pT JER Down", 400, 0, 2000), "jPt_jerDown", "weight")
		u3_1_jerDown = u3_1_jerDown.Clone()
		u3_1_jerDown.SetTitle("Thin Failing Jet pT JER Down")
		u3_1_jerDown.SetXTitle("Jet pT")
		f3_1_jerDown.Add(u3_1_jerDown)


		q1_jesUp = Rdf_Pass.Histo1D(("q1_jesUp", "Passing Softdrop Mass JER Up", 40, 0, 200), "jM_jesUp", "weight")
		q1_jesUp = q1_jesUp.Clone()
		q1_jesUp.SetTitle("Passing Softdrop Mass JER Up")
		q1_jesUp.SetXTitle("Softdrop Mass")
		p1_jesUp.Add(q1_jesUp)
	
	        q1_1_jesUp = Rdf_Pass.Histo1D(("q1_1_jesUp", "Thin Passing Softdrop Mass JER Up", 200, 0, 200), "jM_jesUp", "weight")
	        q1_1_jesUp = q1_1_jesUp.Clone()
	        q1_1_jesUp.SetTitle("Passing Softdrop Mass JER Up")
       		q1_1_jesUp.SetXTitle("Softdrop Mass")
        	p1_1_jesUp.Add(q1_1_jesUp)

        	q1_2_jesUp = Rdf_Pass.Histo1D(("q1_2_jesUp", "Thin (Uncorrected) Passing Softdrop Mass JER Up", 200, 0, 200), "jM_uncorr_jesUp", "weight")
        	q1_2_jesUp = q1_2_jesUp.Clone()
        	q1_2_jesUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Up")
        	q1_2_jesUp.SetXTitle("Softdrop Mass")
        	p1_2_jesUp.Add(q1_2_jesUp)
		
		q3_jesUp = Rdf_Pass.Histo1D(("q3_jesUp", "Passing Jet pT JER Up", 40, 0, 2000), "jPt_jesUp", "weight")
		q3_jesUp = q3_jesUp.Clone()
		q3_jesUp.SetTitle("Passing Jet pT")
		q3_jesUp.SetXTitle("Jet pT")
		p3_jesUp.Add(q3_jesUp)
	
		q3_1_jesUp = Rdf_Pass.Histo1D(("q3_1_jesUp", "Thin Passing Jet pT JER Up", 400, 0, 2000), "jPt_jesUp", "weight")
		q3_1_jesUp = q3_1_jesUp.Clone()
		q3_1_jesUp.SetTitle("Thin Passing Jet pT JER Up")
		q3_1_jesUp.SetXTitle("Jet pT")
		p3_1_jesUp.Add(q3_1_jesUp)
		
		u1_jesUp = Rdf_Fail.Histo1D(("u1_jesUp", "Failing Softdrop Mass JER Up", 40, 0, 200), "jM_jesUp", "weight")
		u1_jesUp = u1_jesUp.Clone()
		u1_jesUp.SetTitle("Failing Softdrop Mass JER Up")
		u1_jesUp.SetXTitle("Softdrop Mass JER Up")
		f1_jesUp.Add(u1_jesUp)

	        u1_1_jesUp = Rdf_Fail.Histo1D(("u1_1_jesUp", "Failing Softdrop Mass JER Up", 200, 0, 200), "jM_jesUp", "weight")
	        u1_1_jesUp = u1_1_jesUp.Clone()
	        u1_1_jesUp.SetTitle("Failing Softdrop Mass JER Up")
	        u1_1_jesUp.SetXTitle("Softdrop Mass")
	        f1_1_jesUp.Add(u1_1_jesUp)
	
	        u1_2_jesUp = Rdf_Fail.Histo1D(("u1_2_jesUp", "Thin (Uncorrected) Failing Softdrop Mass JER Up", 200, 0, 200), "jM_uncorr_jesUp", "weight")
	        u1_2_jesUp = u1_2_jesUp.Clone()
	        u1_2_jesUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Up")
	        u1_2_jesUp.SetXTitle("Softdrop Mass")
	        f1_2_jesUp.Add(u1_2_jesUp)

		u3_jesUp = Rdf_Fail.Histo1D(("u3_jesUp", "Failing Jet pT JER Up", 40, 0, 2000), "jPt_jesUp", "weight")
		u3_jesUp = u3_jesUp.Clone()
		u3_jesUp.SetTitle("Failing Jet pT JER Up")
		u3_jesUp.SetXTitle("Jet pT")
		f3_jesUp.Add(u3_jesUp)
	
		u3_1_jesUp = Rdf_Fail.Histo1D(("u3_1_jesUp", "Thin Failing Jet pT JER Up", 400, 0, 2000), "jPt_jesUp", "weight")
		u3_1_jesUp = u3_1_jesUp.Clone()
		u3_1_jesUp.SetTitle("Thin Failing Jet pT JER Up")
		u3_1_jesUp.SetXTitle("Jet pT")
		f3_1_jesUp.Add(u3_1_jesUp)


		q1_jesDown = Rdf_Pass.Histo1D(("q1_jesDown", "Passing Softdrop Mass JER Down", 40, 0, 200), "jM_jesDown", "weight")
		q1_jesDown = q1_jesDown.Clone()
		q1_jesDown.SetTitle("Passing Softdrop Mass JER Down")
		q1_jesDown.SetXTitle("Softdrop Mass")
		p1_jesDown.Add(q1_jesDown)
	
	        q1_1_jesDown = Rdf_Pass.Histo1D(("q1_1_jesDown", "Thin Passing Softdrop Mass JER Down", 200, 0, 200), "jM_jesDown", "weight")
	        q1_1_jesDown = q1_1_jesDown.Clone()
	        q1_1_jesDown.SetTitle("Passing Softdrop Mass JER Down")
       		q1_1_jesDown.SetXTitle("Softdrop Mass")
        	p1_1_jesDown.Add(q1_1_jesDown)

        	q1_2_jesDown = Rdf_Pass.Histo1D(("q1_2_jesDown", "Thin (Uncorrected) Passing Softdrop Mass JER Down", 200, 0, 200), "jM_uncorr_jesDown", "weight")
        	q1_2_jesDown = q1_2_jesDown.Clone()
        	q1_2_jesDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Down")
        	q1_2_jesDown.SetXTitle("Softdrop Mass")
        	p1_2_jesDown.Add(q1_2_jesDown)
		
		q3_jesDown = Rdf_Pass.Histo1D(("q3_jesDown", "Passing Jet pT JER Down", 40, 0, 2000), "jPt_jesDown", "weight")
		q3_jesDown = q3_jesDown.Clone()
		q3_jesDown.SetTitle("Passing Jet pT")
		q3_jesDown.SetXTitle("Jet pT")
		p3_jesDown.Add(q3_jesDown)
	
		q3_1_jesDown = Rdf_Pass.Histo1D(("q3_1_jesDown", "Thin Passing Jet pT JER Down", 400, 0, 2000), "jPt_jesDown", "weight")
		q3_1_jesDown = q3_1_jesDown.Clone()
		q3_1_jesDown.SetTitle("Thin Passing Jet pT JER Down")
		q3_1_jesDown.SetXTitle("Jet pT")
		p3_1_jesDown.Add(q3_1_jesDown)
		
		u1_jesDown = Rdf_Fail.Histo1D(("u1_jesDown", "Failing Softdrop Mass JER Down", 40, 0, 200), "jM_jesDown", "weight")
		u1_jesDown = u1_jesDown.Clone()
		u1_jesDown.SetTitle("Failing Softdrop Mass JER Down")
		u1_jesDown.SetXTitle("Softdrop Mass JER Down")
		f1_jesDown.Add(u1_jesDown)

	        u1_1_jesDown = Rdf_Fail.Histo1D(("u1_1_jesDown", "Failing Softdrop Mass JER Down", 200, 0, 200), "jM_jesDown", "weight")
	        u1_1_jesDown = u1_1_jesDown.Clone()
	        u1_1_jesDown.SetTitle("Failing Softdrop Mass JER Down")
	        u1_1_jesDown.SetXTitle("Softdrop Mass")
	        f1_1_jesDown.Add(u1_1_jesDown)
	
	        u1_2_jesDown = Rdf_Fail.Histo1D(("u1_2_jesDown", "Thin (Uncorrected) Failing Softdrop Mass JER Down", 200, 0, 200), "jM_uncorr_jesDown", "weight")
	        u1_2_jesDown = u1_2_jesDown.Clone()
	        u1_2_jesDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Down")
	        u1_2_jesDown.SetXTitle("Softdrop Mass")
	        f1_2_jesDown.Add(u1_2_jesDown)

		u3_jesDown = Rdf_Fail.Histo1D(("u3_jesDown", "Failing Jet pT JER Down", 40, 0, 2000), "jPt_jesDown", "weight")
		u3_jesDown = u3_jesDown.Clone()
		u3_jesDown.SetTitle("Failing Jet pT JER Down")
		u3_jesDown.SetXTitle("Jet pT")
		f3_jesDown.Add(u3_jesDown)
	
		u3_1_jesDown = Rdf_Fail.Histo1D(("u3_1_jesDown", "Thin Failing Jet pT JER Down", 400, 0, 2000), "jPt_jesDown", "weight")
		u3_1_jesDown = u3_1_jesDown.Clone()
		u3_1_jesDown.SetTitle("Thin Failing Jet pT JER Down")
		u3_1_jesDown.SetXTitle("Jet pT")
		f3_1_jesDown.Add(u3_1_jesDown)



		j41_w_puUp = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_puUp", "Passing Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Up")
	        j41_w_puUp = j41_w_puUp.Clone()
	        h41_w_puUp.Add(j41_w_puUp)

	        j42_w_puUp = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_puUp", "Total Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Up")
	        j42_w_puUp = j42_w_puUp.Clone()
	        h42_w_puUp.Add(j42_w_puUp)

	        j43_w_puUp = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_puUp", "Failing Jet pT vs. Softdrop Mass PileUp Up", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Up")
	        j43_w_puUp = j43_w_puUp.Clone()
	        h43_w_puUp.Add(j43_w_puUp)

		j41_w_puDown = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_puDown", "Passing Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Down")
	        j41_w_puDown = j41_w_puDown.Clone()
	        h41_w_puDown.Add(j41_w_puDown)

	        j42_w_puDown = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_puDown", "Total Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Down")
	        j42_w_puDown = j42_w_puDown.Clone()
	        h42_w_puDown.Add(j42_w_puDown)

	        j43_w_puDown = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_puDown", "Failing Jet pT vs. Softdrop Mass PileUp Down", 7, widebins6, 40, 0, 200), "jPt", "jM", "weight_Down")
	        j43_w_puDown = j43_w_puDown.Clone()
	        h43_w_puDown.Add(j43_w_puDown)


		j41_w_jerUp = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_jerUp", "Passing Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200), "jPt_jerUp", "jM_jerUp", "weight")
	        j41_w_jerUp = j41_w_jerUp.Clone()
	        h41_w_jerUp.Add(j41_w_jerUp)

	        j42_w_jerUp = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_jerUp", "Total Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200), "jPt_jerUp", "jM_jerUp", "weight")
	        j42_w_jerUp = j42_w_jerUp.Clone()
	        h42_w_jerUp.Add(j42_w_jerUp)

	        j43_w_jerUp = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_jerUp", "Failing Jet pT vs. Softdrop Mass JER Up", 7, widebins6, 40, 0, 200), "jPt_jerUp", "jM_jerUp", "weight")
	        j43_w_jerUp = j43_w_jerUp.Clone()
	        h43_w_jerUp.Add(j43_w_jerUp)

		j41_w_jerDown = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_jerDown", "Passing Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200), "jPt_jerDown", "jM_jerDown", "weight")
	        j41_w_jerDown = j41_w_jerDown.Clone()
	        h41_w_jerDown.Add(j41_w_jerDown)

	        j42_w_jerDown = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_jerDown", "Total Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200), "jPt_jerDown", "jM_jerDown", "weight")
	        j42_w_jerDown = j42_w_jerDown.Clone()
	        h42_w_jerDown.Add(j42_w_jerDown)

	        j43_w_jerDown = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_jerDown", "Failing Jet pT vs. Softdrop Mass JER Down", 7, widebins6, 40, 0, 200), "jPt_jerDown", "jM_jerDown", "weight")
	        j43_w_jerDown = j43_w_jerDown.Clone()
	        h43_w_jerDown.Add(j43_w_jerDown)
		
		j41_w_jesUp = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_jesUp", "Passing Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200), "jPt_jesUp", "jM_jesUp", "weight")
	        j41_w_jesUp = j41_w_jesUp.Clone()
	        h41_w_jesUp.Add(j41_w_jesUp)

	        j42_w_jesUp = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_jesUp", "Total Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200), "jPt_jesUp", "jM_jesUp", "weight")
	        j42_w_jesUp = j42_w_jesUp.Clone()
	        h42_w_jesUp.Add(j42_w_jesUp)

	        j43_w_jesUp = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_jesUp", "Failing Jet pT vs. Softdrop Mass JES Up", 7, widebins6, 40, 0, 200), "jPt_jesUp", "jM_jesUp", "weight")
	        j43_w_jesUp = j43_w_jesUp.Clone()
	        h43_w_jesUp.Add(j43_w_jesUp)

		j41_w_jesDown = Rdf_Pass.Histo2D(("pt_soft_pass_wide6_wide_jesDown", "Passing Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200), "jPt_jesDown", "jM_jesDown", "weight")
	        j41_w_jesDown = j41_w_jesDown.Clone()
	        h41_w_jesDown.Add(j41_w_jesDown)

	        j42_w_jesDown = Rdf_Final.Histo2D(("pt_soft_tot_wide6_wide_jesDown", "Total Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200), "jPt_jesDown", "jM_jesDown", "weight")
	        j42_w_jesDown = j42_w_jesDown.Clone()
	        h42_w_jesDown.Add(j42_w_jesDown)

	        j43_w_jesDown = Rdf_Fail.Histo2D(("pt_soft_pass_wide6_wide_jesDown", "Failing Jet pT vs. Softdrop Mass JES Down", 7, widebins6, 40, 0, 200), "jPt_jesDown", "jM_jesDown", "weight")
	        j43_w_jesDown = j43_w_jesDown.Clone()
	        h43_w_jesDown.Add(j43_w_jesDown)



	print(str(nocut)+" Events Before Cuts in "+fname+" Sample")		
	print(str(trig_pass)+" Events After Trigger Cuts in "+fname+" Sample")		
	print(str(npcut)+" Events After nPho>0 in in "+fname+" Sample")		
	print(str(njcut)+" Events After nFatJet>0 in "+fname+" Sample")		
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
	
#	print("Passing Fraction: "+str(pass_pass_weight/(pass_pass_weight+fail_pass_weight)))

	rep_final = Rdf_Final.Report()
	rep_pass = Rdf_Pass.Report()
	rep_fail = Rdf_Fail.Report()

	print("Final Report")
	rep_final.Print()
	print("Pass Report")
	rep_pass.Print()
	print("Fail Report")
	rep_fail.Print()



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

        h47.SetTitle("Number of Good Reconstructed Primary Verticies")
        h47.SetXTitle("Good Primary Verticies")
        ofile.WriteObject(h47, "npvs_Good")

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
	
	p3_1.SetTitle("Thin Passing Jet pT")
	p3_1.SetXTitle("Jet pT")
	ofile.WriteObject(p3_1, "thin_pass_jet_pt")
	

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

        f1_1.SetTitle("Failing Softdrop Mass")
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
	
	f3_1.SetTitle("Thin Failing Jet pT")
	f3_1.SetXTitle("Jet pT")
	ofile.WriteObject(f3_1, "thin_fail_jet_pt")

	f4.SetTitle("Failing Rho")
	f4.SetXTitle("Rho")
	ofile.WriteObject(f4, "fail_rho")

	f5.SetTitle("Failing Photon Eta")
	f5.SetXTitle("Photon Eta")
	ofile.WriteObject(f5, "fail_photon_eta")

	f6.SetTitle("Failing Jet Eta")
	f6.SetXTitle("Jet Eta")
	ofile.WriteObject(f6, "fail_jet_eta")
	
	# Saving Systematics Histograms
        if sample[3] == "mc" or sample[3] == "GJ" or sample[3] == "QCD":
		h2_puUp.SetTitle("Softdrop Mass PileUp Up")
		h2_puUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_puUp, "softdrop_puUp")

        	h2_1_puUp.SetTitle("Thin Softdrop Mass PileUp Up")
        	h2_1_puUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_puUp, "thin_softdrop_puUp")

        	h2_2_puUp.SetTitle("Thin (Uncorrected) Softdrop Mass PileUp Up")
        	h2_2_puUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_puUp, "thin_uncorr_softdrop_puUp")
	
		h5_puUp.SetTitle("Jet pT PileUp Up")
		h5_puUp.SetXTitle("Jet pT")
		ofile.WriteObject(h5_puUp, "jet_pt_puUp")

		h5_1_puUp.SetTitle("Thin Jet pT PileUp Up")
		h5_1_puUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_puUp, "thin_jet_pt_puUp")
        
		h6_puUp.SetTitle("Number of Good Reconstructed Primary Verticies PileUp Up")
        	h6_puUp.SetXTitle("Good Primary Verticies")
        	ofile.WriteObject(h6_puUp, "npvs_Good_puUp")
	
		p1_puUp.SetTitle("Passing Softdrop Mass PileUp Up")
		p1_puUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_puUp, "pass_soft_puUp")

	        p1_1_puUp.SetTitle("Thin Passing Softdrop Mass PileUp Up")
	        p1_1_puUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_puUp, "pass_soft_thin_puUp")

	        p1_2_puUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass PileUp Up")
	        p1_2_puUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_puUp, "pass_soft_uncorr_thin_puUp")
	
		p3_puUp.SetTitle("Passing Jet pT PileUp Up")
		p3_puUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_puUp, "pass_jet_pt_puUp")
	
		p3_1_puUp.SetTitle("Thin Passing Jet pT PileUp Up")
		p3_1_puUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_puUp, "thin_pass_jet_pt_puUp")

		f1_puUp.SetTitle("Failing Softdrop Mass PileUp Up")
		f1_puUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_puUp, "fail_soft_puUp")

		f1_1_puUp.SetTitle("Failing Softdrop Mass PileUp Up")
	        f1_1_puUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_puUp, "fail_soft_thin_puUp")

	        f1_2_puUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass PileUp Up")
	        f1_2_puUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_puUp, "fail_soft_uncorr_thin_puUp")
	
		f3_puUp.SetTitle("Failing Jet pT PileUp Up")
		f3_puUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_puUp, "fail_jet_pt_puUp")
	
		f3_1_puUp.SetTitle("Thin Failing Jet pT PileUp Up")
		f3_1_puUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_puUp, "thin_fail_jet_pt_puUp")
		
		h41_w_puUp.SetTitle("Passing Jet pT vs. Softdrop Mass PileUp Up")
        	h41_w_puUp.SetYTitle("Softdrop Mass")
        	h41_w_puUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_puUp, "jet_pt_soft_pass_wide6_wide_puUp")

        	h42_w_puUp.SetTitle("Total Jet pT vs. Softdrop Mass PileUp Up")
        	h42_w_puUp.SetYTitle("Softdrop Mass")
        	h42_w_puUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_puUp, "jet_pt_soft_total_wide6_wide_puUp")

        	h43_w_puUp.SetTitle("Failing Jet pT vs. Softdrop Mass PileUp Up")
        	h43_w_puUp.SetYTitle("Softdrop Mass")
        	h43_w_puUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_puUp, "jet_pt_soft_fail_wide6_wide_puUp")
		
		
		h2_puDown.SetTitle("Softdrop Mass PileUp Down")
		h2_puDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_puDown, "softdrop_puDown")

        	h2_1_puDown.SetTitle("Thin Softdrop Mass PileUp Down")
        	h2_1_puDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_puDown, "thin_softdrop_puDown")

        	h2_2_puDown.SetTitle("Thin (Uncorrected) Softdrop Mass PileUp Down")
        	h2_2_puDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_puDown, "thin_uncorr_softdrop_puDown")
	
		h5_puDown.SetTitle("Jet pT PileUp Down")
		h5_puDown.SetXTitle("Jet pT")
		ofile.WriteObject(h5_puDown, "jet_pt_puDown")

		h5_1_puDown.SetTitle("Thin Jet pT PileUp Down")
		h5_1_puDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_puDown, "thin_jet_pt_puDown")
	
		h6_puDown.SetTitle("Number of Good Reconstructed Primary Verticies PileUp Down")
        	h6_puDown.SetXTitle("Good Primary Verticies")
        	ofile.WriteObject(h6_puDown, "npvs_Good_puDown")
		
		p1_puDown.SetTitle("Passing Softdrop Mass PileUp Down")
		p1_puDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_puDown, "pass_soft_puDown")

	        p1_1_puDown.SetTitle("Thin Passing Softdrop Mass PileUp Down")
	        p1_1_puDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_puDown, "pass_soft_thin_puDown")

	        p1_2_puDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass PileUp Down")
	        p1_2_puDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_puDown, "pass_soft_uncorr_thin_puDown")
	
		p3_puDown.SetTitle("Passing Jet pT PileUp Down")
		p3_puDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_puDown, "pass_jet_pt_puDown")
	
		p3_1_puDown.SetTitle("Thin Passing Jet pT PileUp Down")
		p3_1_puDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_puDown, "thin_pass_jet_pt_puDown")

		f1_puDown.SetTitle("Failing Softdrop Mass PileUp Down")
		f1_puDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_puDown, "fail_soft_puDown")

		f1_1_puDown.SetTitle("Failing Softdrop Mass PileUp Down")
	        f1_1_puDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_puDown, "fail_soft_thin_puDown")

	        f1_2_puDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass PileUp Down")
	        f1_2_puDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_puDown, "fail_soft_uncorr_thin_puDown")
	
		f3_puDown.SetTitle("Failing Jet pT PileUp Down")
		f3_puDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_puDown, "fail_jet_pt_puDown")
	
		f3_1_puDown.SetTitle("Thin Failing Jet pT PileUp Down")
		f3_1_puDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_puDown, "thin_fail_jet_pt_puDown")
		
		h41_w_puDown.SetTitle("Passing Jet pT vs. Softdrop Mass PileUp Down")
        	h41_w_puDown.SetYTitle("Softdrop Mass")
        	h41_w_puDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_puDown, "jet_pt_soft_pass_wide6_wide_puDown")

        	h42_w_puDown.SetTitle("Total Jet pT vs. Softdrop Mass PileUp Down")
        	h42_w_puDown.SetYTitle("Softdrop Mass")
        	h42_w_puDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_puDown, "jet_pt_soft_total_wide6_wide_puDown")

        	h43_w_puDown.SetTitle("Failing Jet pT vs. Softdrop Mass PileUp Down")
        	h43_w_puDown.SetYTitle("Softdrop Mass")
        	h43_w_puDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_puDown, "jet_pt_soft_fail_wide6_wide_puDown")
		
		
		h2_jerUp.SetTitle("Softdrop Mass JER Up")
		h2_jerUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_jerUp, "softdrop_jerUp")

        	h2_1_jerUp.SetTitle("Thin Softdrop Mass JER Up")
        	h2_1_jerUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_jerUp, "thin_softdrop_jerUp")

        	h2_2_jerUp.SetTitle("Thin (Uncorrected) Softdrop Mass JER Up")
        	h2_2_jerUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_jerUp, "thin_uncorr_softdrop_jerUp")
	
		h5_jerUp.SetTitle("Jet pT JER Up")
		h5_jerUp.SetXTitle("Jet pT")
		ofile.WriteObject(h5_jerUp, "jet_pt_jerUp")

		h5_1_jerUp.SetTitle("Thin Jet pT JER Up")
		h5_1_jerUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_jerUp, "thin_jet_pt_jerUp")
	
		p1_jerUp.SetTitle("Passing Softdrop Mass JER Up")
		p1_jerUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_jerUp, "pass_soft_jerUp")

	        p1_1_jerUp.SetTitle("Thin Passing Softdrop Mass JER Up")
	        p1_1_jerUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_jerUp, "pass_soft_thin_jerUp")

	        p1_2_jerUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Up")
	        p1_2_jerUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_jerUp, "pass_soft_uncorr_thin_jerUp")
	
		p3_jerUp.SetTitle("Passing Jet pT JER Up")
		p3_jerUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_jerUp, "pass_jet_pt_jerUp")
	
		p3_1_jerUp.SetTitle("Thin Passing Jet pT JER Up")
		p3_1_jerUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_jerUp, "thin_pass_jet_pt_jerUp")

		f1_jerUp.SetTitle("Failing Softdrop Mass JER Up")
		f1_jerUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_jerUp, "fail_soft_jerUp")

		f1_1_jerUp.SetTitle("Failing Softdrop Mass JER Up")
	        f1_1_jerUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_jerUp, "fail_soft_thin_jerUp")

	        f1_2_jerUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Up")
	        f1_2_jerUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_jerUp, "fail_soft_uncorr_thin_jerUp")
	
		f3_jerUp.SetTitle("Failing Jet pT JER Up")
		f3_jerUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_jerUp, "fail_jet_pt_jerUp")
	
		f3_1_jerUp.SetTitle("Thin Failing Jet pT JER Up")
		f3_1_jerUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_jerUp, "thin_fail_jet_pt_jerUp")
		
		h41_w_jerUp.SetTitle("Passing Jet pT vs. Softdrop Mass JER Up")
        	h41_w_jerUp.SetYTitle("Softdrop Mass")
        	h41_w_jerUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_jerUp, "jet_pt_soft_pass_wide6_wide_jerUp")

        	h42_w_jerUp.SetTitle("Total Jet pT vs. Softdrop Mass JER Up")
        	h42_w_jerUp.SetYTitle("Softdrop Mass")
        	h42_w_jerUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_jerUp, "jet_pt_soft_total_wide6_wide_jerUp")

        	h43_w_jerUp.SetTitle("Failing Jet pT vs. Softdrop Mass JER Up")
        	h43_w_jerUp.SetYTitle("Softdrop Mass")
        	h43_w_jerUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_jerUp, "jet_pt_soft_fail_wide6_wide_jerUp")
		
		
		h2_jerDown.SetTitle("Softdrop Mass JER Down")
		h2_jerDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_jerDown, "softdrop_jerDown")

        	h2_1_jerDown.SetTitle("Thin Softdrop Mass JER Down")
        	h2_1_jerDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_jerDown, "thin_softdrop_jerDown")

        	h2_2_jerDown.SetTitle("Thin (Uncorrected) Softdrop Mass JER Down")
        	h2_2_jerDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_jerDown, "thin_uncorr_softdrop_jerDown")
	
		h5_jerDown.SetTitle("Jet pT JER Down")
		h5_jerDown.SetXTitle("Jet pT")
		ofile.WriteObject(h5_jerDown, "jet_pt_jerDown")

		h5_1_jerDown.SetTitle("Thin Jet pT JER Down")
		h5_1_jerDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_jerDown, "thin_jet_pt_jerDown")
	
		p1_jerDown.SetTitle("Passing Softdrop Mass JER Down")
		p1_jerDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_jerDown, "pass_soft_jerDown")

	        p1_1_jerDown.SetTitle("Thin Passing Softdrop Mass JER Down")
	        p1_1_jerDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_jerDown, "pass_soft_thin_jerDown")

	        p1_2_jerDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JER Down")
	        p1_2_jerDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_jerDown, "pass_soft_uncorr_thin_jerDown")
	
		p3_jerDown.SetTitle("Passing Jet pT JER Down")
		p3_jerDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_jerDown, "pass_jet_pt_jerDown")
	
		p3_1_jerDown.SetTitle("Thin Passing Jet pT JER Down")
		p3_1_jerDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_jerDown, "thin_pass_jet_pt_jerDown")

		f1_jerDown.SetTitle("Failing Softdrop Mass JER Down")
		f1_jerDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_jerDown, "fail_soft_jerDown")

		f1_1_jerDown.SetTitle("Failing Softdrop Mass JER Down")
	        f1_1_jerDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_jerDown, "fail_soft_thin_jerDown")

	        f1_2_jerDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JER Down")
	        f1_2_jerDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_jerDown, "fail_soft_uncorr_thin_jerDown")
	
		f3_jerDown.SetTitle("Failing Jet pT JER Down")
		f3_jerDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_jerDown, "fail_jet_pt_jerDown")
	
		f3_1_jerDown.SetTitle("Thin Failing Jet pT JER Down")
		f3_1_jerDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_jerDown, "thin_fail_jet_pt_jerDown")
		
		h41_w_jerDown.SetTitle("Passing Jet pT vs. Softdrop Mass JER Down")
        	h41_w_jerDown.SetYTitle("Softdrop Mass")
        	h41_w_jerDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_jerDown, "jet_pt_soft_pass_wide6_wide_jerDown")

        	h42_w_jerDown.SetTitle("Total Jet pT vs. Softdrop Mass JER Down")
        	h42_w_jerDown.SetYTitle("Softdrop Mass")
        	h42_w_jerDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_jerDown, "jet_pt_soft_total_wide6_wide_jerDown")

        	h43_w_jerDown.SetTitle("Failing Jet pT vs. Softdrop Mass JER Down")
        	h43_w_jerDown.SetYTitle("Softdrop Mass")
        	h43_w_jerDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_jerDown, "jet_pt_soft_fail_wide6_wide_jerDown")
		
		
		h2_jesUp.SetTitle("Softdrop Mass JES Up")
		h2_jesUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_jesUp, "softdrop_jesUp")

        	h2_1_jesUp.SetTitle("Thin Softdrop Mass JES Up")
        	h2_1_jesUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_jesUp, "thin_softdrop_jesUp")

        	h2_2_jesUp.SetTitle("Thin (Uncorrected) Softdrop Mass JES Up")
        	h2_2_jesUp.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_jesUp, "thin_uncorr_softdrop_jesUp")
	
		h5_jesUp.SetTitle("Jet pT JES Up")
		h5_jesUp.SetXTitle("Jet pT")
		ofile.WriteObject(h5_jesUp, "jet_pt_jesUp")

		h5_1_jesUp.SetTitle("Thin Jet pT JES Up")
		h5_1_jesUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_jesUp, "thin_jet_pt_jesUp")
	
		p1_jesUp.SetTitle("Passing Softdrop Mass JES Up")
		p1_jesUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_jesUp, "pass_soft_jesUp")

	        p1_1_jesUp.SetTitle("Thin Passing Softdrop Mass JES Up")
	        p1_1_jesUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_jesUp, "pass_soft_thin_jesUp")

	        p1_2_jesUp.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JES Up")
	        p1_2_jesUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_jesUp, "pass_soft_uncorr_thin_jesUp")
	
		p3_jesUp.SetTitle("Passing Jet pT JES Up")
		p3_jesUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_jesUp, "pass_jet_pt_jesUp")
	
		p3_1_jesUp.SetTitle("Thin Passing Jet pT JES Up")
		p3_1_jesUp.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_jesUp, "thin_pass_jet_pt_jesUp")

		f1_jesUp.SetTitle("Failing Softdrop Mass JES Up")
		f1_jesUp.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_jesUp, "fail_soft_jesUp")

		f1_1_jesUp.SetTitle("Failing Softdrop Mass JES Up")
	        f1_1_jesUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_jesUp, "fail_soft_thin_jesUp")

	        f1_2_jesUp.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JES Up")
	        f1_2_jesUp.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_jesUp, "fail_soft_uncorr_thin_jesUp")
	
		f3_jesUp.SetTitle("Failing Jet pT JES Up")
		f3_jesUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_jesUp, "fail_jet_pt_jesUp")
	
		f3_1_jesUp.SetTitle("Thin Failing Jet pT JES Up")
		f3_1_jesUp.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_jesUp, "thin_fail_jet_pt_jesUp")
		
		h41_w_jesUp.SetTitle("Passing Jet pT vs. Softdrop Mass JES Up")
        	h41_w_jesUp.SetYTitle("Softdrop Mass")
        	h41_w_jesUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_jesUp, "jet_pt_soft_pass_wide6_wide_jesUp")

        	h42_w_jesUp.SetTitle("Total Jet pT vs. Softdrop Mass JES Up")
        	h42_w_jesUp.SetYTitle("Softdrop Mass")
        	h42_w_jesUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_jesUp, "jet_pt_soft_total_wide6_wide_jesUp")

        	h43_w_jesUp.SetTitle("Failing Jet pT vs. Softdrop Mass JES Up")
        	h43_w_jesUp.SetYTitle("Softdrop Mass")
        	h43_w_jesUp.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_jesUp, "jet_pt_soft_fail_wide6_wide_jesUp")
		
		
		h2_jesDown.SetTitle("Softdrop Mass JES Down")
		h2_jesDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h2_jesDown, "softdrop_jesDown")

        	h2_1_jesDown.SetTitle("Thin Softdrop Mass JES Down")
        	h2_1_jesDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_1_jesDown, "thin_softdrop_jesDown")

        	h2_2_jesDown.SetTitle("Thin (Uncorrected) Softdrop Mass JES Down")
        	h2_2_jesDown.SetXTitle("Softdrop Mass")
        	ofile.WriteObject(h2_2_jesDown, "thin_uncorr_softdrop_jesDown")
	
		h5_jesDown.SetTitle("Jet pT JES Down")
		h5_jesDown.SetXTitle("Jet pT")
		ofile.WriteObject(h5_jesDown, "jet_pt_jesDown")

		h5_1_jesDown.SetTitle("Thin Jet pT JES Down")
		h5_1_jesDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h5_1_jesDown, "thin_jet_pt_jesDown")
	
		p1_jesDown.SetTitle("Passing Softdrop Mass JES Down")
		p1_jesDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(p1_jesDown, "pass_soft_jesDown")

	        p1_1_jesDown.SetTitle("Thin Passing Softdrop Mass JES Down")
	        p1_1_jesDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_1_jesDown, "pass_soft_thin_jesDown")

	        p1_2_jesDown.SetTitle("Thin (Uncorrected) Passing Softdrop Mass JES Down")
	        p1_2_jesDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(p1_2_jesDown, "pass_soft_uncorr_thin_jesDown")
	
		p3_jesDown.SetTitle("Passing Jet pT JES Down")
		p3_jesDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_jesDown, "pass_jet_pt_jesDown")
	
		p3_1_jesDown.SetTitle("Thin Passing Jet pT JES Down")
		p3_1_jesDown.SetXTitle("Jet pT")
		ofile.WriteObject(p3_1_jesDown, "thin_pass_jet_pt_jesDown")

		f1_jesDown.SetTitle("Failing Softdrop Mass JES Down")
		f1_jesDown.SetXTitle("Softdrop Mass")
		ofile.WriteObject(f1_jesDown, "fail_soft_jesDown")

		f1_1_jesDown.SetTitle("Failing Softdrop Mass JES Down")
	        f1_1_jesDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_1_jesDown, "fail_soft_thin_jesDown")

	        f1_2_jesDown.SetTitle("Thin (Uncorrected) Failing Softdrop Mass JES Down")
	        f1_2_jesDown.SetXTitle("Softdrop Mass")
	        ofile.WriteObject(f1_2_jesDown, "fail_soft_uncorr_thin_jesDown")
	
		f3_jesDown.SetTitle("Failing Jet pT JES Down")
		f3_jesDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_jesDown, "fail_jet_pt_jesDown")
	
		f3_1_jesDown.SetTitle("Thin Failing Jet pT JES Down")
		f3_1_jesDown.SetXTitle("Jet pT")
		ofile.WriteObject(f3_1_jesDown, "thin_fail_jet_pt_jesDown")
		
		h41_w_jesDown.SetTitle("Passing Jet pT vs. Softdrop Mass JES Down")
        	h41_w_jesDown.SetYTitle("Softdrop Mass")
        	h41_w_jesDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h41_w_jesDown, "jet_pt_soft_pass_wide6_wide_jesDown")

        	h42_w_jesDown.SetTitle("Total Jet pT vs. Softdrop Mass JES Down")
        	h42_w_jesDown.SetYTitle("Softdrop Mass")
        	h42_w_jesDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h42_w_jesDown, "jet_pt_soft_total_wide6_wide_jesDown")

        	h43_w_jesDown.SetTitle("Failing Jet pT vs. Softdrop Mass JES Down")
        	h43_w_jesDown.SetYTitle("Softdrop Mass")
        	h43_w_jesDown.SetXTitle("Jet pT")
        	ofile.WriteObject(h43_w_jesDown, "jet_pt_soft_fail_wide6_wide_jesDown")
		
		

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
