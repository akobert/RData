import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Trigger_Processor_Data2 import *

if __name__ == "__main__":
	print("Starting Run")

#	files = [["/cms/xaastorage/NanoAOD/2018/JUNE19/EGamma_RunA_Test/branch_present", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/EGamma_RunA_Test/branch_missing", str(1.0), 2], ["/cms/xaastorage/NanoAOD/2018/JUNE19/EGamma_RunB_Test/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/EGamma_RunC_Test/", str(1.0), 1], ["/cms/xaastorage/NanoAOD/2018/JUNE19/EGamma_RunD_Test/", str(1.0), 1]]

	#files = [["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunB/", str(1.0), 1]]
	#files = [["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018A", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018B", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018C", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018D", str(1.0)]]
	files = [["/cms/akobert/NanoToolOutput/UL/GJets/100to200/", str(59.9 * 9238000.0/31722998.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/UL/GJets/200to400/", str(59.9 * 2305000.0/62560811.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/UL/GJets/400to600/", str(59.9 * 274400.0/16898927.0), 1, "GJ"], ["/cms/akobert/NanoToolOutput/UL/GJets/600toInf/", str(59.9 * 93460.0/16678401.0), 1, "GJ"]]


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
	fname = "Trigger_GJ"
	DataPro(files, fname)	
	
	

	print("Trigger Study Finished")