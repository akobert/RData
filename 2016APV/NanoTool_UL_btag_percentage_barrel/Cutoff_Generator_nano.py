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

	#ROOT.ROOT.EnableImplicitMT()


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

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<int> pID)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(pt[i]>200 && abs(eta[i])<1.44 && pID[i] >= 3)
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

			//	float corr = -2.4745403973317837+0.23753091987946806*z+4.925353593370313*pow(z,2)+-2.530857263055647*pow(z,3)+-0.2520959209106019*pow(z,4)+0.6756424585724189*pow(z,5)+-0.31691066142859414*pow(z,6)+1.2146923035474209*y+-0.15528779058061698*y*z+-1.4226133583093474*y*pow(z,2)+0.8562674943440518*y*pow(z,3)+0.035002398192904405*y*pow(z,4)+-0.22185472630279834*y*pow(z,5)+0.10561402945388013*y*pow(z,6)+-0.09982078709644471*pow(y,2)+0.017423805250361524*pow(y,2)*z+0.10089928587289848*pow(y,2)*pow(z,2)+-0.07080515704181325*pow(y,2)*pow(z,3)+0.001724051062261922*pow(y,2)*pow(z,4)+0.01791086402243891*pow(y,2)*pow(z,5)+-0.00893818303550728*pow(y,2)*pow(z,6)+49.92738293849151*x+-14.803616086388146*x*z+-78.02057882564986*x*pow(z,2)+59.12410184099671*x*pow(z,3)+22.34265151315238*x*pow(z,4)+-16.799781749879827*x*pow(z,5)+-1.0580391770472288*x*pow(z,6)+-17.152900662043653*x*y+5.8424133898382635*x*y*z+22.326674416171794*x*y*pow(z,2)+-19.672981426904272*x*y*pow(z,3)+-6.331512708870987*x*y*pow(z,4)+5.515405752506041*x*y*pow(z,5)+0.3055285954413165*x*y*pow(z,6)+1.3879066785417145*x*pow(y,2)+-0.5369524492674032*x*pow(y,2)*z+-1.5759115278506073*x*pow(y,2)*pow(z,2)+1.6128191725806857*x*pow(y,2)*pow(z,3)+0.42767532089865234*x*pow(y,2)*pow(z,4)+-0.4479122145013683*x*pow(y,2)*pow(z,5)+-0.01893918992129251*x*pow(y,2)*pow(z,6)+-249.2731636659133*pow(x,2)+93.29949721756607*pow(x,2)*z+343.62289633969436*pow(x,2)*pow(z,2)+-313.8060220674564*pow(x,2)*pow(z,3)+-150.28457119774802*pow(x,2)*pow(z,4)+90.15982324459115*pow(x,2)*pow(z,5)+24.87028032528544*pow(x,2)*pow(z,6)+81.6773654437746*pow(x,2)*y+-34.88028327284992*pow(x,2)*y*z+-98.53186532009046*pow(x,2)*y*pow(z,2)+104.36387382209475*pow(x,2)*y*pow(z,3)+45.56614117926423*pow(x,2)*y*pow(z,4)+-29.713454538744116*pow(x,2)*y*pow(z,5)+-8.26756220696175*pow(x,2)*y*pow(z,6)+-6.381737568473227*pow(x,2)*pow(y,2)+3.1084994435336597*pow(x,2)*pow(y,2)*z+6.992416861290316*pow(x,2)*pow(y,2)*pow(z,2)+-8.56764952718844*pow(x,2)*pow(y,2)*pow(z,3)+-3.404919925967576*pow(x,2)*pow(y,2)*pow(z,4)+2.4257555330776057*pow(x,2)*pow(y,2)*pow(z,5)+0.677562542943809*pow(x,2)*pow(y,2)*pow(z,6)+325.63747455530745*pow(x,3)+-188.35744481698828*pow(x,3)*z+-508.13830535777555*pow(x,3)*pow(z,2)+509.46256922940574*pow(x,3)*pow(z,3)+284.76540976034113*pow(x,3)*pow(z,4)+-141.6711223338959*pow(x,3)*pow(z,5)+-59.61843203842773*pow(x,3)*pow(z,6)+-101.58456386632785*pow(x,3)*y+67.94379804667597*pow(x,3)*y*z+147.9269918157215*pow(x,3)*y*pow(z,2)+-169.86753910744608*pow(x,3)*y*pow(z,3)+-89.89477255632804*pow(x,3)*y*pow(z,4)+46.900571080956674*pow(x,3)*y*pow(z,5)+20.210518847017042*pow(x,3)*y*pow(z,6)+7.54538935338082*pow(x,3)*pow(y,2)+-5.931864133004979*pow(x,3)*pow(y,2)*z+-10.708476435930228*pow(x,3)*pow(y,2)*pow(z,2)+13.998882543288316*pow(x,3)*pow(y,2)*pow(z,3)+7.067902362827244*pow(x,3)*pow(y,2)*pow(z,4)+-3.848928287816829*pow(x,3)*pow(y,2)*pow(z,5)+-1.701976288483138*pow(x,3)*pow(y,2)*pow(z,6);
				float corr = -2.400581670784209+0.07017280462805661*z+4.826753283325524*pow(z,2)+-2.5995979055659926*pow(z,3)+-0.10585882188232407*pow(z,4)+0.735399768576503*pow(z,5)+-0.3771995736013154*pow(z,6)+1.1931316130746445*y+-0.10676274976869475*y*z+-1.3871990545227375*y*pow(z,2)+0.8808906241272851*y*pow(z,3)+-0.015000102827152723*y*pow(z,4)+-0.24088500202507923*y*pow(z,5)+0.1255445810607451*y*pow(z,6)+-0.09824818349964035*pow(y,2)+0.013926365474772384*pow(y,2)*z+0.09781674853836711*pow(y,2)*pow(z,2)+-0.07293554386952106*pow(y,2)*pow(z,3)+0.005910921294691701*pow(y,2)*pow(z,4)+0.01940630304158275*pow(y,2)*pow(z,5)+-0.010566283492013981*pow(y,2)*pow(z,6)+48.336171620336906*x+-11.8005131967152*x*z+-75.78812009222547*x*pow(z,2)+59.06587399436351*x*pow(z,3)+19.7748623352216*x*pow(z,4)+-17.348818102778708*x*pow(z,5)+-0.27496830069233913*x*pow(z,6)+-16.70239900092191*x*y+4.97802023210963*x*y*z+21.552195142587703*x*y*pow(z,2)+-19.72961128246493*x*y*pow(z,3)+-5.4679110419222345*x*y*pow(z,4)+5.697746419621026*x*y*pow(z,5)+0.049537060975632485*x*y*pow(z,6)+1.3555603581153122*x*pow(y,2)+-0.4753358746548546*x*pow(y,2)*z+-1.510814519058977*x*pow(y,2)*pow(z,2)+1.6226575407479977*x*pow(y,2)*pow(z,3)+0.35705562915257616*x*pow(y,2)*pow(z,4)+-0.4627637980265007*x*pow(y,2)*pow(z,5)+0.0015780428596232632*x*pow(y,2)*pow(z,6)+-242.63523900649142*pow(x,2)+79.59669017745854*pow(x,2)*z+339.4528319435343*pow(x,2)*pow(z,2)+-313.43732528697655*pow(x,2)*pow(z,3)+-144.94310129825078*pow(x,2)*pow(z,4)+92.14290171452834*pow(x,2)*pow(z,5)+23.05798551340166*pow(x,2)*pow(z,6)+79.77556047239908*pow(x,2)*y+-31.059838148185936*pow(x,2)*y*z+-96.99553116671206*pow(x,2)*y*pow(z,2)+104.73290985564115*pow(x,2)*y*pow(z,3)+43.771098724610724*pow(x,2)*y*pow(z,4)+-30.40677297910865*pow(x,2)*y*pow(z,5)+-7.6901091372401655*pow(x,2)*y*pow(z,6)+-6.241359141919041*pow(x,2)*pow(y,2)+2.847180263036366*pow(x,2)*pow(y,2)*z+6.860436888678411*pow(x,2)*pow(y,2)*pow(z,2)+-8.632487947691654*pow(x,2)*pow(y,2)*pow(z,3)+-3.2626883061794665*pow(x,2)*pow(y,2)*pow(z,4)+2.4846745424255445*pow(x,2)*pow(y,2)*pow(z,5)+0.6333387871225113*pow(x,2)*pow(y,2)*pow(z,6)+315.37711798641425*pow(x,3)+-171.78297981762975*pow(x,3)*z+-521.1453508295931*pow(x,3)*pow(z,2)+511.68383023547375*pow(x,3)*pow(z,3)+293.29568166022443*pow(x,3)*pow(z,4)+-144.41434995751746*pow(x,3)*pow(z,5)+-60.29935591102161*pow(x,3)*pow(z,6)+-98.45816714975405*pow(x,3)*y+63.66116823199033*pow(x,3)*y*z+151.8591129416519*pow(x,3)*y*pow(z,2)+-171.48824054005112*pow(x,3)*y*pow(z,3)+-92.6343898440522*pow(x,3)*y*pow(z,4)+47.90302565102922*pow(x,3)*y*pow(z,5)+20.46165181432913*pow(x,3)*y*pow(z,6)+7.296683320050363*pow(x,3)*pow(y,2)+-5.670134914218804*pow(x,3)*pow(y,2)*z+-11.011808885824742*pow(x,3)*pow(y,2)*pow(z,2)+14.195912623356769*pow(x,3)*pow(y,2)*pow(z,3)+7.297446486487428*pow(x,3)*pow(y,2)*pow(z,4)+-3.9373135518365068*pow(x,3)*pow(y,2)*pow(z,5)+-1.7268180632239307*pow(x,3)*pow(y,2)*pow(z,6);
				
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
					cout << "Empty Vector!" << endl;
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
        	Rdf_PreSel = Rdf_PreSel.Filter("nFatJet > 0.")

		Rdf_PreSel = Rdf_PreSel.Define("jIndex", "jet_index_define(nFatJet, FatJet_pt_nom, FatJet_eta, FatJet_msoftdrop_raw, FatJet_jetId)")
        	Rdf_PreSel = Rdf_PreSel.Define("pIndex", "photon_index_define(nPhoton, Photon_pt, Photon_eta, Photon_cutBased)")

                #Now Require GJets events must have direct prompt photons
                Rdf_PreSel = Rdf_PreSel.Filter("dir_prompt(nGenPart, GenPart_status, GenPart_genPartIdxMother, GenPart_pdgId, GenPart_phi, GenPart_eta)")


		Rdf = Rdf_PreSel.Filter("pIndex >= 0")
	        Rdf = Rdf.Filter("jIndex >= 0")
		
		#Note I am using corrected softdrop mass

		if sample[3] == "data":
			Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]")
		else:
			Rdf = Rdf.Define("jM_uncorr", "FatJet_msoftdrop_raw[jIndex]*FatJet_corr_JER[jIndex]")
        	Rdf = Rdf.Define("jEta", "FatJet_eta[jIndex]")
        	Rdf = Rdf.Define("jPhi", "FatJet_phi[jIndex]")
        	Rdf = Rdf.Define("jPt", "FatJet_pt_nom[jIndex]")
        	Rdf = Rdf.Define("pPt", "Photon_pt[pIndex]")
        	Rdf = Rdf.Define("pEta", "Photon_eta[pIndex]")
        	Rdf = Rdf.Define("pPhi", "Photon_phi[pIndex]")
        	Rdf = Rdf.Define("N2", "FatJet_n2b1[jIndex]")
		Rdf = Rdf.Define("jM", "jM_uncorr*JMC_corr(jM_uncorr,jPt,jEta)")
        	Rdf = Rdf.Define("jID", "FatJet_jetId[jIndex]")
        	Rdf = Rdf.Define("Rho", "rho(jPt, jM)")
		Rdf = Rdf.Define("dR", "deltaR(jEta, pEta, jPhi, pPhi)")

               	Rdf = Rdf.Define("pCut", "Photon_cutBased[pIndex]")
                Rdf = Rdf.Define("weight", F[1])

	        Rdf = Rdf.Define("nj4", "nJet")
	        Rdf = Rdf.Define("ak4_nomatch", "ak4_match(nj4, Jet_eta, Jet_phi, jEta, jPhi, Jet_pt, Jet_btagDeepFlavB)") #AK4 IDs that do NOT match the boosted AK8 jet sorted by btag score
	        Rdf = Rdf.Define("jBtag", "ak4_ret(ak4_nomatch, Jet_btagDeepFlavB)[0]")

	        Rdf = Rdf.Define("PuppiMETpt", "PuppiMET_pt")

		#d1 = Rdf.Display("")
		#print(d1->Print())

