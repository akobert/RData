import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_2016 import *

if __name__ == "__main__":
	print("Starting Run")
	GJets = [["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_100to200", str(59.9*9238000.0/10125438.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_200to400", str(59.9*2305000.0/19258533.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_400to600", str(59.9*274400.0/4795233.0)], ["/cms/xaastorage/NanoAOD/2018/JUNE19/GJetsHTBinned/GJetsHT_600toInf", str(59.9*93460.0/5044493.0)]]


	Cutoff(GJets)	

	print("Cutoffs 2016 Finished")
