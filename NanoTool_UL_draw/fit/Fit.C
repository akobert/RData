#include <math.h>
#include <string.h>
Double_t FitLimLow = 10;
Double_t FitLimHigh = 35;

Double_t DefPar0 = 250;
Double_t DefPar1 = 8;
Double_t DefPar2 = 25;

Double_t fitf(double *x, double *par)
{
	Double_t fitval = par[0]*TMath::Exp(-pow((x[0]-par[2]), 2)/(2*pow(par[1], 2)));
	
	return fitval;	
}

int FitFunc(char* ifile, char* out_png, Double_t mass, char* title, Double_t low, Double_t high, char* var)
{
	FitLimLow = low;
	FitLimHigh = high;
	
	DefPar2 = (high - low)/2;

	gROOT->SetStyle("Plain");
	gStyle->SetOptFit(111111);
	
	TFile *f = new TFile(ifile);
	TCanvas *c1 = new TCanvas("c1", "the fit canvas", 1000, 800);
	c1->cd();
	
	//create combined histogram
	TH1F *hpx = (TH1F*)f->Get(var);
	hpx->SetTitle(title);
	DefPar0 = hpx->GetMaximum();
	DefPar2 = mass;
	
	//Creates a Root function based on function fitf above
	TF1 *func = new TF1("function4", fitf,FitLimLow, FitLimHigh, 3);
	
	func->SetParameters(DefPar0, DefPar1, DefPar2);
	func->SetParNames("GaussAmp", "GaussSigma", "GaussMean");
	
	func->SetParLimits(0, 0, 1000);
	func->SetParLimits(1, 1, 50);
	func->SetParLimits(2, FitLimLow, FitLimHigh);

	//Fit Histogram in Range
	hpx->SetLineColor(1);
	hpx->Fit(func, "r");
	hpx->Draw("samehiste");	

        c1->SaveAs(out_png);
	
//	TFile* file2 = new TFile(out_root, "UPDATE");
//	file2->cd();
//	func->Write();
//	file2->Close();
	return 0;
}


