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

	ofile = ROOT.TFile("RData_Cutoffs_nano.root", "RECREATE")
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
                                        if(pt[i]>220 && abs(eta[i])<2.4 && msoft[i]>0 && jID[i]>=2)
                                        {
                                                return i;
                                        }
                                }
                                return -1;
                        }

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<int> pID)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(pt[i]>220 && abs(eta[i])<1.44 && pID[i] >= 3)
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
                                float deta = abs(eta1 - eta2);
                                float dphi = abs(phi1 - phi2);
                                if(dphi > M_PI)
                                {
                                        dphi -= float(2*M_PI);
                                }
                                return sqrt(pow(deta, 2) + pow(dphi, 2));
                        }
                        '''
        prompt_code =   '''
                        bool dir_prompt(int nGenPart, RVec<int> gen_status, RVec<int> gen_mother, RVec<int> gen_pdg, RVec<float> gen_phi, RVec<float> gen_eta)
                        {
                                for(int i=0; i < nGenPart; i++)
                                {
                                        if(gen_status[i] != 1 || (gen_mother[i] > 22 && gen_mother[i] != 2212))
                                        {
                                                continue;
                                        }
                                        //past this point are prompt photons
                                        for(int j=0; j < nGenPart; j++)
                                        {
                                                if(j == i) //if j is examined photon skip
                                                {
                                                        continue;
                                                }
                                                if((gen_pdg[j] <= 9 || gen_pdg[i] == 21) && gen_status[j] == 23)
                                                {
                                                        if(deltaR(gen_eta[i], gen_eta[j], gen_phi[i], gen_phi[j]) > .4)
                                                        {
                                                                return true;
                                                        }
                                                }
                                        }
                                }
                                return false;
                        }
                        '''
        submass_code =  '''
                        float submass(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2)
                        {
                                TLorentzVector v1 = TLorentzVector();
                                TLorentzVector v2 = TLorentzVector();

                                v1.SetPtEtaPhiM(pt1, eta1, phi1, m1);
                                v2.SetPtEtaPhiM(pt2, eta2, phi2, m2);

                                return (v1 + v2).M();

                        }
                        '''

        JMC_code =      '''
                        float JMC_corr(float sdm, float pt, float eta)
                        {
                                float x = sdm/pt;
                                float y = log(pt);
                                float z = eta;

				float corr = -1.7677365131607674+-0.7429958086003288*z+-2.025282239123113*pow(z,2)+0.9517559457308561*pow(z,3)+1.5132658053401622*pow(z,4)+-0.1795148819508862*pow(z,5)+-0.19807400217068177*pow(z,6)+1.0904862924242777*y+0.2410435245810032*y*z+0.5967638354157488*y*pow(z,2)+-0.3149072573691545*y*pow(z,3)+-0.4683023177121198*y*pow(z,4)+0.0604571508349716*y*pow(z,5)+0.06125275741769842*y*pow(z,6)+-0.09760148720762943*pow(y,2)+-0.019452046087440722*pow(y,2)*z+-0.04415125142540788*pow(y,2)*pow(z,2)+0.02601282752108569*pow(y,2)*pow(z,3)+0.03574261738660586*pow(y,2)*pow(z,4)+-0.005088934511006227*pow(y,2)*pow(z,5)+-0.004627550913670786*pow(y,2)*pow(z,6)+16.51394877392092*x+12.119287569200438*x*z+35.59150369481447*x*pow(z,2)+-17.803800245447825*x*pow(z,3)+-26.094626703791427*x*pow(z,4)+3.231234672069579*x*pow(z,5)+3.8488932179716078*x*pow(z,6)+-6.9001535114412675*x*y+-3.876768442725194*x*y*z+-10.878380313296745*x*y*pow(z,2)+5.8404470792633*x*y*pow(z,3)+8.21851075799449*x*y*pow(z,4)+-1.0752835668673804*x*y*pow(z,5)+-1.2240993280149777*x*y*pow(z,6)+0.6007815367709846*x*pow(y,2)+0.30866854928584786*x*pow(y,2)*z+0.8290672489383386*x*pow(y,2)*pow(z,2)+-0.4784421781377759*x*pow(y,2)*pow(z,3)+-0.640696555869031*x*pow(y,2)*pow(z,4)+0.0894853690426416*x*pow(y,2)*pow(z,5)+0.09617914089292512*x*pow(y,2)*pow(z,6)+-29.141570024443627*pow(x,2)+-49.97954245264583*pow(x,2)*z+-176.50760682479572*pow(x,2)*pow(z,2)+89.43450974456483*pow(x,2)*pow(z,3)+123.36994818915969*pow(x,2)*pow(z,4)+-16.202688513762148*pow(x,2)*pow(z,5)+-18.28609784627234*pow(x,2)*pow(z,6)+10.738391284778862*pow(x,2)*y+15.571071086857401*pow(x,2)*y*z+54.580216933729815*pow(x,2)*y*pow(z,2)+-29.065103319958137*pow(x,2)*y*pow(z,3)+-38.77769382081733*pow(x,2)*y*pow(z,4)+5.333288274964675*pow(x,2)*y*pow(z,5)+5.798605161883083*pow(x,2)*y*pow(z,6)+-0.6699662223778642*pow(x,2)*pow(y,2)+-1.2076227999290925*pow(x,2)*pow(y,2)*z+-4.223213276414069*pow(x,2)*pow(y,2)*pow(z,2)+2.360746562525458*pow(x,2)*pow(y,2)*pow(z,3)+3.0250171837617525*pow(x,2)*pow(y,2)*pow(z,4)+-0.4394658738849859*pow(x,2)*pow(y,2)*pow(z,5)+-0.45558172558287424*pow(x,2)*pow(y,2)*pow(z,6)+-63.64650316857145*pow(x,3)+68.66014824263873*pow(x,3)*z+264.23338980476143*pow(x,3)*pow(z,2)+-139.83901691215453*pow(x,3)*pow(z,3)+-173.41714526632677*pow(x,3)*pow(z,4)+25.261715279036014*pow(x,3)*pow(z,5)+25.28477143621113*pow(x,3)*pow(z,6)+26.93059435963283*pow(x,3)*y+-20.82671785620973*pow(x,3)*y*z+-81.95594518831057*pow(x,3)*y*pow(z,2)+45.13146458474475*pow(x,3)*y*pow(z,3)+53.92393890627598*pow(x,3)*y*pow(z,4)+-8.249418530240968*pow(x,3)*y*pow(z,5)+-7.915529403221475*pow(x,3)*y*pow(z,6)+-3.012361892800792*pow(x,3)*pow(y,2)+1.571662769526669*pow(x,3)*pow(y,2)*z+6.383414470137923*pow(x,3)*pow(y,2)*pow(z,2)+-3.6428410245059215*pow(x,3)*pow(y,2)*pow(z,3)+-4.170212091831145*pow(x,3)*pow(y,2)*pow(z,4)+0.6748556886647457*pow(x,3)*pow(y,2)*pow(z,5)+0.6147838754649904*pow(x,3)*pow(y,2)*pow(z,6);

                                return corr;
                        }

                        '''
        ROOT.gInterpreter.Declare(includes)
        ROOT.gInterpreter.Declare(dr_code)

        match_code =    '''
                        RVec<int> ak4_match(int nJet, RVec<float> ak4_eta, RVec<float> ak4_phi, float eta, float phi, RVec<float> ak4_pt, RVec<float> btag) //now returns vector in decending order of b-tag score
                        {
                                RVec<int> match;
                                if(nJet == 0)
                                {
                                        match.push_back(-1);
                                        //cout << "Empty Vector!" << endl;
                                        return match;
                                }

                                for(int i=0; i<nJet; i++)
                                {
                                        if(deltaR(ak4_eta[i], eta, ak4_phi[i], phi) > 0.8 && abs(ak4_eta[i]) < 2.4 && ak4_pt[i] > 30)
                                        {
                                                match.push_back(i);
                                        }
                                }
                                if(match.size() == 0)
                                {
                                        match.push_back(-1);
                                        //cout << "Empty Vector!" << endl;
                                        return match;
                                }
                                //sort vector by b-tag score
                                int temp = 0;
                                for(int j=0; j<(match.size()-1); j++)
                                {
                                        for(int k=0; k<(match.size()-j-1); k++)
                                        {
                                                temp = -1;
                                                if(btag[match[k]] < btag[match[k+1]])
                                                {
                                                        temp = match[k];
                                                        match[k] = match[k+1];
                                                        match[k+1] = temp;
                                                }
                                        }
                                }
                                return match;
                        }
                        '''

        ak4_code =      '''
                        RVec<float> ak4_ret(RVec<int> match, RVec<float> var)
                        {
                                RVec<float> match_var;
                                if(match[0] == -1)
                                {
                                        match_var.push_back(-1000); //default for empty match vector
                                        return match_var;
                                }
                                for(int i=0; i<match.size(); i++)
                                {
                                //        cout << var[match[i]] << endl;
                                        match_var.push_back(var[match[i]]);
                                }
                                return match_var;
                        }
                        '''

	ROOT.gInterpreter.Declare(prompt_code)
        ROOT.gInterpreter.Declare(match_code)
        ROOT.gInterpreter.Declare(ak4_code)

        ROOT.gInterpreter.Declare(submass_code)
	ROOT.gInterpreter.Declare(rho_code)
	ROOT.gInterpreter.Declare(index_code)
	ROOT.gInterpreter.Declare(JMC_code)

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
		Rdf_PreSel = Rdf_noCut.Filter("nPhoton > 0.")
        	Rdf_PreSel = Rdf_PreSel.Filter("nselectedPatJetsAK8PFPuppi > 0.")

		Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nselectedPatJetsAK8PFPuppi, selectedPatJetsAK8PFPuppi_pt_nom, selectedPatJetsAK8PFPuppi_eta, selectedPatJetsAK8PFPuppi_msoftdrop_raw, selectedPatJetsAK8PFPuppi_jetId)")
        	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

		#Now Require GJets events must have direct prompt photons
		Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")

		Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	        Rdf = Rdf.Filter("jIndex >= 0")
		
		#Note I am using corrected softdrop mass

		Rdf = Rdf.Define("jM_uncorr", "selectedPatJetsAK8PFPuppi_msoftdrop_raw[jIndex]")
        	Rdf = Rdf.Define("jEta", "selectedPatJetsAK8PFPuppi_eta[jIndex]")
        	Rdf = Rdf.Define("jPhi", "selectedPatJetsAK8PFPuppi_phi[jIndex]")
        	Rdf = Rdf.Define("jPt", "selectedPatJetsAK8PFPuppi_pt_nom[jIndex]")
        	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
        	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
        	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
        	Rdf = Rdf.Define("N2", "selectedPatJetsAK8PFPuppi_ak8PFJetsPuppiSoftDropValueMap_nb1AK8PuppiSoftDropN2[jIndex]")
		Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
        	Rdf = Rdf.Define("jID", "selectedPatJetsAK8PFPuppi_jetId[jIndex]")
        	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")
		Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")

               	Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")
                Rdf = Rdf.Define("weight", F[1])
                Rdf = Rdf.Define("nj4", "nJet")
                Rdf = Rdf.Define("ak4_nomatch", "ak4_match(nj4, Jet_eta, Jet_phi, jEta, jPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that do NOT match the boosted AK8 jet sorted by btag score
                Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_nomatch, Jet_btagDeepFlavB)[0]")

                Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")

                Rdf_final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2 && (HLT_Photon200 >0.0) && PuppiMET_pt < 75 && jBtag < 0.0532")

		print("test1")
		print(float(Rdf_final.Count().GetValue()))

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

