#!/bin/bash

#This Script merges separate bins of the same sample (i.e. DataA, DataB, DataC and DataD)

#echo -e "\n Hello World \n" >> file.txt

#echo -e "First Arg: $1"
#echo -e "Second Arg: $2"
#echo -e "Third Arg: $3"

hadd -f $1_UL_10.root $2*merged_10.root 



#rm output/RData_$1_UL_*.root

root -l $1_UL_10.root <<-EOF
using namespace std;
.> $1_10.txt
cout<<"Total Events: "<<cut_vals->GetBinContent(0)<<endl;
cout<<"10% of Events: "<<cut_vals->GetBinContent(1)<<endl;
cout<<"nPhoton>0: "<<cut_vals->GetBinContent(2)<<endl;
cout<<"nJet>0: "<<cut_vals->GetBinContent(3)<<endl;
cout<<"Photon pT>120: "<<cut_vals->GetBinContent(4)<<endl;
cout<<"Direct Prompt Events (If Relevant): "<<cut_vals->GetBinContent(18)<<endl;
cout<<"Jet pT>120: "<<cut_vals->GetBinContent(5)<<endl;
cout<<"|Photon Eta|<1.44: "<<cut_vals->GetBinContent(6)<<endl;
cout<<"|Jet Eta|<2.4: "<<cut_vals->GetBinContent(7)<<endl;
cout<<"Tight CutBased Photon ID: "<<cut_vals->GetBinContent(8)<<endl;
cout<<"Jet ID>=2: "<<cut_vals->GetBinContent(9)<<endl;
cout<<"Softdrop Mass>0: "<<cut_vals->GetBinContent(10)<<endl;
cout<<"Trigger(s) Passed: "<<cut_vals->GetBinContent(11)<<endl;
cout<<"N2>0: "<<cut_vals->GetBinContent(12)<<endl;
cout<<"-7<rho<-2: "<<cut_vals->GetBinContent(13)<<endl;
cout<<"dR>2.2: "<<cut_vals->GetBinContent(14)<<endl;
cout<<"All Events After Selection: "<<cut_vals->GetBinContent(15)<<endl;
cout<<"Passing Events: "<<cut_vals->GetBinContent(16)<<endl;
cout<<"Failing Events: "<<cut_vals->GetBinContent(17)<<endl;
cout<<"All Events After Selection (No Weights): "<<cut_vals->GetBinContent(19)<<endl;
cout<<"Passing Events (No Weights): "<<cut_vals->GetBinContent(20)<<endl;
cout<<"Failing Events (No Weights): "<<cut_vals->GetBinContent(21)<<endl;
cout<<"Events in Sample (No Weights): "<<cut_vals->GetBinContent(22)<<endl;
EOF

