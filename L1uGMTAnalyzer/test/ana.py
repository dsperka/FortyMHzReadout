import FWCore.ParameterSet.Config as cms

process = cms.Process( "TEST" )


process.Timing = cms.Service("Timing",
                             summaryOnly = cms.untracked.bool(True)
                             )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
process.myFilter = hlt.hltHighLevel.clone(
    HLTPaths =[ "HLT_ZeroBias_v5", "HLT_ZeroBias_v6" ],
    throw = False
    )

process.Ana = cms.EDAnalyzer('L1uGMTAnalyzer',
    saveTags = cms.bool( True ),
    CentralBxOnly = cms.bool( False ),
    SelectQualities = cms.vint32(  ),
    CandTag = cms.InputTag( 'gmtStage2Digis','Muon' )
)

process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:/eos/cms/store/data/Run2018A/ZeroBias/AOD/PromptReco-v1/000/315/768/00000/26EA83D2-9D52-E811-AE35-02163E019ED0.root'

 #'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/625/00000/940739C1-EF6C-E811-8DB0-02163E00B32B.root'

#'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/591/00000/281DB004-B96C-E811-A08C-FA163E3D3DF8.root',
#'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/591/00000/4A8990D9-BB6C-E811-A66D-FA163E54B47A.root',
#'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/591/00000/680FE48A-C26C-E811-954E-FA163E559492.root',
#'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/591/00000/7233408F-CF6C-E811-8F38-02163E01A113.root',
#'file:/eos/cms/store/data/Run2018B/ZeroBias/MINIAOD/PromptReco-v1/000/317/591/00000/AC4098DC-B56C-E811-9FA1-FA163E5234B3.root',

 #'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/FEAB4497-5CD4-E711-921E-A0369F7F8E80.root',
 #'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/FAA4C8D3-D4D3-E711-A750-484D7E8DF114.root',
 'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/F6F95AF8-26D4-E711-9DA0-A4BF0112BC14.root',
 'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/EEA0CA2C-2AD4-E711-A6F9-A4BF01125780.root',
 'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/ECC0EC7C-26D4-E711-AD63-001E677926FC.root',
 'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/ECA9307E-3ED4-E711-9406-A4BF0112BD44.root',
 'root://xrootd-cms.infn.it//store/data/Run2017B/ZeroBias/MINIAOD/17Nov2017-v1/50000/EAED5891-5CD4-E711-BCB4-A4BF0112E3E8.root'

    ),
    inputCommands = cms.untracked.vstring(
        'keep *'
    )
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("outputL1uGMTAnalyzer.root")
)

#process.p = cms.Path(process.Ana)
process.p = cms.Path(process.myFilter*process.Ana)
