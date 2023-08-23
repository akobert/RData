#!/bin/bash

#This Script merges multiple files of the same bin (i.e. file 1,2,3,4... of DataC)

#echo -e "\n Hello World \n" >> file.txt

#echo -e "First Arg: $1"
#echo -e "Second Arg: $2"
#echo -e "Third Arg: $3"

hadd -f $1_2016_merged.root output/RData_$1_*.root

root -l $1_2016_merged.root <<-EOF
using namespace std;
.> $1.txt
cout<<"Total Events: "<<cut_vals->GetBinContent(0)<<endl;
cout<<"10% of Events: "<<cut_vals->GetBinContent(1)<<endl;
cout<<"nPhoton>0: "<<cut_vals->GetBinContent(2)<<endl;
cout<<"nJet>0: "<<cut_vals->GetBinContent(3)<<endl;
cout<<"Photon pT>220: "<<cut_vals->GetBinContent(4)<<endl;
cout<<"Direct Prompt Events (If Relevant): "<<cut_vals->GetBinContent(18)<<endl;
cout<<"Jet pT>220: "<<cut_vals->GetBinContent(5)<<endl;
cout<<"|Photon Eta|<2.4: "<<cut_vals->GetBinContent(6)<<endl;
cout<<"|Jet Eta|<2.4: "<<cut_vals->GetBinContent(7)<<endl;
cout<<"Tight CutBased Photon ID: "<<cut_vals->GetBinContent(8)<<endl;
cout<<"Jet ID>=2: "<<cut_vals->GetBinContent(9)<<endl;
cout<<"Softdrop Mass>0: "<<cut_vals->GetBinContent(10)<<endl;
cout<<"Photon200 Trigger Passed: "<<cut_vals->GetBinContent(11)<<endl;
cout<<"N2>0: "<<cut_vals->GetBinContent(12)<<endl;
cout<<"-7<rho<-2: "<<cut_vals->GetBinContent(13)<<endl;
cout<<"dR>2.2: "<<cut_vals->GetBinContent(14)<<endl;
cout<<"All Events After Selection: "<<cut_vals->GetBinContent(15)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.8: "<<cut_vals->GetBinContent(20)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.85: "<<cut_vals->GetBinContent(21)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.9: "<<cut_vals->GetBinContent(22)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.91: "<<cut_vals->GetBinContent(23)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.92: "<<cut_vals->GetBinContent(24)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.93: "<<cut_vals->GetBinContent(25)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.94: "<<cut_vals->GetBinContent(26)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.95: "<<cut_vals->GetBinContent(27)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.96: "<<cut_vals->GetBinContent(28)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.97: "<<cut_vals->GetBinContent(29)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.98: "<<cut_vals->GetBinContent(30)<<endl;
cout<<"Xqq/(Xqq+QCD)>0.99: "<<cut_vals->GetBinContent(31)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.8: "<<cut_vals->GetBinContent(32)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.85: "<<cut_vals->GetBinContent(33)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.9: "<<cut_vals->GetBinContent(34)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.91: "<<cut_vals->GetBinContent(35)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.92: "<<cut_vals->GetBinContent(36)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.93: "<<cut_vals->GetBinContent(37)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.94: "<<cut_vals->GetBinContent(38)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.95: "<<cut_vals->GetBinContent(39)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.96: "<<cut_vals->GetBinContent(40)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.97: "<<cut_vals->GetBinContent(41)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.98: "<<cut_vals->GetBinContent(42)<<endl;
cout<<"(Xqq+Xcc+Xbb)/(Xqq+Xcc+Xbb+QCD)>0.99: "<<cut_vals->GetBinContent(43)<<endl;
EOF


#rm output/RData_$1_UL_*.root

