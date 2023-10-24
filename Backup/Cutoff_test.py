import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_test import *

if __name__ == "__main__":
	print("Starting Run")
	GJets = [["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_100to200", str(59.9 * 8640000.0/9798176.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_200to400", str(59.9 * 2185000.0/19062809.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_400to600", str(59.9 * 259900.0/4655985.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_600toInf", str(59.9 * 85310.0/4981121.0)]]


	Cutoff(GJets)	

	print("Cutoffs Finished")
