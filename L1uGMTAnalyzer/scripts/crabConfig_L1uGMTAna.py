from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration() 
config.section_('General')
config.General.workArea = 'results_L1uGMTAna_Jun20_v1/'

#config.General.requestName = 'ZeroBias_Run2018A-PromptReco-v1'
#config.General.requestName = 'ZeroBias_Run2018B-PromptReco-v1'
#config.General.requestName = 'ZeroBias_Run2017F-17Nov2017-v1'
config.General.requestName = 'ZeroBiasDST_Run2018B-v1'
#config.General.requestName = 'JpsiToMuMu_OniaMuonFilter_TuneCP5_13TeV-pythia8'
#config.General.requestName = 'Min_Bias_13TeV_pythia8_TuneCUETP8M1'
#config.General.requestName = 'SingleNeutrino'
#config.General.requestName = 'QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8' 
#config.General.requestName = 'QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8' 
#config.General.requestName = 'QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8' 
#config.General.requestName = 'UpsilonMuMu_UpsilonPt6_TuneCP5_13TeV-pythia8-evtgen' 

config.General.transferOutputs = True
config.General.transferLogs=True
config.General.failureLimit=1

import os
config.section_('JobType')
#config.JobType.psetName = 'ana.py'
config.JobType.psetName = 'nanoDSTana.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['outputL1uGMTAnalyzer.root']

config.section_('Data')
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
#config.Data.inputDataset = '/ZeroBias/Run2018A-PromptReco-v1/MINIAOD'
#config.Data.inputDataset = '/ZeroBias/Run2018B-PromptReco-v1/MINIAOD'
#config.Data.inputDataset = '/ZeroBias/Run2017F-17Nov2017-v1/MINIAOD'
config.Data.inputDataset = '/L1Accept/Run2018B-v1/RAW'
#config.Data.inputDataset = '/JpsiToMuMu_OniaMuonFilter_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'
#config.Data.inputDataset = '/Min_Bias_13TeV_pythia8_TuneCUETP8M1/RunIISummer17MiniAOD-FlatPU0to75_92X_upgrade2017_realistic_v10-v2/MINIAODSIM'
#config.Data.inputDataset = '/SingleNeutrino/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM'
#config.Data.inputDataset = '/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM'
#config.Data.inputDataset = '/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM'
#config.Data.inputDataset = '/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM'
#config.Data.inputDataset = '/UpsilonMuMu_UpsilonPt6_TuneCP5_13TeV-pythia8-evtgen/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'

#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 20000000
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5

config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/%s/L1uGMTAna/results_L1uGMTAna_Jun20_v1/' % (getUsernameFromSiteDB())
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_MuonPhys.txt'
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-317391_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'

config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ['T2_*']
