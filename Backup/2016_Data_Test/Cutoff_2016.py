import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_2016 import *

if __name__ == "__main__":
	print("Starting Run")
	Data = [["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016B", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016C", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016D", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016E", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016F", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016G", str(1.0)], ["/cms/vlq/NANOAOD/APR20/SinglePhoton/Run2016H", str(1.0)]]


	Cutoff(Data)	

	print("Cutoffs 2016 Finished")
