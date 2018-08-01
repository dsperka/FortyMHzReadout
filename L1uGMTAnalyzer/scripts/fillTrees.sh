#!/bin/bash

#for i in {1..4}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v2/JpsiToMuMu_OniaMuonFilter_TuneCP5_13TeV-pythia8/outputL1uGMTAnalyzer.root -o Jpsi -n 5 -j $i >& log_Jpsi_$i.txt &
#done

#for i in {1..4}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v2/UpsilonMuMu_UpsilonPt6_TuneCP5_13TeV-pythia8-evtgen/crab_UpsilonMuMu_UpsilonPt6_TuneCP5_13TeV-pythia8-evtgen/180613_154330/0000/outputL1uGMTAnalyzer_1.root -o Upsilon -n 5 -j $i >& log_$i.txt &
#done

#for i in {1..4}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v2/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/outputL1uGMTAnalyzer.root -o QCD_15-20 -n 5 -j $i >& log_QCD_$i.txt &
#done

#for i in {1..4}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v2/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/outputL1uGMTAnalyzer.root -o QCD_20-30 -n 5 -j $i >& log_QCD20_$i.txt &
#done

#for i in {1..4}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v2/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/outputL1uGMTAnalyzer.root -o QCD_30-50 -n 5 -j $i >& log_QCD30_$i.txt &
#done


#for i in {1..8}
#do
#   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun12_v3/ZeroBias/outputL1uGMTAnalyzer.root -o ZeroBias17_v3 -n 8 -j $i >& log_ZeroBias_v3_$i.txt &
#done

for i in {1..4}
do
   python -u fillTree.py -i /eos/cms/store/user/dsperka/L1uGMTAna/results_L1uGMTAna_Jun20_v1/L1Accept/outputL1uGMTAnalyzer.root -o ZeroBias18DST -n 4 -j $i >& log_ZeroBias18DST_$i.txt &
done


