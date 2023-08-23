import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Trigger_Processor_Data2_2016 import *

if __name__ == "__main__":
	print("Starting Run")

	files = [["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunB_ver1/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunB_ver2/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunC/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunD/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunE/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunF/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunF_HIPM/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunG/", str(1.0), 1, "data"], ["/cms/akobert/NanoToolOutput/2016/SingleMuon/RunH/", str(1.0), 1, "data"]]


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
	fname = "Trigger_Data_2016"
	DataPro(files, fname)	
	
	

	print("Trigger Study Finished")
