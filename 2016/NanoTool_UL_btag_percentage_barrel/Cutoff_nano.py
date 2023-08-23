import ROOT
RDF = ROOT.ROOT.RDataFrame
#ROOT.ROOT.EnableImplicitMT()
from ROOT import *
import sys,os

from Cutoff_Generator_nano import *

if __name__ == "__main__":
	print("Starting Run")
#	GJets = [["/cms/akobert/NanoToolOutput/2016/GJets/100to200/", str(16.81 * 9238000.0/10003194.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/100to200_APV/", str(16.81 * 9238000.0/9332192.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/200to400/", str(16.81 * 2305000.0/19881850.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/200to400_APV/", str(16.81 * 2305000.0/19122823.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/400to600/", str(16.81 * 274400.0/4629781.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/400to600_APV/", str(16.81 * 274400.0/4486234.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/600toInf/", str(16.81 * 93460.0/4358379.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/600toInf_APV/", str(16.81 * 93460.0/4661194.0)]]
	GJets = [["/cms/akobert/NanoToolOutput/2016/GJets/100to200/", str(16.81 * 9238000.0/10003194.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/200to400/", str(16.81 * 2305000.0/19881850.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/400to600/", str(16.81 * 274400.0/4629781.0)], ["/cms/akobert/NanoToolOutput/2016/GJets/600toInf/", str(16.81 * 93460.0/4358379.0)]]


	#Cutoff(GJets)	
	#Redone with finer binned pT and rho
	Cutoff(GJets)	

	print("Cutoffs Finished")
