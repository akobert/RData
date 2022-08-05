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

def MakeHist(Chain, cut_hist, ofile, fname, weight, a, b, c, d, ifile):
	Rdf_noCut = RDF(Chain)
	C = Rdf_noCut.Count()
	total_events = float(C.GetValue())
#	print("File: "+ifile+" ")
#	print(str(C.GetValue())+" Events Before Cuts in "+fname+" Sample")

	if not hasattr(Chain, "HLT_Photon110EB_TightID_TightIso"):
		print("Missing Branch")
		print(ifile)
		

	

#	Rdf = Rdf.Define("total_weight", weight)


#	print("Non-Preselection Cuts Begin")

	

#	Rdf = Rdf.Filter("(HLT_Photon110EB_TightID_TightIso > 0.0 || HLT_Photon175 > 0.0)")
#	C = Rdf.Count()
#	print(str(C.GetValue())+" Events after Trigger requirements in "+fname+" Sample")

	

def DataPro(sample, fname, cut_hist, percentage=10, a=100, b=300, c=15, d=30):
	#a, b are jet pT signal region. c, d are softdrop mass window
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
					ifile = os.path.join(path, name) 
					#n = RDF(File).Count()
					#print n.GetValue()
					Chain.Add(File)
					MakeHist(Chain, cut_hist, ofile, fname, sample[0][1], a, b, c, d, ifile)
					Chain.Reset()


	ofile.Write()

