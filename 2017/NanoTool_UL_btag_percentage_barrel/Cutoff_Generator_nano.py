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

				//float corr = -2.025164719705561+-0.5140259110734045*z+0.037039697756029985*pow(z,2)+0.5443031156602056*pow(z,3)+0.382075985318862*pow(z,4)+-0.08380001510789203*pow(z,5)+-0.0999842647107955*pow(z,6)+1.1662862965099836*y+0.1385845834043816*y*z+-0.04984202576624602*y*pow(z,2)+-0.15377006163609108*y*pow(z,3)+-0.11856056857282526*y*pow(z,4)+0.022502440649922656*y*pow(z,5)+0.03354940763153698*y*pow(z,6)+-0.10306177286110155*pow(y,2)+-0.00904369899520463*pow(y,2)*z+0.006055700205388037*pow(y,2)*pow(z,2)+0.010643809210392097*pow(y,2)*pow(z,3)+0.009429485941518906*pow(y,2)*pow(z,4)+-0.001440116784911738*pow(y,2)*pow(z,5)+-0.002840138663855629*pow(y,2)*pow(z,6)+11.774273208826544*x+6.272781119920241*x*z+15.487247905409896*x*pow(z,2)+-7.862198761559968*x*pow(z,3)+-16.550406824266755*x*pow(z,4)+1.3073086413884958*x*pow(z,5)+4.051953194090605*x*pow(z,6)+-5.377141424165095*x*y+-1.6156575058847702*x*y*z+-4.92081677797172*x*y*pow(z,2)+2.2304019676380786*x*y*pow(z,3)+5.601960805237469*x*y*pow(z,4)+-0.3593108945860104*x*y*pow(z,5)+-1.3953987392294391*x*y*pow(z,6)+0.47453141291612333*x*pow(y,2)+0.09623198547250666*x*pow(y,2)*z+0.39748146681926233*x*pow(y,2)*pow(z,2)+-0.15342643048624094*x*pow(y,2)*pow(z,3)+-0.47768052867574884*x*pow(y,2)*pow(z,4)+0.02347268870853636*x*pow(y,2)*pow(z,5)+0.12060459712344263*x*pow(y,2)*pow(z,6)+2.3992463816780942*pow(x,2)+-10.757119753670795*pow(x,2)*z+-99.1842035373288*pow(x,2)*pow(z,2)+27.186098053072875*pow(x,2)*pow(z,3)+90.22559424072583*pow(x,2)*pow(z,4)+-4.935193987643966*pow(x,2)*pow(z,5)+-21.79311223252144*pow(x,2)*pow(z,6)+0.4507229194551865*pow(x,2)*y+1.3203970735855592*pow(x,2)*y*z+32.38999606334254*pow(x,2)*y*pow(z,2)+-7.185272678775053*pow(x,2)*y*pow(z,3)+-30.601773516764748*pow(x,2)*y*pow(z,4)+1.284203108104069*pow(x,2)*y*pow(z,5)+7.49413314060847*pow(x,2)*y*pow(z,6)+0.19171465764175633*pow(x,2)*pow(y,2)+0.07477940414212458*pow(x,2)*pow(y,2)*z+-2.6811366191409913*pow(x,2)*pow(y,2)*pow(z,2)+0.4408574546784374*pow(x,2)*pow(y,2)*pow(z,3)+2.6124216003379086*pow(x,2)*pow(y,2)*pow(z,4)+-0.07601035867524963*pow(x,2)*pow(y,2)*pow(z,5)+-0.6463645019378834*pow(x,2)*pow(y,2)*pow(z,6)+-157.44701323685382*pow(x,3)+-6.290874057056821*pow(x,3)*z+174.84378561745652*pow(x,3)*pow(z,2)+-29.17480356061592*pow(x,3)*pow(z,3)+-136.87219242690315*pow(x,3)*pow(z,4)+6.312623181378316*pow(x,3)*pow(z,5)+32.65389596638383*pow(x,3)*pow(z,6)+57.87646554689217*pow(x,3)*y+5.530827588781179*pow(x,3)*y*z+-57.449510455581205*pow(x,3)*y*pow(z,2)+6.81298706357242*pow(x,3)*y*pow(z,3)+46.08067823582773*pow(x,3)*y*pow(z,4)+-1.5564840912505011*pow(x,3)*y*pow(z,5)+-11.159781937223055*pow(x,3)*y*pow(z,6)+-5.60105318836044*pow(x,3)*pow(y,2)+-0.7413886626423871*pow(x,3)*pow(y,2)*z+4.789176299539881*pow(x,3)*pow(y,2)*pow(z,2)+-0.32279246667682626*pow(x,3)*pow(y,2)*pow(z,3)+-3.910340414108277*pow(x,3)*pow(y,2)*pow(z,4)+0.08250062386442725*pow(x,3)*pow(y,2)*pow(z,5)+0.9569105821367216*pow(x,3)*pow(y,2)*pow(z,6);
				float corr = -2.3130685607003336+-0.1512472133634402*z+0.3956321776814697*pow(z,2)+0.19468804550014523*pow(z,3)+0.19537219002117645*pow(z,4)+-0.013761534102992433*pow(z,5)+-0.07154744603234295*pow(z,6)+1.2608638616300327*y+0.021813490541564173*y*z+-0.17503907604912344*y*pow(z,2)+-0.040942152005053634*y*pow(z,3)+-0.052059536097167514*y*pow(z,4)+-0.00023058845419857144*y*pow(z,5)+0.023277630375435787*y*pow(z,6)+-0.11088070451598911*pow(y,2)+0.00033482130540041233*pow(y,2)*z+0.01692202402080406*pow(y,2)*pow(z,2)+0.0015625069624542048*pow(y,2)*pow(z,3)+0.003502595806937403*pow(y,2)*pow(z,4)+0.00040029230564175844*pow(y,2)*pow(z,5)+-0.0019106073224789133*pow(y,2)*pow(z,6)+15.94175512266266*x+-0.30312732815513*x*z+7.679313289686396*x*pow(z,2)+-1.7030496734961993*x*pow(z,3)+-13.29708076389269*x*pow(z,4)+0.08517715899562897*x*pow(z,5)+3.6934558662267856*x*pow(z,6)+-6.758518464529408*x*y+0.4822032871366592*x*y*z+-2.302172859364022*x*y*pow(z,2)+0.2635837524551365*x*y*pow(z,3)+4.490843721659719*x*y*pow(z,4)+0.033985271268613726*x*y*pow(z,5)+-1.2702395796333983*x*y*pow(z,6)+0.5886046836924788*x*pow(y,2)+-0.07087362605496494*x*pow(y,2)*z+0.17829258257992464*x*pow(y,2)*pow(z,2)+0.003398591115968963*x*pow(y,2)*pow(z,3)+-0.3825310986950292*x*pow(y,2)*pow(z,4)+-0.008138975252995007*x*pow(y,2)*pow(z,5)+0.10961704921748383*x*pow(y,2)*pow(z,6)+-18.768847040559052*pow(x,2)+24.9685008748653*pow(x,2)*z+-43.98002840115775*pow(x,2)*pow(z,2)+-5.90124599053705*pow(x,2)*pow(z,3)+65.79888363392033*pow(x,2)*pow(z,4)+1.4621307069230607*pow(x,2)*pow(z,5)+-18.918399644511528*pow(x,2)*pow(z,6)+7.458958357170526*pow(x,2)*y+-9.997542927433216*pow(x,2)*y*z+14.001885088954635*pow(x,2)*y*pow(z,2)+3.2960228706334913*pow(x,2)*y*pow(z,3)+-22.330157625019343*pow(x,2)*y*pow(z,4)+-0.757304010379688*pow(x,2)*y*pow(z,5)+6.505461555561464*pow(x,2)*y*pow(z,6)+-0.3865305932753511*pow(x,2)*pow(y,2)+0.9700969155576642*pow(x,2)*pow(y,2)*z+-1.1514197287376184*pow(x,2)*pow(y,2)*pow(z,2)+-0.3881477867742644*pow(x,2)*pow(y,2)*pow(z,3)+1.9106409017997752*pow(x,2)*pow(y,2)*pow(z,4)+0.08671130909064573*pow(x,2)*pow(y,2)*pow(z,5)+-0.5609958799591936*pow(x,2)*pow(y,2)*pow(z,6)+-127.26975232289175*pow(x,3)+-63.27503404047485*pow(x,3)*z+65.47764566347806*pow(x,3)*pow(z,2)+23.644449371791442*pow(x,3)*pow(z,3)+-85.6983201857925*pow(x,3)*pow(z,4)+-3.6383787689245755*pow(x,3)*pow(z,5)+26.2798571724315*pow(x,3)*pow(z,6)+47.90381426051584*pow(x,3)*y+23.467550380545063*pow(x,3)*y*z+-21.02379677741606*pow(x,3)*y*pow(z,2)+-9.793758380413388*pow(x,3)*y*pow(z,3)+28.74519958586503*pow(x,3)*y*pow(z,4)+1.5919696067251023*pow(x,3)*y*pow(z,5)+-8.971739329856897*pow(x,3)*y*pow(z,6)+-4.779015644382648*pow(x,3)*pow(y,2)+-2.1509509587167344*pow(x,3)*pow(y,2)*z+1.7573549588862094*pow(x,3)*pow(y,2)*pow(z,2)+0.9805175074743815*pow(x,3)*pow(y,2)*pow(z,3)+-2.439790611054416*pow(x,3)*pow(y,2)*pow(z,4)+-0.16625501792459518*pow(x,3)*pow(y,2)*pow(z,5)+0.7686002157301313*pow(x,3)*pow(y,2)*pow(z,6);

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

		#Rdf_final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2 && (HLT_Photon110EB_TightID_TightIso > 0. || HLT_Photon200 >0.0) && PuppiMET_pt < 75 && jBtag < 0.0532")
		Rdf_final = Rdf.Filter("N2 >= 0.0 && Rho > -7 && Rho < -2  && dR >= 2.2 && HLT_Photon200 >0.0 && PuppiMET_pt < 75 && jBtag < 0.0532")
		

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

