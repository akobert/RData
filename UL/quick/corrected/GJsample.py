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
                                        if(pt[i]>120 && abs(eta[i])<2.4 && msoft[i]>0 && jID[i]>=2)
                                        {
                                                return i;
                                        }
                                }
                                return -1;
                        }

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<float> pID)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(pt[i]>120 && abs(eta[i])<2.4 && pID[i] >= 3)
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
                                        if(ppt[i] >120)
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
                                        if(abs(peta[i]) < 2.4 && ppt[i] >120)
                                        {
                                                return true;
                                        }
                                }
                                return false;
                        }
                        bool PID(RVec<float> ppt, RVec<float> peta, RVec<float> pID, int nPho)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(abs(peta[i]) < 2.4 && ppt[i] >120 && pID[i] >= 3)
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
                                        if(jpt[i] >120)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >120)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >120 && jID[i] >= 2)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >120 && jID[i] >= 2 && msoft[i] > 0)
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

	JMC_code =      '''
                        float JMC_corr(float sdm, float pt, float eta)
                        {
                                float x = sdm/pt;
                                float y = log(pt);
                                float z = eta;

                                float corr = -2.6781040799918046+0.22805629598522514*z+3.822051715803456*pow(z,2)+-0.25847902822294455*pow(z,3)+-1.9906618990224196*pow(z,4)+1.281922906479581*y+-0.05764701838148456*y*z+-1.19157113243718*y*pow(z,2)+0.05219680526757439*y*pow(z,3)+0.6191658717004951*y*pow(z,4)+-0.10542490860541673*pow(y,2)+0.003543658797323268*pow(y,2)*z+0.09161372035308879*pow(y,2)*pow(z,2)+-0.002055209900798355*pow(y,2)*pow(z,3)+-0.04756513737251103*pow(y,2)*pow(z,4)+27.630454585882163*x+1.2282936699516687*x*z+-55.40737486287197*x*pow(z,2)+-2.187779079919814*x*pow(z,3)+33.15702069572564*x*pow(z,4)+-10.429551656104934*x*y+-0.5499045112809384*x*y*z+16.975213855410686*x*y*pow(z,2)+1.068294172219309*x*y*pow(z,3)+-10.11611193210793*x*y*pow(z,4)+0.8921511135152933*x*pow(y,2)+0.05341470306283691*x*pow(y,2)*z+-1.2903748632973944*x*pow(y,2)*pow(z,2)+-0.10958120465757243*x*pow(y,2)*pow(z,3)+0.7652144468987805*x*pow(y,2)*pow(z,4)+-137.30810879199973*pow(x,2)+1.4250938574300314*pow(x,2)*z+244.1697463305552*pow(x,2)*pow(z,2)+9.247850770150258*pow(x,2)*pow(z,3)+-152.18261576030096*pow(x,2)*pow(z,4)+48.839036081466745*pow(x,2)*y+0.4177982232027091*pow(x,2)*y*z+-74.07841375507141*pow(x,2)*y*pow(z,2)+-4.75164907296069*pow(x,2)*y*pow(z,3)+46.01949331355662*pow(x,2)*y*pow(z,4)+-4.057341551154323*pow(x,2)*pow(y,2)+-0.08921302773340045*pow(x,2)*pow(y,2)*z+5.598423211226944*pow(x,2)*pow(y,2)*pow(z,2)+0.4996626723315103*pow(x,2)*pow(y,2)*pow(z,3)+-3.4692972272553106*pow(x,2)*pow(y,2)*pow(z,4)+216.2197122699742*pow(x,3)+-16.996192143841746*pow(x,3)*z+-325.76986096501423*pow(x,3)*pow(z,2)+-6.080844349424701*pow(x,3)*pow(z,3)+209.04804420695004*pow(x,3)*pow(z,4)+-72.98169510125607*pow(x,3)*y+3.722596664298891*pow(x,3)*y*z+98.3189639862738*pow(x,3)*y*pow(z,2)+4.909585260625917*pow(x,3)*y*pow(z,3)+-62.93507064555101*pow(x,3)*y*pow(z,4)+5.906846026803585*pow(x,3)*pow(y,2)+-0.18199127362211698*pow(x,3)*pow(y,2)*z+-7.401431737695784*pow(x,3)*pow(y,2)*pow(z,2)+-0.5953145142530616*pow(x,3)*pow(y,2)*pow(z,3)+4.731801297000523*pow(x,3)*pow(y,2)*pow(z,4);

                                return corr;
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
	ROOT.gInterpreter.Declare(JMC_code)
	
	percentage = 20
	fname = "GJets_UL_20_quick_corr"
	Processor(GJets, fname, cut_hist, percentage)	
	
	

	print("GJets Finished")
