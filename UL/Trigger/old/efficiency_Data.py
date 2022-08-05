import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Efficiency_Processor import *

if __name__ == "__main__":
	print("Starting Run")


	files = [["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018B", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018C", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SingleMuon/Run2018D", str(1.0)]]


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
	fname = "Efficiency_Data"
	DataPro(files, fname)	
	
	

	print("Trigger Study Finished")
