import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from GJets_Processor_Percentage import *

if __name__ == "__main__":
	print("Starting Run")
	#GJets = [["/cms/xaastorage/NanoAOD/2018/JUNE19/NanoToolOutput/2018/v7/GJetsHTBinned/100to200", str(59.9 * 8640000.0/10125438.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/NanoToolOutput/2018/v7/GJetsHTBinned/200to400", str(59.9 * 2185000.0/19258533.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/NanoToolOutput/2018/v7/GJetsHTBinned/400to600", str(59.9 * 259900.0/4795233.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/NanoToolOutput/2018/v7/GJetsHTBinned/600toInf", str(59.9 * 85310.0/5044493.0)]]
	GJets = [["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/100to200", str(59.9 * 8640000.0/10125438.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/200to400", str(59.9 * 2183000.0/19755305.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/400to600", str(59.9 * 260200.0/4786197.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/600toInf", str(59.9 * 86589.0/4905665.0)]]

	cutfile = "./RData_Cutoffs.root"
	cf = TFile(cutfile)
	
	cut_hist = TH2F()
	cut_ID = "cuts_20"
        cf.GetObject(cut_ID, cut_hist)
	ROOT.gInterpreter.ProcessLine("auto cutoff = "+str(cut_ID)+";")


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


        ddt_code =      '''
                        //#include <cmath>
                        float rho(float pt, float msoft)
                        {
                                float r = log((msoft*msoft)/(pt*pt));
                                return r;
                        }
                        float ddt(float pt, float msoft, float n2)
                        {

                                float r = rho(pt, msoft);

                                int xbin = int(((r + 8.0)*2.0)+1.0);
                                int ybin = int((pt/50.0)+1.0);

                                return n2 - cutoff->GetBinContent(xbin, ybin);
                        }
                        '''
        region_code = "float a=20; float b=35;"

        index_code =    '''
                        int jet_index_define(int nJet, RVec<float> pt, RVec<float> eta, RVec<float> msoft, RVec<float> jID)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(pt[i]>100 && abs(eta[i])<2.4 && msoft[i]>0 && jID[i]>=2)
                                        {
                                                return i;
                                        }
                                }
                                return -1;
                        }

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<float> pID, RVec<float> r9)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(pt[i]>110 && abs(eta[i])<2.4 && pID[i] > 0.8 && r9[i] >= .1)
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
        cflow_code =    '''
                        bool PPT(RVec<float> ppt, int nPho)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(ppt[i] > 110)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool PETA(RVec<float> ppt, RVec<float> peta, int nPho)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(abs(peta[i]) < 2.4 && ppt[i] > 110)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool PID(RVec<float> ppt, RVec<float> peta, RVec<float> pID, int nPho, RVec<float> r9)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(abs(peta[i]) < 2.4 && ppt[i] > 110 && pID[i] > 0.8 && r9[i] >= .1)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool JPT(RVec<float> jpt, int nJet)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(jpt[i] >= 100)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool JETA(RVec<float> jpt, RVec<float> jeta, int nJet)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >= 100)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool JID(RVec<float> jpt, RVec<float> jeta, RVec<float> jID, int nJet)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >= 100 && jID[i] >= 2)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool JSOFT(RVec<float> jpt, RVec<float> jeta, RVec<float> jID, RVec<float> msoft, int nJet)
                        {
                                for(int i=0; i<nJet; i++)
                                {
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >= 100 && jID[i] >= 2 && msoft[i] > 0)
                                        {
                                                return true;
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
	prompt_code = 	'''
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

        ROOT.gInterpreter.Declare(submass_code)
        ROOT.gInterpreter.Declare(includes)
        ROOT.gInterpreter.Declare(ddt_code)
        ROOT.gInterpreter.Declare(region_code)
        ROOT.gInterpreter.Declare(index_code)
        ROOT.gInterpreter.Declare(dr_code)
        ROOT.gInterpreter.Declare(cflow_code)
        ROOT.gInterpreter.Declare(prompt_code)

	
	percentage = 20
	fname = "GJets_MVA1"
	Processor(GJets, fname, cut_hist, percentage)	
	
	

	print("GJets Finished")
