import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Trigger_Processor_Data2_2017 import *

if __name__ == "__main__":
	print("Starting Run")

	files = [["/cms/akobert/NanoToolOutput/2017/GJets/100to200/", str(41.53 * 9238000.0/23341682.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2017/GJets/200to400/", str(41.53 * 2305000.0/55102371.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2017/GJets/400to600/", str(41.53 * 274400.0/11952145.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/2017/GJets/600toInf/", str(41.53 * 93460.0/11423214.0), 1, "GJ"]]


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
	fname = "Trigger_GJ_2017"
	DataPro(files, fname)	
	
	

	print("Trigger Study Finished")