void Fit(){
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M10_UL_nano_merged.root", "../plots/10GeV_pass_soft_fit.png", 10, "10 GeV JEC", 5, 15, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M10_UL_nano_merged.root", "../plots/10GeV_pass_soft_fit_corr.png", 10, "10 GeV JEC and JMC", 5, 15, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M20_UL_nano_merged.root", "../plots/20GeV_pass_soft_fit.png", 20, "20 GeV JEC", 10, 30, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M20_UL_nano_merged.root", "../plots/20GeV_pass_soft_fit_corr.png", 20, "20 GeV JEC and JMC", 10, 30, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M25_UL_nano_merged.root", "../plots/25GeV_pass_soft_fit.png", 25, "25 GeV JEC", 15, 35, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M25_UL_nano_merged.root", "../plots/25GeV_pass_soft_fit_corr.png", 25, "25 GeV JEC and JMC", 15, 35, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M50_UL_nano_merged.root", "../plots/50GeV_pass_soft_fit.png", 50, "50 GeV JEC", 35, 65, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M50_UL_nano_merged.root", "../plots/50GeV_pass_soft_fit_corr.png", 50, "50 GeV JEC and JMC", 35, 65, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/WGamma_UL_nano_merged.root", "../plots/WGamma_pass_soft_fit.png", 80, "W+Gamma JEC", 65, 105, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/WGamma_UL_nano_merged.root", "../plots/WGamma_pass_soft_fit_corr.png", 80, "W+Gamma JEC and JMC", 65, 105, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/ZGamma_UL_nano_merged.root", "../plots/ZGamma_pass_soft_fit.png", 91, "Z+Gamma JEC", 70, 120, "pass_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/ZGamma_UL_nano_merged.root", "../plots/ZGamma_pass_soft_fit_corr.png", 91, "Z+Gamma JEC and JMC", 70, 120, "pass_soft_thin");


	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M10_UL_nano_merged.root", "../plots/10GeV_fail_soft_fit.png", 10, "10 GeV JEC", 5, 15, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M10_UL_nano_merged.root", "../plots/10GeV_fail_soft_fit_corr.png", 10, "10 GeV JEC and JMC", 5, 15, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M20_UL_nano_merged.root", "../plots/20GeV_fail_soft_fit.png", 20, "20 GeV JEC", 10, 30, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M20_UL_nano_merged.root", "../plots/20GeV_fail_soft_fit_corr.png", 20, "20 GeV JEC and JMC", 10, 30, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M25_UL_nano_merged.root", "../plots/25GeV_fail_soft_fit.png", 25, "25 GeV JEC", 15, 35, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M25_UL_nano_merged.root", "../plots/25GeV_fail_soft_fit_corr.png", 25, "25 GeV JEC and JMC", 15, 35, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M50_UL_nano_merged.root", "../plots/50GeV_fail_soft_fit.png", 50, "50 GeV JEC", 35, 65, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/M50_UL_nano_merged.root", "../plots/50GeV_fail_soft_fit_corr.png", 50, "50 GeV JEC and JMC", 35, 65, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/WGamma_UL_nano_merged.root", "../plots/WGamma_fail_soft_fit.png", 80, "W+Gamma JEC", 65, 105, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/WGamma_UL_nano_merged.root", "../plots/WGamma_fail_soft_fit_corr.png", 80, "W+Gamma JEC and JMC", 65, 105, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/ZGamma_UL_nano_merged.root", "../plots/ZGamma_fail_soft_fit.png", 91, "Z+Gamma JEC", 70, 120, "fail_soft_thin");
	FitFunc("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr/ZGamma_UL_nano_merged.root", "../plots/ZGamma_fail_soft_fit_corr.png", 91, "Z+Gamma JEC and JMC", 70, 120, "fail_soft_thin");


	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_1.png", 10, "Passing 10 GeV JEC 120-130", 5, 15, "base_pass_1");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_1.png", 10, "Passing 10 GeV JEC and JMC 120-130", 5, 15, "corr_pass_1");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_1.png", 10, "Failing 10 GeV JEC 120-130", 5, 15, "base_fail_1");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_1.png", 10, "Failing 10 GeV JEC and JMC 120-130", 5, 15, "corr_fail_1");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_2.png", 10, "Passing 10 GeV JEC 130-145", 5, 15, "base_pass_2");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_2.png", 10, "Passing 10 GeV JEC and JMC 130-145", 5, 15, "corr_pass_2");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_2.png", 10, "Failing 10 GeV JEC 130-145", 5, 15, "base_fail_2");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_2.png", 10, "Failing 10 GeV JEC and JMC 130-145", 5, 15, "corr_fail_2");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_3.png", 10, "Passing 10 GeV JEC 145-160", 5, 15, "base_pass_3");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_3.png", 10, "Passing 10 GeV JEC and JMC 145-160", 5, 15, "corr_pass_3");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_3.png", 10, "Failing 10 GeV JEC 145-160", 5, 15, "base_fail_3");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_3.png", 10, "Failing 10 GeV JEC and JMC 145-160", 5, 15, "corr_fail_3");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_4.png", 10, "Passing 10 GeV JEC 160-180", 5, 15, "base_pass_4");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_4.png", 10, "Passing 10 GeV JEC and JMC 160-180", 5, 15, "corr_pass_4");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_4.png", 10, "Failing 10 GeV JEC 160-180", 5, 15, "base_fail_4");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_4.png", 10, "Failing 10 GeV JEC and JMC 160-180", 5, 15, "corr_fail_4");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_5.png", 10, "Passing 10 GeV JEC 180-200", 5, 15, "base_pass_5");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_5.png", 10, "Passing 10 GeV JEC and JMC 180-200", 5, 15, "corr_pass_5");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_5.png", 10, "Failing 10 GeV JEC 180-200", 5, 15, "base_fail_5");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_5.png", 10, "Failing 10 GeV JEC and JMC 180-200", 5, 15, "corr_fail_5");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_6.png", 10, "Passing 10 GeV JEC 200-250", 5, 15, "base_pass_6");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_6.png", 10, "Passing 10 GeV JEC and JMC 200-250", 5, 15, "corr_pass_6");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_6.png", 10, "Failing 10 GeV JEC 200-250", 5, 15, "base_fail_6");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_6.png", 10, "Failing 10 GeV JEC and JMC 200-250", 5, 15, "corr_fail_6");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_7.png", 10, "Passing 10 GeV JEC 250-300", 5, 15, "base_pass_7");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_7.png", 10, "Passing 10 GeV JEC and JMC 250-300", 5, 15, "corr_pass_7");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_7.png", 10, "Failing 10 GeV JEC 250-300", 5, 15, "base_fail_7");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_7.png", 10, "Failing 10 GeV JEC and JMC 250-300", 5, 15, "corr_fail_7");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_8.png", 10, "Passing 10 GeV JEC 300-400", 5, 15, "base_pass_8");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_8.png", 10, "Passing 10 GeV JEC and JMC 300-400", 5, 15, "corr_pass_8");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_8.png", 10, "Failing 10 GeV JEC 300-400", 5, 15, "base_fail_8");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_8.png", 10, "Failing 10 GeV JEC and JMC 300-400", 5, 15, "corr_fail_8");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_base_9.png", 10, "Passing 10 GeV JEC 400-500", 5, 15, "base_pass_9");
	FitFunc("../M10_plots.root", "../plots/10GeV_pass_corr_9.png", 10, "Passing 10 GeV JEC and JMC 400-500", 5, 15, "corr_pass_9");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_base_9.png", 10, "Failing 10 GeV JEC 400-500", 5, 15, "base_fail_9");
	FitFunc("../M10_plots.root", "../plots/10GeV_fail_corr_9.png", 10, "Failing 10 GeV JEC and JMC 400-500", 5, 15, "corr_fail_9");

	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_1.png", 20, "Passing 20 GeV JEC 120-130", 10, 30, "base_pass_1");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_1.png", 20, "Passing 20 GeV JEC and JMC 120-130", 10, 30, "corr_pass_1");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_1.png", 20, "Failing 20 GeV JEC 120-130", 10, 30, "base_fail_1");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_1.png", 20, "Failing 20 GeV JEC and JMC 120-130", 10, 30, "corr_fail_1");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_2.png", 20, "Passing 20 GeV JEC 130-145", 10, 30, "base_pass_2");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_2.png", 20, "Passing 20 GeV JEC and JMC 130-145", 10, 30, "corr_pass_2");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_2.png", 20, "Failing 20 GeV JEC 130-145", 10, 30, "base_fail_2");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_2.png", 20, "Failing 20 GeV JEC and JMC 130-145", 10, 30, "corr_fail_2");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_3.png", 20, "Passing 20 GeV JEC 145-160", 10, 30, "base_pass_3");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_3.png", 20, "Passing 20 GeV JEC and JMC 145-160", 10, 30, "corr_pass_3");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_3.png", 20, "Failing 20 GeV JEC 145-160", 10, 30, "base_fail_3");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_3.png", 20, "Failing 20 GeV JEC and JMC 145-160", 10, 30, "corr_fail_3");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_4.png", 20, "Passing 20 GeV JEC 160-180", 10, 30, "base_pass_4");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_4.png", 20, "Passing 20 GeV JEC and JMC 160-180", 10, 30, "corr_pass_4");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_4.png", 20, "Failing 20 GeV JEC 160-180", 10, 30, "base_fail_4");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_4.png", 20, "Failing 20 GeV JEC and JMC 160-180", 10, 30, "corr_fail_4");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_5.png", 20, "Passing 20 GeV JEC 180-200", 10, 30, "base_pass_5");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_5.png", 20, "Passing 20 GeV JEC and JMC 180-200", 10, 30, "corr_pass_5");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_5.png", 20, "Failing 20 GeV JEC 180-200", 10, 30, "base_fail_5");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_5.png", 20, "Failing 20 GeV JEC and JMC 180-200", 10, 30, "corr_fail_5");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_6.png", 20, "Passing 20 GeV JEC 200-250", 10, 30, "base_pass_6");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_6.png", 20, "Passing 20 GeV JEC and JMC 200-250", 10, 30, "corr_pass_6");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_6.png", 20, "Failing 20 GeV JEC 200-250", 10, 30, "base_fail_6");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_6.png", 20, "Failing 20 GeV JEC and JMC 200-250", 10, 30, "corr_fail_6");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_7.png", 20, "Passing 20 GeV JEC 250-300", 10, 30, "base_pass_7");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_7.png", 20, "Passing 20 GeV JEC and JMC 250-300", 10, 30, "corr_pass_7");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_7.png", 20, "Failing 20 GeV JEC 250-300", 10, 30, "base_fail_7");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_7.png", 20, "Failing 20 GeV JEC and JMC 250-300", 10, 30, "corr_fail_7");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_8.png", 20, "Passing 20 GeV JEC 300-400", 10, 30, "base_pass_8");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_8.png", 20, "Passing 20 GeV JEC and JMC 300-400", 10, 30, "corr_pass_8");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_8.png", 20, "Failing 20 GeV JEC 300-400", 10, 30, "base_fail_8");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_8.png", 20, "Failing 20 GeV JEC and JMC 300-400", 10, 30, "corr_fail_8");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_base_9.png", 20, "Passing 20 GeV JEC 400-500", 10, 30, "base_pass_9");
	FitFunc("../M20_plots.root", "../plots/20GeV_pass_corr_9.png", 20, "Passing 20 GeV JEC and JMC 400-500", 10, 30, "corr_pass_9");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_base_9.png", 20, "Failing 20 GeV JEC 400-500", 10, 30, "base_fail_9");
	FitFunc("../M20_plots.root", "../plots/20GeV_fail_corr_9.png", 20, "Failing 20 GeV JEC and JMC 400-500", 10, 30, "corr_fail_9");

	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_1.png", 25, "Passing 25 GeV JEC 120-130", 15, 35, "base_pass_1");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_1.png", 25, "Passing 25 GeV JEC and JMC 120-130", 15, 35, "corr_pass_1");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_1.png", 25, "Failing 25 GeV JEC 120-130", 15, 35, "base_fail_1");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_1.png", 25, "Failing 25 GeV JEC and JMC 120-130", 15, 35, "corr_fail_1");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_2.png", 25, "Passing 25 GeV JEC 130-145", 15, 35, "base_pass_2");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_2.png", 25, "Passing 25 GeV JEC and JMC 130-145", 15, 35, "corr_pass_2");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_2.png", 25, "Failing 25 GeV JEC 130-145", 15, 35, "base_fail_2");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_2.png", 25, "Failing 25 GeV JEC and JMC 130-145", 15, 35, "corr_fail_2");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_3.png", 25, "Passing 25 GeV JEC 145-160", 15, 35, "base_pass_3");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_3.png", 25, "Passing 25 GeV JEC and JMC 145-160", 15, 35, "corr_pass_3");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_3.png", 25, "Failing 25 GeV JEC 145-160", 15, 35, "base_fail_3");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_3.png", 25, "Failing 25 GeV JEC and JMC 145-160", 15, 35, "corr_fail_3");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_4.png", 25, "Passing 25 GeV JEC 160-180", 15, 35, "base_pass_4");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_4.png", 25, "Passing 25 GeV JEC and JMC 160-180", 15, 35, "corr_pass_4");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_4.png", 25, "Failing 25 GeV JEC 160-180", 15, 35, "base_fail_4");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_4.png", 25, "Failing 25 GeV JEC and JMC 160-180", 15, 35, "corr_fail_4");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_5.png", 25, "Passing 25 GeV JEC 180-200", 15, 35, "base_pass_5");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_5.png", 25, "Passing 25 GeV JEC and JMC 180-200", 15, 35, "corr_pass_5");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_5.png", 25, "Failing 25 GeV JEC 180-200", 15, 35, "base_fail_5");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_5.png", 25, "Failing 25 GeV JEC and JMC 180-200", 15, 35, "corr_fail_5");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_6.png", 25, "Passing 25 GeV JEC 200-250", 15, 35, "base_pass_6");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_6.png", 25, "Passing 25 GeV JEC and JMC 200-250", 15, 35, "corr_pass_6");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_6.png", 25, "Failing 25 GeV JEC 200-250", 15, 35, "base_fail_6");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_6.png", 25, "Failing 25 GeV JEC and JMC 200-250", 15, 35, "corr_fail_6");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_7.png", 25, "Passing 25 GeV JEC 250-300", 15, 35, "base_pass_7");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_7.png", 25, "Passing 25 GeV JEC and JMC 250-300", 15, 35, "corr_pass_7");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_7.png", 25, "Failing 25 GeV JEC 250-300", 15, 35, "base_fail_7");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_7.png", 25, "Failing 25 GeV JEC and JMC 250-300", 15, 35, "corr_fail_7");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_8.png", 25, "Passing 25 GeV JEC 300-400", 15, 35, "base_pass_8");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_8.png", 25, "Passing 25 GeV JEC and JMC 300-400", 15, 35, "corr_pass_8");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_8.png", 25, "Failing 25 GeV JEC 300-400", 15, 35, "base_fail_8");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_8.png", 25, "Failing 25 GeV JEC and JMC 300-400", 15, 35, "corr_fail_8");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_base_9.png", 25, "Passing 25 GeV JEC 400-500", 15, 35, "base_pass_9");
	FitFunc("../M25_plots.root", "../plots/25GeV_pass_corr_9.png", 25, "Passing 25 GeV JEC and JMC 400-500", 15, 35, "corr_pass_9");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_base_9.png", 25, "Failing 25 GeV JEC 400-500", 15, 35, "base_fail_9");
	FitFunc("../M25_plots.root", "../plots/25GeV_fail_corr_9.png", 25, "Failing 25 GeV JEC and JMC 400-500", 15, 35, "corr_fail_9");

	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_1.png", 50, "Passing 50 GeV JEC 120-130", 35, 65, "base_pass_1");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_1.png", 50, "Passing 50 GeV JEC and JMC 120-130", 35, 65, "corr_pass_1");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_1.png", 50, "Failing 50 GeV JEC 120-130", 35, 65, "base_fail_1");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_1.png", 50, "Failing 50 GeV JEC and JMC 120-130", 35, 65, "corr_fail_1");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_2.png", 50, "Passing 50 GeV JEC 130-145", 35, 65, "base_pass_2");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_2.png", 50, "Passing 50 GeV JEC and JMC 130-145", 35, 65, "corr_pass_2");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_2.png", 50, "Failing 50 GeV JEC 130-145", 35, 65, "base_fail_2");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_2.png", 50, "Failing 50 GeV JEC and JMC 130-145", 35, 65, "corr_fail_2");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_3.png", 50, "Passing 50 GeV JEC 145-160", 35, 65, "base_pass_3");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_3.png", 50, "Passing 50 GeV JEC and JMC 145-160", 35, 65, "corr_pass_3");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_3.png", 50, "Failing 50 GeV JEC 145-160", 35, 65, "base_fail_3");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_3.png", 50, "Failing 50 GeV JEC and JMC 145-160", 35, 65, "corr_fail_3");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_4.png", 50, "Passing 50 GeV JEC 160-180", 35, 65, "base_pass_4");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_4.png", 50, "Passing 50 GeV JEC and JMC 160-180", 35, 65, "corr_pass_4");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_4.png", 50, "Failing 50 GeV JEC 160-180", 35, 65, "base_fail_4");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_4.png", 50, "Failing 50 GeV JEC and JMC 160-180", 35, 65, "corr_fail_4");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_5.png", 50, "Passing 50 GeV JEC 180-200", 35, 65, "base_pass_5");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_5.png", 50, "Passing 50 GeV JEC and JMC 180-200", 35, 65, "corr_pass_5");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_5.png", 50, "Failing 50 GeV JEC 180-200", 35, 65, "base_fail_5");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_5.png", 50, "Failing 50 GeV JEC and JMC 180-200", 35, 65, "corr_fail_5");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_6.png", 50, "Passing 50 GeV JEC 200-250", 35, 65, "base_pass_6");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_6.png", 50, "Passing 50 GeV JEC and JMC 200-250", 35, 65, "corr_pass_6");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_6.png", 50, "Failing 50 GeV JEC 200-250", 35, 65, "base_fail_6");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_6.png", 50, "Failing 50 GeV JEC and JMC 200-250", 35, 65, "corr_fail_6");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_7.png", 50, "Passing 50 GeV JEC 250-300", 35, 65, "base_pass_7");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_7.png", 50, "Passing 50 GeV JEC and JMC 250-300", 35, 65, "corr_pass_7");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_7.png", 50, "Failing 50 GeV JEC 250-300", 35, 65, "base_fail_7");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_7.png", 50, "Failing 50 GeV JEC and JMC 250-300", 35, 65, "corr_fail_7");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_8.png", 50, "Passing 50 GeV JEC 300-400", 35, 65, "base_pass_8");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_8.png", 50, "Passing 50 GeV JEC and JMC 300-400", 35, 65, "corr_pass_8");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_8.png", 50, "Failing 50 GeV JEC 300-400", 35, 65, "base_fail_8");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_8.png", 50, "Failing 50 GeV JEC and JMC 300-400", 35, 65, "corr_fail_8");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_base_9.png", 50, "Passing 50 GeV JEC 400-500", 35, 65, "base_pass_9");
	FitFunc("../M50_plots.root", "../plots/50GeV_pass_corr_9.png", 50, "Passing 50 GeV JEC and JMC 400-500", 35, 65, "corr_pass_9");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_base_9.png", 50, "Failing 50 GeV JEC 400-500", 35, 65, "base_fail_9");
	FitFunc("../M50_plots.root", "../plots/50GeV_fail_corr_9.png", 50, "Failing 50 GeV JEC and JMC 400-500", 35, 65, "corr_fail_9");

	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_1.png", 80, "Passing W+Gamma JEC 120-130", 65, 105, "base_pass_1");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_1.png", 80, "Passing W+Gamma JEC and JMC 120-130", 65, 105, "corr_pass_1");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_1.png", 80, "Failing W+Gamma JEC 120-130", 65, 105, "base_fail_1");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_1.png", 80, "Failing W+Gamma JEC and JMC 120-130", 65, 105, "corr_fail_1");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_2.png", 80, "Passing W+Gamma JEC 130-145", 65, 105, "base_pass_2");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_2.png", 80, "Passing W+Gamma JEC and JMC 130-145", 65, 105, "corr_pass_2");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_2.png", 80, "Failing W+Gamma JEC 130-145", 65, 105, "base_fail_2");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_2.png", 80, "Failing W+Gamma JEC and JMC 130-145", 65, 105, "corr_fail_2");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_3.png", 80, "Passing W+Gamma JEC 145-160", 65, 105, "base_pass_3");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_3.png", 80, "Passing W+Gamma JEC and JMC 145-160", 65, 105, "corr_pass_3");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_3.png", 80, "Failing W+Gamma JEC 145-160", 65, 105, "base_fail_3");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_3.png", 80, "Failing W+Gamma JEC and JMC 145-160", 65, 105, "corr_fail_3");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_4.png", 80, "Passing W+Gamma JEC 160-180", 65, 105, "base_pass_4");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_4.png", 80, "Passing W+Gamma JEC and JMC 160-180", 65, 105, "corr_pass_4");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_4.png", 80, "Failing W+Gamma JEC 160-180", 65, 105, "base_fail_4");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_4.png", 80, "Failing W+Gamma JEC and JMC 160-180", 65, 105, "corr_fail_4");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_5.png", 80, "Passing W+Gamma JEC 180-200", 65, 105, "base_pass_5");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_5.png", 80, "Passing W+Gamma JEC and JMC 180-200", 65, 105, "corr_pass_5");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_5.png", 80, "Failing W+Gamma JEC 180-200", 65, 105, "base_fail_5");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_5.png", 80, "Failing W+Gamma JEC and JMC 180-200", 65, 105, "corr_fail_5");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_6.png", 80, "Passing W+Gamma JEC 200-250", 65, 105, "base_pass_6");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_6.png", 80, "Passing W+Gamma JEC and JMC 200-250", 65, 105, "corr_pass_6");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_6.png", 80, "Failing W+Gamma JEC 200-250", 65, 105, "base_fail_6");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_6.png", 80, "Failing W+Gamma JEC and JMC 200-250", 65, 105, "corr_fail_6");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_7.png", 80, "Passing W+Gamma JEC 250-300", 65, 105, "base_pass_7");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_7.png", 80, "Passing W+Gamma JEC and JMC 250-300", 65, 105, "corr_pass_7");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_7.png", 80, "Failing W+Gamma JEC 250-300", 65, 105, "base_fail_7");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_7.png", 80, "Failing W+Gamma JEC and JMC 250-300", 65, 105, "corr_fail_7");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_8.png", 80, "Passing W+Gamma JEC 300-400", 65, 105, "base_pass_8");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_8.png", 80, "Passing W+Gamma JEC and JMC 300-400", 65, 105, "corr_pass_8");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_8.png", 80, "Failing W+Gamma JEC 300-400", 65, 105, "base_fail_8");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_8.png", 80, "Failing W+Gamma JEC and JMC 300-400", 65, 105, "corr_fail_8");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_base_9.png", 80, "Passing W+Gamma JEC 400-500", 65, 105, "base_pass_9");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_pass_corr_9.png", 80, "Passing W+Gamma JEC and JMC 400-500", 65, 105, "corr_pass_9");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_base_9.png", 80, "Failing W+Gamma JEC 400-500", 65, 105, "base_fail_9");
	FitFunc("../WGamma_plots.root", "../plots/WGamma_fail_corr_9.png", 80, "Failing W+Gamma JEC and JMC 400-500", 65, 105, "corr_fail_9");

	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_1.png", 91, "Passing Z+Gamma JEC 120-130", 70, 120, "base_pass_1");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_1.png", 91, "Passing Z+Gamma JEC and JMC 120-130", 70, 120, "corr_pass_1");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_1.png", 91, "Failing Z+Gamma JEC 120-130", 70, 120, "base_fail_1");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_1.png", 91, "Failing Z+Gamma JEC and JMC 120-130", 70, 120, "corr_fail_1");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_2.png", 91, "Passing Z+Gamma JEC 130-145", 70, 120, "base_pass_2");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_2.png", 91, "Passing Z+Gamma JEC and JMC 130-145", 70, 120, "corr_pass_2");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_2.png", 91, "Failing Z+Gamma JEC 130-145", 70, 120, "base_fail_2");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_2.png", 91, "Failing Z+Gamma JEC and JMC 130-145", 70, 120, "corr_fail_2");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_3.png", 91, "Passing Z+Gamma JEC 145-160", 70, 120, "base_pass_3");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_3.png", 91, "Passing Z+Gamma JEC and JMC 145-160", 70, 120, "corr_pass_3");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_3.png", 91, "Failing Z+Gamma JEC 145-160", 70, 120, "base_fail_3");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_3.png", 91, "Failing Z+Gamma JEC and JMC 145-160", 70, 120, "corr_fail_3");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_4.png", 91, "Passing Z+Gamma JEC 160-180", 70, 120, "base_pass_4");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_4.png", 91, "Passing Z+Gamma JEC and JMC 160-180", 70, 120, "corr_pass_4");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_4.png", 91, "Failing Z+Gamma JEC 160-180", 70, 120, "base_fail_4");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_4.png", 91, "Failing Z+Gamma JEC and JMC 160-180", 70, 120, "corr_fail_4");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_5.png", 91, "Passing Z+Gamma JEC 180-200", 70, 120, "base_pass_5");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_5.png", 91, "Passing Z+Gamma JEC and JMC 180-200", 70, 120, "corr_pass_5");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_5.png", 91, "Failing Z+Gamma JEC 180-200", 70, 120, "base_fail_5");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_5.png", 91, "Failing Z+Gamma JEC and JMC 180-200", 70, 120, "corr_fail_5");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_6.png", 91, "Passing Z+Gamma JEC 200-250", 70, 120, "base_pass_6");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_6.png", 91, "Passing Z+Gamma JEC and JMC 200-250", 70, 120, "corr_pass_6");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_6.png", 91, "Failing Z+Gamma JEC 200-250", 70, 120, "base_fail_6");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_6.png", 91, "Failing Z+Gamma JEC and JMC 200-250", 70, 120, "corr_fail_6");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_7.png", 91, "Passing Z+Gamma JEC 250-300", 70, 120, "base_pass_7");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_7.png", 91, "Passing Z+Gamma JEC and JMC 250-300", 70, 120, "corr_pass_7");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_7.png", 91, "Failing Z+Gamma JEC 250-300", 70, 120, "base_fail_7");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_7.png", 91, "Failing Z+Gamma JEC and JMC 250-300", 70, 120, "corr_fail_7");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_8.png", 91, "Passing Z+Gamma JEC 300-400", 70, 120, "base_pass_8");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_8.png", 91, "Passing Z+Gamma JEC and JMC 300-400", 70, 120, "corr_pass_8");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_8.png", 91, "Failing Z+Gamma JEC 300-400", 70, 120, "base_fail_8");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_8.png", 91, "Failing Z+Gamma JEC and JMC 300-400", 70, 120, "corr_fail_8");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_base_9.png", 91, "Passing Z+Gamma JEC 400-500", 70, 120, "base_pass_9");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_pass_corr_9.png", 91, "Passing Z+Gamma JEC and JMC 400-500", 70, 120, "corr_pass_9");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_base_9.png", 91, "Failing Z+Gamma JEC 400-500", 70, 120, "base_fail_9");
	FitFunc("../ZGamma_plots.root", "../plots/ZGamma_fail_corr_9.png", 91, "Failing Z+Gamma JEC and JMC 400-500", 70, 120, "corr_fail_9");

}

//save func
//malloc a 3 size array
//get the 3 values: mean, std dev, amp w get params
//use getChisquare() for chi square