#	        q6 = Rdf.Histo1D(("q6", "Btag", 100, 0, 1), "jBtag", "weight")
#	        q6 = q6.Clone()

#		ofile.WriteObject(q6, "test_btag")

		Rdf_final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2 && HLT_Photon175 >0.0 && PuppiMET_pt < 75 && jBtag < 0.0480")
		

		print("test1")
		print(float(Rdf_final.Count().GetValue()))

		h0 = Rdf_final.Histo3D(("a"+str(label),  "Examined Data", rho_bin, -8, -1, pt_bin, 0, 2000, n2_bin, 0, .5), "Rho", "jPt", "N2", "weight")
	#	h0.Draw("COLZ")
		h0 = h0.Clone()
		label += 1
			
		h10.Add(h0)
		
		print("test2")		


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
					#Test Code
#					if (i<=10) and (j<=10):
					print("Rho: "+str(-8+(7.0/rho_bin * i)))
					print("pT: "+str(2000/pt_bin * j))
					print("Percentile "+str(percent)+" Cutoff: "+str(cutoffs.GetBinContent(i+1,j+1)))
					print("N2 Integral: "+str(temp.Integral()))
					cbin = int(cutoffs.GetBinContent(i+1,j+1)/(.5/n2_bin) + 1) #cutoff bin
					print("Events Below Cutoff: "+str(temp.Integral(1,cbin)))

		ofile.WriteObject(cutoffs, "cuts_"+str(percent))
		cut += .01
		
	
	ofile.Write()

