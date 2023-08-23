import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_nano import *

if __name__ == "__main__":
	print("Starting Run")
	GJets = [["/cms/akobert/NanoToolOutput/2017/GJets/100to200/", str(41.48 * 9238000.0/23341682.0)], ["/cms/akobert/NanoToolOutput/2017/GJets/200to400/", str(41.48 * 2305000.0/55102371.0)], ["/cms/akobert/NanoToolOutput/2017/GJets/400to600/", str(41.48 * 274400.0/11952145.0)], ["/cms/akobert/NanoToolOutput/2017/GJets/600toInf/", str(41.48 * 93460.0/11423214.0)]]


	#Cutoff(GJets)	
	#Redone with finer binned pT and rho
	Cutoff(GJets)	

	print("Cutoffs Finished")
