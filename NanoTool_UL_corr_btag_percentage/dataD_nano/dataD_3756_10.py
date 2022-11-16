import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

sys.path.insert(1, '/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/')
from Analysis_Processor_nano import *

if __name__ == "__main__":
	print("Starting Run")


	#files = [["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present", str(1.0), 1],["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_missing", str(1.0), 2], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunB/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunC/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunD/", str(1.0), 1]]
	files = ["/cms/akobert/NanoToolOutput/UL/EGamma_RunD/jetToolbox_dataD2018_4268.root", str(1.0), 1, "data"]

	cutfile = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/RData_Cutoffs_nano.root"
	cf = TFile(cutfile)
	
	cut_hist = TH2F()
	cut_ID = "cuts_10"
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


        JMC_code =      '''
                        float JMC_corr(float sdm, float pt, float eta)
                        {
                                float x = sdm/pt;
                                float y = log(pt);
                                float z = eta;

				float corr = -1.9343106921545696+0.318828229410817*z+0.41893961737062785*pow(z,2)+-0.15125039105355234*pow(z,3)+0.2078091910874115*pow(z,4)+0.0537114683776172*pow(z,5)+-0.03910068463556481*pow(z,6)+1.0697315844803388*y+-0.08751032173886875*y*z+-0.1554028483866286*y*pow(z,2)+0.03783240310716063*y*pow(z,3)+-0.06661055997471138*y*pow(z,4)+-0.015875103135748192*y*pow(z,5)+0.013322766159151636*y*pow(z,6)+-0.09045127554515031*pow(y,2)+0.005992765631767705*pow(y,2)*z+0.013423673528675684*pow(y,2)*pow(z,2)+-0.0023004573000961134*pow(y,2)*pow(z,3)+0.005168673053199138*pow(y,2)*pow(z,4)+0.001198597911839419*pow(y,2)*pow(z,5)+-0.0010741654292384106*pow(y,2)*pow(z,6)+23.426230286738804*x+-6.46622069424304*x*z+0.4981247986498274*x*pow(z,2)+3.8191260135605303*x*pow(z,3)+-6.512553774289694*x*pow(z,4)+-1.229001962808593*x*pow(z,5)+1.6092651634823152*x*pow(z,6)+-9.108425425070237*x*y+1.8188990981975768*x*y*z+-0.21360518020103803*x*y*pow(z,2)+-1.0605668872938288*x*y*pow(z,3)+2.44011933044516*x*y*pow(z,4)+0.38239238991828106*x*y*pow(z,5)+-0.604707670675042*x*y*pow(z,6)+0.7900987571011355*x*pow(y,2)+-0.1287019576968902*x*pow(y,2)*z+0.024197524605959142*x*pow(y,2)*pow(z,2)+0.07459979385969095*x*pow(y,2)*pow(z,3)+-0.2233688360495094*x*pow(y,2)*pow(z,4)+-0.030391335757068205*x*pow(y,2)*pow(z,5)+0.05545233362751212*x*pow(y,2)*pow(z,6)+-128.71223693320252*pow(x,2)+46.141244466789296*pow(x,2)*z+-3.535332804835174*pow(x,2)*pow(z,2)+-28.90635451072205*pow(x,2)*pow(z,3)+26.745272329337887*pow(x,2)*pow(z,4)+7.710577364316852*pow(x,2)*pow(z,5)+-6.985666428360249*pow(x,2)*pow(z,6)+45.89816806374216*pow(x,2)*y+-13.451006207325529*pow(x,2)*y*z+1.626593617168784*pow(x,2)*y*pow(z,2)+8.467667339060824*pow(x,2)*y*pow(z,3)+-10.458362955498835*pow(x,2)*y*pow(z,4)+-2.4377292376848705*pow(x,2)*y*pow(z,5)+2.7060605223235736*pow(x,2)*y*pow(z,6)+-3.8153327817863376*pow(x,2)*pow(y,2)+0.9855510467355035*pow(x,2)*pow(y,2)*z+-0.1851697384067723*pow(x,2)*pow(y,2)*pow(z,2)+-0.6272660158605703*pow(x,2)*pow(y,2)*pow(z,3)+0.9931378393152039*pow(x,2)*pow(y,2)*pow(z,4)+0.19577084519472532*pow(x,2)*pow(y,2)*pow(z,5)+-0.25476842501108*pow(x,2)*pow(y,2)*pow(z,6)+210.99237698004626*pow(x,3)+-88.2037861030198*pow(x,3)*z+-11.663727761501567*pow(x,3)*pow(z,2)+55.12613385310085*pow(x,3)*pow(z,3)+-20.917996936300263*pow(x,3)*pow(z,4)+-13.076586529293103*pow(x,3)*pow(z,5)+7.19951241576897*pow(x,3)*pow(z,6)+-70.72304457833293*pow(x,3)*y+26.071636209939815*pow(x,3)*y*z+3.1519075336051388*pow(x,3)*y*pow(z,2)+-16.371008623079316*pow(x,3)*y*pow(z,3)+9.297048571513661*pow(x,3)*y*pow(z,4)+4.137074087455883*pow(x,3)*y*pow(z,5)+-2.962398825070448*pow(x,3)*y*pow(z,6)+5.694372510115539*pow(x,3)*pow(y,2)+-1.934398509835003*pow(x,3)*pow(y,2)*z+-0.17231520587172167*pow(x,3)*pow(y,2)*pow(z,2)+1.226848901553737*pow(x,3)*pow(y,2)*pow(z,3)+-0.9698066971530204*pow(x,3)*pow(y,2)*pow(z,4)+-0.3318733680016539*pow(x,3)*pow(y,2)*pow(z,5)+0.2921102701753693*pow(x,3)*pow(y,2)*pow(z,6);
	
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
        ak4_code =      '''
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


        ROOT.gInterpreter.Declare(match_code)
        ROOT.gInterpreter.Declare(ak4_code)


        ROOT.gInterpreter.Declare(submass_code)
        ROOT.gInterpreter.Declare(ddt_code)
        ROOT.gInterpreter.Declare(region_code)
        ROOT.gInterpreter.Declare(index_code)
        ROOT.gInterpreter.Declare(cflow_code)
	ROOT.gInterpreter.Declare(JMC_code)
	
	percentage = 10
	fname = "DataD_UL_nano_3756_10"
	DataPro(files, fname, cut_hist, percentage)	
	
	

	print("All Data Finished")
