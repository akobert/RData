#
import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

import math


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

def MakeHist(Chain, cut_hist, ofile, fname, weight):
	Rdf_noCut = RDF(Chain)
	C = Rdf_noCut.Count()
	total_events = float(C.GetValue())
	print(str(C.GetValue())+" Events Before Cuts in "+fname+" Sample")
	

	Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
	C = Rdf_PreSel.Count()
	print(str(C.GetValue())+" Events After nPho>0 in "+fname+" Sample")
	Rdf_PreSel = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")
	C = Rdf_PreSel.Count()
	print(str(C.GetValue())+" Events After nselectedJet>0 in "+fname+" Sample")
	num_pass = float(C.GetValue())


	
	Rdf_cflow = Rdf_PreSel.Filter("PPT(Photon_pt, nPhoton)")
	ppt_pass = float(Rdf_cflow.Count().GetValue())

	Rdf_cflow = Rdf_cflow.Filter("JPT(selectedPatJetsAK8PFPuppi_pt, nselectedPatJetsAK8PFPuppi)")
	jpt_pass = float(Rdf_cflow.Count().GetValue())


	Rdf_cflow = Rdf_cflow.Filter("PETA(Photon_pt, Photon_eta, nPhoton)")
	peta_pass = float(Rdf_cflow.Count().GetValue())

	
	Rdf_cflow = Rdf_cflow.Filter("JETA(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, nselectedPatJetsAK8PFPuppi)")
	jeta_pass = float(Rdf_cflow.Count().GetValue())

	
	Rdf_cflow = Rdf_cflow.Filter("PID(Photon_pt, Photon_eta, Photon_cutBased, nPhoton)")
	pid_pass = float(Rdf_cflow.Count().GetValue())

	
	Rdf_cflow = Rdf_cflow.Filter("JID(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId, nselectedPatJetsAK8PFPuppi)")
	jid_pass = float(Rdf_cflow.Count().GetValue())

	
	Rdf_cflow = Rdf_cflow.Filter("JSOFT(selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_jetId,selectedPatJetsAK8PFPuppi_softdropMass, nselectedPatJetsAK8PFPuppi)")
	jsoft_pass = float(Rdf_cflow.Count().GetValue())
	
	
	Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_softdropMass, selectedPatJetsAK8PFPuppi_jetId)")
	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")


	Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events After Photon Cuts in "+fname+" Sample")

	Rdf = Rdf.Filter("jIndex >= 0")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events After Jet Cuts in "+fname+" Sample")
	

	#Note Corrected softdrop mass is being used

	Rdf = Rdf.Define("jM", "selectedPatJetsAK8PFPuppi_softdropMass[jIndex]/(1 - selectedPatJetsAK8PFPuppi_rawFactor[jIndex])")
	#Rdf = Rdf.Define("sub_jM", "submass((selectedPatJetsAK8PFPuppiSoftDrop_Subjets_pt[jIndex]), selectedPatJetsAK8PFPuppiSoftDrop_Subjets_eta[jIndex], selectedPatJetsAK8PFPuppiSoftDrop_Subjets_phi[jIndex],selectedPatJetsAK8PFPuppiSoftDrop_Subjets_mass[jIndex], (selectedPatJetsAK8PFPuppiSoftDrop_Subjets_pt[1+jIndex]), selectedPatJetsAK8PFPuppiSoftDrop_Subjets_eta[1+jIndex], selectedPatJetsAK8PFPuppiSoftDrop_Subjets_phi[1+jIndex],selectedPatJetsAK8PFPuppiSoftDrop_Subjets_mass[1+jIndex])")
	Rdf = Rdf.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
	Rdf = Rdf.Define("jPt", "selectedPatJetsAK8PFPuppi_pt[jIndex]")
	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
	Rdf = Rdf.Define("N2", "selectedPatJetsAK8PFPuppi_ak8PFJetsPuppiSoftDropValueMap_nb1AK8PuppiSoftDropN2[jIndex]")
	Rdf = Rdf.Define("jID", "selectedPatJetsAK8PFPuppi_jetId[jIndex]")
	Rdf = Rdf.Define("n2ddt", "ddt(jPt, jM, N2)")
	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")
	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
	Rdf = Rdf.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
	Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
	Rdf = Rdf.Define("total_weight", weight)
	Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")

	Rdf = Rdf.Define("pTratio", "pPt/jPt")

	print("Non-Preselection Cuts Begin")

	

	Rdf = Rdf.Filter("(HLT_Photon110EB_TightID_TightIso > 0.0 || HLT_Photon200 > 0.0)")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events after Trigger requirements in "+fname+" Sample")
	
	trig_pass = float(C.GetValue())

	Rdf = Rdf.Filter("N2 >= 0")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events after N2 cut in "+fname+" Sample")
	
	n2_pass = float(C.GetValue())

	
	Rdf = Rdf.Filter("Rho < -2 && Rho > -7 ")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events after Rho cut in "+fname+" Sample")
	
	rho_pass = float(C.GetValue())


	Rdf = Rdf.Filter("jPt >120")
	C = Rdf.Count()
	print(str(C.GetValue())+" Events after Jet pT cut in "+fname+" Sample")

        Rdf = Rdf.Filter("dR >= 2.2")
        C = Rdf.Count()
        print(str(C.GetValue())+" Events after DeltaR cut in "+fname+" Sample")
        dR_pass = float(C.GetValue())

	

	Rdf_Pass = Rdf.Filter("n2ddt <= 0")
	C = Rdf_Pass.Count()
	print(str(C.GetValue())+" Passing Events after N2DDT cut in "+fname+" Sample")
	
	pass_pass = float(C.GetValue())


	Rdf_Fail = Rdf.Filter("n2ddt > 0")
	C = Rdf_Fail.Count()
	print(str(C.GetValue())+" Failing Events after N2DDT cut in "+fname+" Sample")

	fail_pass = float(C.GetValue())

	#Create pT slices
	print("pT Slice Creation Begins")
	for i in range(1, 7):
		print("pT Slice #"+str(i))
		#slice_num = "float p = "+str(i*100)+";"
		#ROOT.gInterpreter.Declare(slice_num)
		slice_range = "jPt >= "+str(i*100)+" && jPt <= "+str((i+1)*100)
		#Rdf_ptSlice = Rdf.Filter("jPt >= p && jPt <= (p+100.0)")
		Rdf_ptSlice = Rdf.Filter(slice_range)
		slice_title = "Softdrop Mass in "+fname+" pT slice: "+str(i*100)+" to "+str((i+1)*100)
		h1_pt = Rdf_ptSlice.Histo1D(("h1_pt", slice_title, 40, 0, 200), "jM", "total_weight")
		h1_pt = h1_pt.Clone()
		h1_pt.SetTitle(slice_title)
		h1_pt.SetXTitle("Softdrop Mass")
		ofile.WriteObject(h1_pt, "softdrop_pt"+str(i))
		
	#Wide bin declaration
	ROOT.gInterpreter.Declare("Double_t widebins[9] = {0, 125, 135, 145, 160, 175, 200, 245, 2000};")

	print("Plot 1")
	h1 = Rdf.Histo1D(("h1",  ';N^{2}_{1}', 25, 0, .5), "N2", "total_weight")
	h1 = h1.Clone()
	h1.SetTitle("N2")
	h1.SetXTitle("N2")
	ofile.WriteObject(h1, "N2")
	#ofile.WriteObject(h1.Clone(), "N2")
	
	c1 = TCanvas()
	c1.cd()
	h1.Draw()
	c1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_N2.png")
	c1.Close()

	
	print("Plot 2")

	h2 = Rdf_Pass.Histo1D(("h2", "Passing Softdrop Mass", 40, 0, 200), "jM", "total_weight")
	h2 = h2.Clone()
	h2.SetTitle("Passing Softdrop Mass")
	h2.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2, "pass_soft")
	
	c2 = TCanvas()
	c2.cd()
	h2.Draw()
	c2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_soft.png")
	c2.Close()
	print("Plot 2_2")
	
	
	h2_2 = Rdf.Histo1D(("h2_2", "Softdrop Mass", 40, 0, 200), "jM", "total_weight")
	h2_2 = h2_2.Clone()
	h2_2.SetTitle("Softdrop Mass")
	h2_2.SetXTitle("Softdrop Mass")
	ofile.WriteObject(h2_2, "softdrop")
	
	c2_2 = TCanvas()
	c2_2.cd()
	h2_2.Draw()
	c2_2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_soft.png")
	c2_2.Close()
	print("Plot 3")

	h3 = Rdf.Histo1D(("h3",  "N2DDT", 50, -.5, .5), "n2ddt", "total_weight")
	h3 = h3.Clone()
	ofile.WriteObject(h3, "n2ddt")

	c3 = TCanvas()
	c3.cd()
	h3.Draw()
	c3.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2ddt.png")
	c3.Close()
	print("Plot 4")

	h4 = Rdf_Pass.Histo1D(("h4", "Passing Photon Pt", 40, 0, 1000), "pPt", "total_weight")
	h4 = h4.Clone()
	h4.SetTitle("Passing Photon Pt")
	h4.SetXTitle("Pt")
	ofile.WriteObject(h4, "pass_photon_pt")
	
	c4 = TCanvas()
	c4.cd()
	h4.Draw()
	c4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_photon_pt.png")
	c4.Close()
	print("Plot 5")

	h5 = Rdf_Pass.Histo1D(("h5", "Passing Jet Pt", 40, 0, 2000), "jPt", "total_weight")
	h5 = h5.Clone()
	h5.SetTitle("Passing Jet Pt")
	h5.SetXTitle("Pt")
	ofile.WriteObject(h5, "pass_jet_pt")
	
	c5 = TCanvas()
	c5.cd()
	h5.Draw()
	c5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_jet_pt.png")
	c5.Close()
	print("Plot 6")
	
	h6 = Rdf_Pass.Histo1D(("h6", "Passing Jet Eta", 20, -2.5, 2.5), "jEta", "total_weight")
	h6 = h6.Clone()
	h6.SetTitle("Passing Jet Eta")
	h6.SetXTitle("Eta")
	ofile.WriteObject(h6, "pass_jet_eta")
	
	c6 = TCanvas()
	c6.cd()
	h6.Draw()
	c6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_jet_eta.png")
	c6.Close()
	print("Plot 7")
	
	h7 = Rdf_Pass.Histo1D(("h7", "Passing Rho", 28, -8, -1), "Rho", "total_weight")
	h7 = h7.Clone()
	h7.SetTitle("Passing Rho")
	h7.SetXTitle("Rho")
	ofile.WriteObject(h7, "pass_rho")
	
	c7 = TCanvas()
	c7.cd()
	h7.Draw()
	c7.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_rho.png")
	c7.Close()

        h7_1 = Rdf.Histo1D(("h7_1", "Rho", 28, -8, -1), "Rho", "total_weight")
        h7_1 = h7_1.Clone()
        h7_1.SetTitle("Rho")
        h7_1.SetXTitle("Rho")
        ofile.WriteObject(h7_1, "finerho")

        c7_1 = TCanvas()
        c7_1.cd()
        h7_1.Draw()
        c7_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_finerho.png")
        c7_1.Close()


	print("Plot 8")
	
	h8 = Rdf_Pass.Histo1D(("h8", "Passing Photon Eta", 20, -2.5, -2.5), "pEta", "total_weight")
	h8 = h8.Clone()
	h8.SetTitle("Passing Photon Eta")
	h8.SetXTitle("Eta")
	ofile.WriteObject(h8, "pass_photon_eta")
	
	c8 = TCanvas()
	c8.cd()
	h8.Draw()
	c8.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pass_photon_eta.png")
	c8.Close()
	print("Plot f2")
	
	f2 = Rdf_Fail.Histo1D(("f2", "Failing Softdrop Mass", 40, 0, 200), "jM", "total_weight")
	f2 = f2.Clone()
	#f2.Scale(1.0/9.0)
	f2.SetTitle("Failing Softdrop Mass")
	f2.SetXTitle("Softdrop Mass")

	ofile.WriteObject(f2, "fail_soft")
	
	d2 = TCanvas()
	d2.cd()
	f2.Draw()
	d2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_soft.png")
	d2.Close()
	print("Plot f4")
	
	f4 = Rdf_Fail.Histo1D(("f4", "Failing Photon Pt", 40, 0, 1000), "pPt", "total_weight")
	f4 = f4.Clone()
