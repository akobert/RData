import ROOT
RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_nano import *

if __name__ == "__main__":
	print("Starting Run")
	GJets = [["/cms/akobert/NanoToolOutput/UL/GJets/100to200/", str(59.9 * 9238000.0/10412658.0)], ["/cms/akobert/NanoToolOutput/UL/GJets/200to400/", str(59.9 * 2305000.0/19755305.0)], ["/cms/akobert/NanoToolOutput/UL/GJets/400to600/", str(59.9 * 274400.0/4786197.0)], ["/cms/akobert/NanoToolOutput/UL/GJets/600toInf/", str(59.9 * 93460.0/4905665.0)]]


	Cutoff(GJets)	

	print("Cutoffs Finished")
