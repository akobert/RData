#
import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
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



def Cutoff(sample, rho_bin=14, pt_bin=40, n2_bin=500):

	#gROOT.SetBatch(True)

	ofile = ROOT.TFile("RData_Cutoffs_2016.root", "RECREATE")
	ofile.cd()

	ROOT.ROOT.EnableImplicitMT()


        includes =      '''
                        #include <boost/property_tree/ptree.hpp>
                        #include <boost/property_tree/json_parser.hpp>
                        #include <vector>
                        #include <stdexcept>
                        #include <string>
                        #include <algorithm>
                        #include <iostream>
                        #include <cmath>
                        #include "ROOT/RVec.hxx"

                        using namespace ROOT::VecOps;
                        using rvec_f = const RVec<float> &;
                        using rvec_b = const RVec<bool> &;
                        using rvec_i = const RVec<int> &;
                        using rvec_u = const RVec<unsigned int> &;

                        float GetByIndexF(int i, rvec_f THIS)   {return THIS[i];}
                        float GetByIndexI(int i, rvec_i THIS)   {return (float)THIS[i];}
                        float GetByIndexU(int i, rvec_u THIS)   {return (float)THIS[i];}
                        float GetByIndexB(int i, rvec_b THIS)   {if (THIS[i]) {return 1.0;} else {return 0.0;}}
                        '''

	rho_code =	'''
			#include <cmath>
			float rho(float pt, float msoft)
			{
				float r = log((msoft*msoft)/(pt*pt));
				return r;
			}
                    	'''
	index_code =    '''
                        int jet_index_define(int nJet, RVec<float> pt, RVec<float> eta, RVec<float> msoft, RVec<float> jID)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(pt[i]>200 && abs(eta[i])<2.4 && msoft[i]>0 && jID[i]>=2)
                                        {
                                                return i;
                                        }
                                }
                                return -1;
                        }

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<bool> pID)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(pt[i]>200 && abs(eta[i])<2.4 && pID[i])
                                        {
                                                return i;
                                        }
                                }
                                return -1;
                        }

                        int indexer(int index)
                        {
                                if(index >= 0)
                                {
                                        return index;
                                }
                                return 0;
                        }
                        '''
        dr_code =       '''
                        float deltaR(float eta1, float eta2, float phi1, float phi2)
                        {
                                return sqrt(pow(eta1 - eta2, 2) + pow(phi1 - phi2, 2));
                        }
                        '''

	ROOT.gInterpreter.Declare(includes)
	ROOT.gInterpreter.Declare(rho_code)
	ROOT.gInterpreter.Declare(index_code)
	ROOT.gInterpreter.Declare(dr_code)
	
	h10 = TH3F("h10",  "Examined Data", rho_bin, -8, -1, pt_bin, 0, 2000, n2_bin, 0, .5)


	label = 0
	
	h = np.empty(len(sample))

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
	#	Rdf_PreSel = Rdf_noCut.Filter("(HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon175 > 0) && nPhoton > 0. && nFatJet > 0. && FatJet_softdropMass.size()>0")
		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
        	Rdf_PreSel = Rdf_PreSel.Filter("nFatJet > 0.")

	#	Rdf_PreSel = Rdf_PreSel.Filter("FatJet_softdropMass.size()>0")

	
		#ROOT.gInterpreter.Declare('#include "Help.h"')
		Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt, FatJet_eta, FatJet_msoftdrop, FatJet_jetId)")
        	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_mvaID_WP90)")


		Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	        Rdf = Rdf.Filter("jIndex >= 0")

		Rdf = Rdf.Define("jM", "FatJet_msoftdrop[jIndex]")
        	Rdf = Rdf.Define("jEta", "FatJet_eta[jIndex]")
        	Rdf = Rdf.Define("jPhi", "FatJet_phi[jIndex]")
        	Rdf = Rdf.Define("jPt", "FatJet_pt[jIndex]")
        	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
        	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
        	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
        	Rdf = Rdf.Define("N2", "FatJet_n2b1[jIndex]")
        	Rdf = Rdf.Define("jID", "FatJet_jetId[jIndex]")
        	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")
		Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")
                Rdf = Rdf.Define("weight", F[1])

		#pEta requirement added to ensure this is a sideband of the data
		Rdf_final = Rdf.Filter("pEta >= 2.1 && N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2 && HLT_Photon175 >0.0")
		
		h0 = Rdf_final.Histo3D(("a"+str(label),  "Examined Data", rho_bin, -8, -1, pt_bin, 0, 2000, n2_bin, 0, .5), "Rho", "jPt", "N2", "weight")
	#	h0.Draw("COLZ")
		h0 = h0.Clone()
		label += 1
			
		h10.Add(h0)
		
		


	ofile.WriteObject(h10, "3Dhist")
	print("Events in Added Total Histogram is "+str(h10.GetEntries()))
	cutoffs = TH2F("cuts", "N2 Cutoffs", rho_bin, -8, -1, pt_bin, 0, 2000)
        cutoffs.SetStats(0)
	temp = TH1F("temp", "temp n2", n2_bin, 0, .5) #temporarily stores n2 for each rho/pt bin

	cut = .01


	for p in range(0,80):
		print("Percentile " + str(p+1))
		cutoffs.Reset()

		percent = p+1
		cutoffs.SetTitle("N2 Cutoffs "+str(percent)+"% DDT")

		#run over all rho and pt bins
		for i in range(rho_bin):
			#print("set ", i+1)
			for j in range(pt_bin):
				temp.Reset()
				Proj(i, j, n2_bin, temp, h10)
				#self.File.WriteObject(temp, "proj"+str(i+1)+'_'+str(j+1))     
				if temp.GetBinContent(temp.GetMaximumBin()) != 0:
					p = array('d', [cut])
					q = array('d', [0.0]*len(p))
					temp.GetQuantiles(len(p), q, p)
					cutoffs.SetBinContent(i+1, j+1, q[0])


		ofile.WriteObject(cutoffs, "cuts_"+str(percent))
		cut += .01
		
	
	ofile.Write()