#	f4.Scale(1.0/9.0)
	f4.SetTitle("Failing Photon Pt")
	f4.SetXTitle("Pt")
	ofile.WriteObject(f4, "fail_photon_pt")
	
	d4 = TCanvas()
	d4.cd()
	f4.Draw()
	d4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_photon_pt.png")
	d4.Close()
	print("Plot f5")

	f5 = Rdf_Fail.Histo1D(("f5", "Failing Jet Pt", 40, 0, 2000), "jPt", "total_weight")
	f5 = f5.Clone()
#	f5.Scale(1.0/9.0)
	f5.SetTitle("Failing Jet Pt")
	f5.SetXTitle("Pt")

	ofile.WriteObject(f5, "fail_jet_pt")
	
	d5 = TCanvas()
	d5.cd()
	f5.Draw()
	d5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_jet_pt.png")
	d5.Close()
	print("Plot f6")
	
	f6 = Rdf_Fail.Histo1D(("f6", "Failing Jet Eta", 20, -2.5, 2.5), "jEta", "total_weight")
	f6 = f6.Clone()
#	f6.Scale(1.0/9.0)
	f6.SetTitle("Failing Jet Eta")
	f6.SetXTitle("Eta")
	ofile.WriteObject(f6, "fail_jet_eta")
	
	d6 = TCanvas()
	d6.cd()
	f6.Draw()
	d6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_jet_eta.png")
	d6.Close()
	print("Plot f7")
	
	f7 = Rdf_Fail.Histo1D(("f6", "Failing Rho", 28, -8, -1), "Rho", "total_weight")
	f7 = f7.Clone()
