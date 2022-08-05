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



def Processor(sample, fname, cut_hist, percentage=10, rho_bin=28, pt_bin=40, n2_bin=750):

	gROOT.SetBatch(True)

	ofile = ROOT.TFile("RData_" + fname + ".root", "RECREATE")
	ofile.cd()

	ROOT.ROOT.EnableImplicitMT()


        rho_bins = cut_hist.GetNbinsX()
        pt_bins = cut_hist.GetNbinsY()

		

	h2 = TH1F("h2", "SelectedJet Softdrop Mass", 50, 0, 200)
	h3 = TH1F("h3", "SelectedJet Corrected Softdrop Mass", 50, 0, 200)
	h5 = TH1F("h5", "SelectedJet Jet Pt", 500, 0, 2000)
	h6 = TH1F("h6", "SelectedJet rawFactor", 25, 0, .5)
	h7 = TH1F("h7", "SelectedJet N2", 50, 0, 1)
	h8 = TH1F("h8", "SelectedJet BTag", 100, -1, 1)
	
	h2_1 = TH1F("h2_1", "FatJet Softdrop Mass", 50, 0, 200)
	h3_1 = TH1F("h3_1", "FatJet Corrected Softdrop Mass", 50, 0, 200)
	h5_1 = TH1F("h5_1", "FatJet Jet Pt", 500, 0, 2000)
	h6_1 = TH1F("h6_1", "FatJet rawFactor", 25, 0, .5)
	h7_1 = TH1F("h7_1", "FatJet N2", 50, 0, 1)
	h8_1 = TH1F("h8_1", "FatJet BTag", 100, -1, 1)


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

		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
                Rdf_PreSel = Rdf_PreSel.Define("weight", F[1])

        	Rdf = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")
        	Rdf = Rdf.Filter("selectedPatJetsAK8PFPuppi_softdropMass[0]>0")
        	Rdf = Rdf.Filter("nFatJet > 0.")
        	Rdf = Rdf.Filter("FatJet_msoftdrop[0]>0")
		
		#Note corrected softdrop mass is being used

		Rdf = Rdf.Define("selected_jM", "selectedPatJetsAK8PFPuppi_softdropMass[0]")
		Rdf = Rdf.Define("selected_jM_corr", "selectedPatJetsAK8PFPuppi_softdropMass[0]/(1-selectedPatJetsAK8PFPuppi_rawFactor[0])")
        	Rdf = Rdf.Define("selected_jPt", "selectedPatJetsAK8PFPuppi_pt[0]")
        	Rdf = Rdf.Define("selected_raw", "selectedPatJetsAK8PFPuppi_rawFactor[0]")
        	Rdf = Rdf.Define("selected_n2", "selectedPatJetsAK8PFPuppi_ak8PFJetsPuppiSoftDropValueMap_nb1AK8PuppiSoftDropN2[0]")
        	Rdf = Rdf.Define("selected_btag", "selectedPatJetsAK8PFPuppi_pfBoostedDoubleSecondaryVertexAK8BJetTags[0]")

		Rdf = Rdf.Define("FatJet_jM", "FatJet_msoftdrop[0]")
		Rdf = Rdf.Define("FatJet_jM_corr", "FatJet_msoftdrop[0]") #FatJet doesnt need corr
        	Rdf = Rdf.Define("FatJet_jPt", "FatJet_pt[0]")
        	Rdf = Rdf.Define("Fat_raw", "FatJet_rawFactor[0]")
        	Rdf = Rdf.Define("Fat_n2", "FatJet_n2b1[0]")
        	Rdf = Rdf.Define("Fat_btag", "FatJet_btagCSVV2[0]")



        	t2 = Rdf.Histo1D(("t2", "Softdrop Mass", 50, 0, 200), "selected_jM", "weight")
		t2 = t2.Clone()
        	t2.SetTitle("Softdrop Mass")
        	t2.SetXTitle("Softdrop Mass")
		h2.Add(t2)
        	
		t3 = Rdf.Histo1D(("t3", "Softdrop Mass", 50, 0, 200), "selected_jM_corr", "weight")
        	t3 = t3.Clone()
        	t3.SetTitle("Softdrop Mass")
        	t3.SetXTitle("Softdrop Mass")
		h3.Add(t3)
	        
		t5 = Rdf.Histo1D(("t5", "Jet Pt", 500, 0, 2000), "selected_jPt", "weight")
	        t5 = t5.Clone()
	        t5.SetTitle("Jet Pt")
	        t5.SetXTitle("Pt")
		h5.Add(t5)
		
		t6 = Rdf.Histo1D(("t6", "rawFactor", 25, 0, .5), "selected_raw", "weight")
	        t6 = t6.Clone()
	        t6.SetTitle("rawFactor")
	        t6.SetXTitle("rawFactor")
		h6.Add(t6)
		
		t7 = Rdf.Histo1D(("t7", "N2", 50, 0, 1), "selected_n2", "weight")
	        t7 = t7.Clone()
	        t7.SetTitle("N2")
	        t7.SetXTitle("N2")
		h7.Add(t7)
		
		t8 = Rdf.Histo1D(("t8", "BTag", 100, -1, 1), "selected_btag", "weight")
	        t8 = t8.Clone()
	        t8.SetTitle("BTag")
	        t8.SetXTitle("BTag")
		h8.Add(t8)
		
        	t2_1 = Rdf.Histo1D(("t2_1", "Softdrop Mass", 50, 0, 200), "FatJet_jM", "weight")
        	t2_1 = t2_1.Clone()
        	t2_1.SetTitle("Softdrop Mass")
        	t2_1.SetXTitle("Softdrop Mass")
		h2_1.Add(t2_1)
		
		t3_1 = Rdf.Histo1D(("t3_1", "Softdrop Mass", 50, 0, 200), "FatJet_jM_corr", "weight")
        	t3_1 = t3_1.Clone()
        	t3_1.SetTitle("Softdrop Mass")
        	t3_1.SetXTitle("Softdrop Mass")
		h3_1.Add(t3_1)
	        
		t5_1 = Rdf.Histo1D(("t5_1", "Jet Pt", 500, 0, 2000), "FatJet_jPt", "weight")
	        t5_1 = t5_1.Clone()
	        t5_1.SetTitle("Jet Pt")
	        t5_1.SetXTitle("Pt")
		h5_1.Add(t5)

		t6_1 = Rdf.Histo1D(("t6_1", "rawFactor", 25, 0, .5), "selected_raw", "weight")
	        t6_1 = t6_1.Clone()
	        t6_1.SetTitle("rawFactor")
	        t6_1.SetXTitle("rawFactor")
		h6_1.Add(t6_1)
		
		t7_1 = Rdf.Histo1D(("t7_1", "N2", 50, 0, 1), "selected_n2", "weight")
	        t7_1 = t7_1.Clone()
	        t7_1.SetTitle("N2")
	        t7_1.SetXTitle("N2")
		h7_1.Add(t7_1)
		
		t8_1 = Rdf.Histo1D(("t8_1", "BTag", 100, -1, 1), "selected_btag", "weight")
	        t8_1 = t8_1.Clone()
	        t8_1.SetTitle("BTag")
	        t8_1.SetXTitle("BTag")
		h8_1.Add(t8_1)


