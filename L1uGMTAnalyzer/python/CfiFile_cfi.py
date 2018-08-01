import FWCore.ParameterSet.Config as cms

demo = cms.EDAnalyzer('L1uGMTAnalyzer'
     ,tracks = cms.untracked.InputTag('ctfWithMaterialTracks')
)
