import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Sample_Processor_Percentage import *

if __name__ == "__main__":
	print("Starting Run")

	files = [["/cms/akobert/NanoToolOutput/M75/", str(59.9 * 2960.0/505803.0)]]

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
        region_code = "float a=100; float b=300; float c=70; float d=85;"


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


				float corr = -0.6048677660398856+0.5355922541378053*z+5.268909497443718*pow(z,2)+-0.6187765160755296*pow(z,3)+-4.15207021063141*pow(z,4)+0.6639490563920432*y+-0.16483771307745748*y*z+-1.5962272119715673*y*pow(z,2)+0.18040270928228289*y*pow(z,3)+1.2416818231829208*y*pow(z,4)+-0.06155471797648299*pow(y,2)+0.0125822672993261*pow(y,2)*z+0.11997513128878046*pow(y,2)*pow(z,2)+-0.013029849833100876*pow(y,2)*pow(z,3)+-0.0925056091216234*pow(y,2)*pow(z,4)+-2.042367417701553*x+-8.31020557562959*x*z+-72.50762484693495*x*pow(z,2)+8.908110321256935*x*pow(z,3)+61.21399186987669*x*pow(z,4)+-1.2190939965324412*x*y+2.543408105523368*x*y*z+21.839145633082783*x*y*pow(z,2)+-2.541967663778362*x*y*pow(z,3)+-18.27931261466682*x*y*pow(z,4)+0.18715640859370797*x*pow(y,2)+-0.19334327122455935*x*pow(y,2)*z+-1.6368001128383347*x*pow(y,2)*pow(z,2)+0.1792806521558062*x*pow(y,2)*pow(z,3)+1.359029408648763*x*pow(y,2)*pow(z,4)+11.7257192989607*pow(x,2)+57.63989504007768*pow(x,2)*z+325.192356383677*pow(x,2)*pow(z,2)+-54.68697711324447*pow(x,2)*pow(z,3)+-283.82951090564393*pow(x,2)*pow(z,4)+2.1128195206998157*pow(x,2)*y+-17.563027900077067*pow(x,2)*y*z+-97.62637196252874*pow(x,2)*y*pow(z,2)+15.670767154041112*pow(x,2)*y*pow(z,3)+84.72788056194872*pow(x,2)*y*pow(z,4)+-0.44838172858622016*pow(x,2)*pow(y,2)+1.3296451153998419*pow(x,2)*pow(y,2)*z+7.303449188649125*pow(x,2)*pow(y,2)*pow(z,2)+-1.1101941908502866*pow(x,2)*pow(y,2)*pow(z,3)+-6.305576124558815*pow(x,2)*pow(y,2)*pow(z,4)+-14.065248365505866*pow(x,3)+-106.91224121948734*pow(x,3)*z+-468.9397211161268*pow(x,3)*pow(z,2)+92.89110460645637*pow(x,3)*pow(z,3)+419.6032153240844*pow(x,3)*pow(z,4)+-0.18130915890638732*pow(x,3)*y+32.32398220208975*pow(x,3)*y*z+140.39801172224867*pow(x,3)*y*pow(z,2)+-26.46066417535781*pow(x,3)*y*pow(z,3)+-125.22593341286296*pow(x,3)*y*pow(z,4)+0.23212169153287832*pow(x,3)*pow(y,2)+-2.430302082589968*pow(x,3)*pow(y,2)*z+-10.485014799112239*pow(x,3)*pow(y,2)*pow(z,2)+1.8632246341649994*pow(x,3)*pow(y,2)*pow(z,3)+9.325269634264934*pow(x,3)*pow(y,2)*pow(z,4);
                                return corr;
                        }
                        '''

        ROOT.gInterpreter.Declare(JMC_code)

        ROOT.gInterpreter.Declare(submass_code)
        ROOT.gInterpreter.Declare(includes)
        ROOT.gInterpreter.Declare(ddt_code)
        ROOT.gInterpreter.Declare(region_code)
        ROOT.gInterpreter.Declare(index_code)
        ROOT.gInterpreter.Declare(dr_code)
        ROOT.gInterpreter.Declare(cflow_code)

	
	percentage = 20
	fname = "75GeV_20_nano_corr"
	SamplePro(files, fname, cut_hist, percentage, 100, 300, 70, 85)	
	
	

	print("75 GeV Finished")
