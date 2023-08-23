import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

sys.path.insert(1, '/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/')
from Analysis_Processor_nano import *

if __name__ == "__main__":
	print("Starting Run")


	#files = [["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present", str(1.0), 1],["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_missing", str(1.0), 2], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunB/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunC/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunD/", str(1.0), 1]]
	files = ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root", str(1.0), 1]

	cutfile = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/NanoTool_UL_btag_percentage_barrel/RData_Cutoffs_nano.root"
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
        region_code = "float a=100; float b=300; float c=20; float d=35;"

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

                        int photon_index_define(int nPho, RVec<float> pt, RVec<float> eta, RVec<float> pID)
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
        cflow_code =    '''
                        bool PPT(RVec<float> ppt, int nPho)
                        {
                                for(int i=0; i<nPho; i++)
                                {
                                        if(ppt[i] >200)
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
                                        if(abs(peta[i]) < 1.44 && ppt[i] >200)
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
                                        if(abs(peta[i]) < 1.44 && ppt[i] >200 && pID[i] >= 3)
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
                                        if(jpt[i] >200)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >200)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >200 && jID[i] >= 2)
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
                                        if(abs(jeta[i]) < 2.4 && jpt[i] >200 && jID[i] >= 2 && msoft[i] > 0)
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

        ROOT.gInterpreter.Declare(includes)
        ROOT.gInterpreter.Declare(dr_code)

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
        ROOT.gInterpreter.Declare(prompt_code)

        JMC_code =      '''
                        float JMC_corr(float sdm, float pt, float eta)
                        {
                                float x = sdm/pt;
                                float y = log(pt);
                                float z = eta;
				float corr = -2.4745403973317837+0.23753091987946806*z+4.925353593370313*pow(z,2)+-2.530857263055647*pow(z,3)+-0.2520959209106019*pow(z,4)+0.6756424585724189*pow(z,5)+-0.31691066142859414*pow(z,6)+1.2146923035474209*y+-0.15528779058061698*y*z+-1.4226133583093474*y*pow(z,2)+0.8562674943440518*y*pow(z,3)+0.035002398192904405*y*pow(z,4)+-0.22185472630279834*y*pow(z,5)+0.10561402945388013*y*pow(z,6)+-0.09982078709644471*pow(y,2)+0.017423805250361524*pow(y,2)*z+0.10089928587289848*pow(y,2)*pow(z,2)+-0.07080515704181325*pow(y,2)*pow(z,3)+0.001724051062261922*pow(y,2)*pow(z,4)+0.01791086402243891*pow(y,2)*pow(z,5)+-0.00893818303550728*pow(y,2)*pow(z,6)+49.92738293849151*x+-14.803616086388146*x*z+-78.02057882564986*x*pow(z,2)+59.12410184099671*x*pow(z,3)+22.34265151315238*x*pow(z,4)+-16.799781749879827*x*pow(z,5)+-1.0580391770472288*x*pow(z,6)+-17.152900662043653*x*y+5.8424133898382635*x*y*z+22.326674416171794*x*y*pow(z,2)+-19.672981426904272*x*y*pow(z,3)+-6.331512708870987*x*y*pow(z,4)+5.515405752506041*x*y*pow(z,5)+0.3055285954413165*x*y*pow(z,6)+1.3879066785417145*x*pow(y,2)+-0.5369524492674032*x*pow(y,2)*z+-1.5759115278506073*x*pow(y,2)*pow(z,2)+1.6128191725806857*x*pow(y,2)*pow(z,3)+0.42767532089865234*x*pow(y,2)*pow(z,4)+-0.4479122145013683*x*pow(y,2)*pow(z,5)+-0.01893918992129251*x*pow(y,2)*pow(z,6)+-249.2731636659133*pow(x,2)+93.29949721756607*pow(x,2)*z+343.62289633969436*pow(x,2)*pow(z,2)+-313.8060220674564*pow(x,2)*pow(z,3)+-150.28457119774802*pow(x,2)*pow(z,4)+90.15982324459115*pow(x,2)*pow(z,5)+24.87028032528544*pow(x,2)*pow(z,6)+81.6773654437746*pow(x,2)*y+-34.88028327284992*pow(x,2)*y*z+-98.53186532009046*pow(x,2)*y*pow(z,2)+104.36387382209475*pow(x,2)*y*pow(z,3)+45.56614117926423*pow(x,2)*y*pow(z,4)+-29.713454538744116*pow(x,2)*y*pow(z,5)+-8.26756220696175*pow(x,2)*y*pow(z,6)+-6.381737568473227*pow(x,2)*pow(y,2)+3.1084994435336597*pow(x,2)*pow(y,2)*z+6.992416861290316*pow(x,2)*pow(y,2)*pow(z,2)+-8.56764952718844*pow(x,2)*pow(y,2)*pow(z,3)+-3.404919925967576*pow(x,2)*pow(y,2)*pow(z,4)+2.4257555330776057*pow(x,2)*pow(y,2)*pow(z,5)+0.677562542943809*pow(x,2)*pow(y,2)*pow(z,6)+325.63747455530745*pow(x,3)+-188.35744481698828*pow(x,3)*z+-508.13830535777555*pow(x,3)*pow(z,2)+509.46256922940574*pow(x,3)*pow(z,3)+284.76540976034113*pow(x,3)*pow(z,4)+-141.6711223338959*pow(x,3)*pow(z,5)+-59.61843203842773*pow(x,3)*pow(z,6)+-101.58456386632785*pow(x,3)*y+67.94379804667597*pow(x,3)*y*z+147.9269918157215*pow(x,3)*y*pow(z,2)+-169.86753910744608*pow(x,3)*y*pow(z,3)+-89.89477255632804*pow(x,3)*y*pow(z,4)+46.900571080956674*pow(x,3)*y*pow(z,5)+20.210518847017042*pow(x,3)*y*pow(z,6)+7.54538935338082*pow(x,3)*pow(y,2)+-5.931864133004979*pow(x,3)*pow(y,2)*z+-10.708476435930228*pow(x,3)*pow(y,2)*pow(z,2)+13.998882543288316*pow(x,3)*pow(y,2)*pow(z,3)+7.067902362827244*pow(x,3)*pow(y,2)*pow(z,4)+-3.848928287816829*pow(x,3)*pow(y,2)*pow(z,5)+-1.701976288483138*pow(x,3)*pow(y,2)*pow(z,6);
	
                                return corr;
                        }

                        '''

	match_code = 	'''
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
                                        cout << "Empty Vector!" << endl;
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
        ak4_code =    	'''
                        RVec<float> ak4_ret(RVec<int> match, RVec<float> var)
                        {
                                RVec<float> match_var;
				if(match[0] == -1)
				{
					match_var.push_back(-1000); //default for empty match
					return match_var;
				}
                                for(int i=0; i<match.size(); i++)
                                {
					//cout << var[match[i]] << endl;
					match_var.push_back(var[match[i]]);
                                }

                                return match_var;
                        }
                        '''
	HT_code = 	'''
			float HT(RVec<float> pt, RVec<float> eta)
			{
				float ht = 0;
				
				for(int i=0; i<pt.size(); i++)
				{
					if(pt[i]>80 && abs(eta[i]) < 2.4)
					{
						ht += pt[i];
					}
				}
				return ht;
			}
			'''
	ROOT.gInterpreter.Declare(HT_code)

	HT_AK8_code = 	'''
			float HT_AK8(RVec<float> pt, RVec<float> eta)
			{
				float ht = 0;
				
				for(int i=0; i<pt.size(); i++)
				{
					if(pt[i]>200 && abs(eta[i]) < 2.4)
					{
						ht += pt[i];
					}
				}
				return ht;
			}
			'''
	ROOT.gInterpreter.Declare(HT_AK8_code)


	ROOT.gInterpreter.Declare(match_code)
	ROOT.gInterpreter.Declare(ak4_code)

        ROOT.gInterpreter.Declare(submass_code)
        ROOT.gInterpreter.Declare(ddt_code)
        ROOT.gInterpreter.Declare(region_code)
        ROOT.gInterpreter.Declare(index_code)
        ROOT.gInterpreter.Declare(cflow_code)
	ROOT.gInterpreter.Declare(JMC_code)

	
	percentage = 20
	fname = "DataA_present_UL_0"
	DataPro(files, fname, cut_hist, percentage)	
	
	

	print("All Data Finished")