#	h2.Scale(1/h2.Intregral())
#	h3.Scale(1/h3.Intregral())
#	h5.Scale(1/h5.Intregral())
	
#	h2_1.Scale(1/h2_1.Intregral())
#	h3_1.Scale(1/h3_1.Intregral())
#	h5_1.Scale(1/h5_1.Intregral())

	ofile.WriteObject(h2, "selected_softdrop")
	ofile.WriteObject(h3, "selected_softdrop_corr")
	ofile.WriteObject(h5, "selected_jet_pt")
	ofile.WriteObject(h6, "selected_rawFactor")
	ofile.WriteObject(h7, "selected_n2")
	ofile.WriteObject(h8, "selected_btag")
	
	ofile.WriteObject(h2_1, "FatJet_softdrop")
	ofile.WriteObject(h3_1, "FatJet_softdrop_corr")
	ofile.WriteObject(h5_1, "FatJet_jet_pt")
	ofile.WriteObject(h6_1, "FatJet_rawFactor")
	ofile.WriteObject(h7_1, "FatJet_n2")
	ofile.WriteObject(h8_1, "FatJet_btag")

	h2_1.SetLineColor(kGreen)
	h3_1.SetLineColor(kGreen)
	h5_1.SetLineColor(kGreen)
	h6_1.SetLineColor(kGreen)
	h7_1.SetLineColor(kGreen)
	h8_1.SetLineColor(kGreen)

	l1 = TLegend(.6, .75, .9, .9)
	
        h2.SetTitle("Softdrop Mass")
        h2.SetXTitle("Softdrop Mass")
	
        c2 = TCanvas()
        c2.cd()
	c2.SetLogy()
        h2.Draw("hist")
        h2_1.Draw("same hist")
	l1.AddEntry(h2, "SelectedJet")
	l1.AddEntry(h2_1, "FatJet")
	l1.Draw()
	c2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_softdrop.png")
        c2.Close()
	l1.Clear()

	
        h3.SetTitle("Corrected Softdrop Mass")
        h3.SetXTitle("Softdrop Mass")

        c3 = TCanvas()
        c3.cd()
	c3.SetLogy()
        h3.Draw("hist")
        h3_1.Draw("same hist")
	l1.AddEntry(h3, "SelectedJet")
	l1.AddEntry(h3_1, "FatJet")
	l1.Draw()
        c3.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_softdrop_corr.png")
        c3.Close()
	l1.Clear()
	
		
        h5.SetTitle("Jet pT")
        h5.SetXTitle("Jet pT")

        c5 = TCanvas()
        c5.cd()
        h5.Draw("hist")
        h5_1.Draw("same hist")
	l1.AddEntry(h5, "SelectedJet")
	l1.AddEntry(h5_1, "FatJet")
	l1.Draw()
        c5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt.png")
        c5.Close()
	l1.Clear()       
 
        h6.SetTitle("rawFactor")
        h6.SetXTitle("rawFactor")

        c6 = TCanvas()
        c6.cd()
        h6.Draw("hist")
        h6_1.Draw("same hist")
	l1.AddEntry(h6, "SelectedJet")
	l1.AddEntry(h6_1, "FatJet")
	l1.Draw()
        c6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_rawFactor.png")
        c6.Close()
	l1.Clear()       
        
	c7 = TCanvas()
        c7.cd()
        h7.Draw("hist")
        h7_1.Draw("same hist")
	l1.AddEntry(h7, "SelectedJet")
	l1.AddEntry(h7_1, "FatJet")
	l1.Draw()
        c7.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2.png")
        c7.Close()
	l1.Clear()       
	
	c8 = TCanvas()
        c8.cd()
        h8.Draw("hist")
        h8_1.Draw("same hist")
	l1.AddEntry(h8, "SelectedJet")
	l1.AddEntry(h8_1, "FatJet")
	l1.Draw()
        c8.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_btag.png")
        c8.Close()
	l1.Clear()       
		
	ofile.Write()
