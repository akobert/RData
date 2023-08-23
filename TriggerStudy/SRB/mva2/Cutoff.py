import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator import *

if __name__ == "__main__":
	print("Starting Run")
	GJets = [["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/100to200/", str(59.9 * 8644000.0/10412658.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/200to400/", str(59.9 * 2183000.0/19755305)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/400to600/", str(59.9 * 260200.0/4786197)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/UL/GJetsHTBinned/600toInf/", str(59.9 * 86589.0/4905665)]]


	Cutoff(GJets)	

	print("Cutoffs Finished")