#	f7.Scale(1.0/9.0)
	f7.SetTitle("Failing Rho")
	f7.SetXTitle("Rho")
	ofile.WriteObject(f7, "fail_rho")
	
	d7 = TCanvas()
	d7.cd()
	f7.Draw()
	d7.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_rho.png")
	d7.Close()
	print("Plot f8")
	
	f8 = Rdf_Fail.Histo1D(("f6", "Failing Photon Eta", 20, -2.5, 2.5), "pEta", "total_weight")
	f8 = f8.Clone()
#	f8.Scale(1.0/9.0)
	f8.SetTitle("Failing Photon Eta")
	f8.SetXTitle("Eta")
	ofile.WriteObject(f8, "fail_photon_eta")
	
	d8 = TCanvas()
	d8.cd()
	f8.Draw()
	d8.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_fail_photon_eta.png")
	d8.Close()


	h11 = Rdf.Histo2D(("n2_n2ddt", "N2 vs. N2DDT", 25, 0, .5, 50, -.5, .5), "N2", "n2ddt", "total_weight")
        h11 = h11.Clone()
        h11.SetTitle("N2 vs. N2DDT")
        h11.SetXTitle("N2")
        h11.SetYTitle("N2DDT")
        ofile.WriteObject(h11, "n2_n2ddt")

        n1 = TCanvas()
        n1.cd()
        h11.Draw("COLZ")
        n1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2_n2ddt.png")
        n1.Close()

	h12 = Rdf.Histo1D(("N2",  ';N^{2}_{1}', 25, 0, .5), "N2", "total_weight")
	h12 = h12.Clone()
	h12.SetTitle("N2")
	h12.SetXTitle("N2")
	ofile.WriteObject(h12, "N2")
	
	n2 = TCanvas()
	n2.cd()
	h12.Draw()
	n2.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_N2.png")
	n2.Close()
	
	h13 = Rdf.Histo1D(("N2DDT",  "N2DDT", 50, -.5, .5), "n2ddt", "total_weight")
	h13 = h13.Clone()
	h13.SetTitle("N2DDT")
	h13.SetXTitle("N2DDT")
	ofile.WriteObject(h13, "N2DDT")
	
	n3 = TCanvas()
	n3.cd()
	h13.Draw()
	n3.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_N2DDT.png")
	n3.Close()

	h14 = Rdf.Histo2D(("n2_soft", "N2 vs. Softdrop Mass", 25, 0, .5, 40, 0, 200), "N2", "jM", "total_weight")
        h14 = h14.Clone()
        h14.SetTitle("N2 vs. Softdrop Mass")
        h14.SetXTitle("N2")
        h14.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h14, "n2_soft")

        n4 = TCanvas()
        n4.cd()
        h14.Draw("COLZ")
        n4.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2_soft.png")
        n4.Close()

	h15 = Rdf.Histo2D(("n2ddt_soft", "N2DDT vs. Softdrop Mass", 50, -.5, .5, 40, 0, 200), "n2ddt", "jM", "total_weight")
        h15 = h15.Clone()
        h15.SetTitle("N2DDT vs. Softdrop Mass")
        h15.SetXTitle("N2DDT")
        h15.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h15, "n2ddt_soft")

        n5 = TCanvas()
        n5.cd()
        h15.Draw("COLZ")
        n5.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_n2ddt_soft.png")
        n5.Close()
	#ofile.WriteObject(TH1F(h3), "N2DDT")	

        h16 = Rdf_Pass.Histo2D(("pt_soft_pass", "Passing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "total_weight")
        h16 = h16.Clone()
        h16.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h16.SetXTitle("Jet pT")
        h16.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h16, "jet_pt_soft_pass")

        n6 = TCanvas()
        n6.cd()
        h16.Draw("COLZ")
        n6.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_pass.png")
        n6.Close()
        
	h16_w = Rdf_Pass.Histo2D(("pt_soft_pass_wide", "Passing Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200), "jPt", "jM", "total_weight")
        h16_w = h16_w.Clone()
        h16_w.SetTitle("Passing Jet pT vs. Softdrop Mass")
        h16_w.SetXTitle("Jet pT")
        h16_w.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h16_w, "jet_pt_soft_pass_wide")

        n6_w = TCanvas()
        n6_w.cd()
        h16_w.Draw("COLZ")
        n6_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_pass_wide.png")
        n6_w.Close()

        h16_1 = Rdf.Histo2D(("pt_soft_total", "Total Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "total_weight")
        h16_1 = h16_1.Clone()
        h16_1.SetTitle("Total Jet pT vs. Softdrop Mass")
        h16_1.SetXTitle("Jet pT")
        h16_1.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h16_1, "jet_pt_soft_total")

        n6_1 = TCanvas()
        n6_1.cd()
        h16_1.Draw("COLZ")
        n6_1.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_total.png")
        n6_1.Close()
	
	h16_1_w = Rdf.Histo2D(("pt_soft_total_wide", "Total Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200), "jPt", "jM", "total_weight")
        h16_1_w = h16_1_w.Clone()
        h16_1_w.SetTitle("Total Jet pT vs. Softdrop Mass")
        h16_1_w.SetXTitle("Jet pT")
        h16_1_w.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h16_1_w, "jet_pt_soft_total_wide")

        n6_1_w = TCanvas()
        n6_1_w.cd()
        h16_1_w.Draw("COLZ")
        n6_1_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft.png")
        n6_1_w.Close()
        
	h17 = Rdf_Fail.Histo2D(("pt_soft_fail", "Failing Jet pT vs. Softdrop Mass", 40, 0, 2000, 40, 0, 200), "jPt", "jM", "total_weight")
        h17 = h17.Clone()
        h17.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h17.SetXTitle("Jet pT")
        h17.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h17, "jet_pt_soft_fail")

        n7 = TCanvas()
        n7.cd()
        h17.Draw("COLZ")
        n7.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft.png")
        n7.Close()
	
	h17_w = Rdf_Fail.Histo2D(("pt_soft_fail_wide", "Failing Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200), "jPt", "jM", "total_weight")
        h17_w = h17_w.Clone()
        h17_w.SetTitle("Failing Jet pT vs. Softdrop Mass")
        h17_w.SetXTitle("Jet pT")
        h17_w.SetYTitle("Softdrop Mass")
        ofile.WriteObject(h17_w, "jet_pt_soft_fail_wide")

        n7_w = TCanvas()
        n7_w.cd()
        h17_w.Draw("COLZ")
        n7_w.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_jet_pt_soft_fail_wide.png")
        n7_w.Close()

	h26 = Rdf.Histo2D(("pt_photon_jet", "Jet pT vs. Photon pT", 40, 0, 2000, 40, 0, 2000), "jPt", "pPt", "total_weight")
	h26 = h26.Clone()
	h26.SetXTitle("Jet pT")
	h26.SetYTitle("Photon pT")
	ofile.WriteObject(h26, "pt_photon_jet")
	
	n26 = TCanvas()
	n26.cd()
        n26.SetLogz()
	h26.Draw("COLZ")
	n26.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_pt_photon_jet.png")
	n26.Close()

	h27 = Rdf.Histo2D(("photon_jet_ratio_pt", "Jet pT vs. Photon pT / Jet pT", 40, 0, 2000, 40, 0, 3), "jPt", "pTratio", "total_weight")
        h27 = h27.Clone()
        h27.SetXTitle("Jet pT")
        h27.SetYTitle("Photon pT / Jet pT")
	ofile.WriteObject(h27, "photon_jet_ratio_pt")
	
	n27 = TCanvas()
        n27.cd()
        n27.SetLogz()
        h27.Draw("COLZ")
        n27.SaveAs("/home/akobert/CMSSW_11_1_0_pre7/src/plots/RData_"+fname+"_photon_jet_ratio_pt.png")
        n27.Close()
	
	
	print("Total Number of Events: "+str(total_events))

	print("Cutflow Percentages: ")
	print("Num Pho and Num Jet passed: "+str(num_pass/total_events * 100)+"%")
	print("Photon pT passed: "+str(ppt_pass/total_events * 100)+"%")
	print("Jet pT passed: "+str(jpt_pass/total_events * 100)+"%")
	print("Photon Eta passed: "+str(peta_pass/total_events * 100)+"%")
	print("Jet Eta passed: "+str(jeta_pass/total_events * 100)+"%")
	print("MVAID passed: "+str(pid_pass/total_events * 100)+"%")
	print("Jet ID passed: "+str(jid_pass/total_events * 100)+"%")
	print("Softdrop passed: "+str(jsoft_pass/total_events * 100)+"%")
	print("Trigger passed: "+str(trig_pass/total_events * 100)+"%")
	print("N2 passed: "+str(n2_pass/total_events * 100)+"%")
	print("Rho passed: "+str(rho_pass/total_events * 100)+"%")
        print("DeltaR passed: "+str(dR_pass/total_events * 100)+"%")
	print("Passing Events: "+str(pass_pass/total_events * 100)+"%")
	print("Failing Events: "+str(fail_pass/total_events * 100)+"%")
	

def SamplePro(sample, fname, cut_hist, percentage=20):
	gROOT.SetBatch(True)

	ofile = ROOT.TFile("RData_"+ fname + ".root", "RECREATE")
	ofile.cd()

	ROOT.ROOT.EnableImplicitMT()


        rho_bins = cut_hist.GetNbinsX()
       	pt_bins = cut_hist.GetNbinsY()
	
	
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



	MakeHist(Chain, cut_hist, ofile, fname, sample[0][1])



	ofile.Write()

