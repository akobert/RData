import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Trigger_Processor_Data2_2016 import *

if __name__ == "__main__":
	print("Starting Run")

	files = [["/cms/akobert/NanoToolOutput/2016/GJets/100to200/", str(36.47 * 9238000.0/10003194.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/100to200_APV/", str(36.47 * 9238000.0/9332192.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/200to400/", str(36.47 * 2305000.0/19881850.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/200to400_APV/", str(36.47 * 2305000.0/19122823.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/400to600/", str(36.47 * 274400.0/4629781.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/400to600_APV/", str(36.47 * 274400.0/4486234.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/600toInf/", str(36.47 * 93460.0/4358379.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2016/GJets/600toInf_APV/", str(36.47 * 93460.0/4661194.0), 1, "GJ"]]


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


        ROOT.gInterpreter.Declare(includes)
	fname = "Trigger_GJ_2016"
	DataPro(files, fname)	
	
	

	print("Trigger Study Finished")
