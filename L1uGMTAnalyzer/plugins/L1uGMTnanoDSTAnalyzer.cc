// -*- C++ -*-
//
// Package:    L1Scouting/L1uGMTAnalyzer
// Class:      L1uGMTnanoDSTAnalyzer
//
/**\class L1uGMTAnalyzer L1uGMTnanoDSTAnalyzer.cc L1Scouting/L1uGMTAnalyzer/plugins/L1uGMTnanoDSTAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  David Sperka
//         Created:  Mon, 07 May 2018 14:43:35 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Provenance/interface/EventAuxiliary.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerRefsCollections.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/L1Trigger/interface/BXVector.h"

#include "TTree.h"
//
// class declaration
//

class L1uGMTnanoDSTAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit L1uGMTnanoDSTAnalyzer(const edm::ParameterSet&);
      ~L1uGMTnanoDSTAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;


      // ----------member data ---------------------------

      TTree *events;

      //input tag identifying the product containing muons
      edm::InputTag                           candTag_;
      edm::EDGetTokenT<l1t::MuonBxCollection> candToken_;

      /// Quality codes:
      /// to be updated with new L1 quality definitions
      int qualityBitMask_;    
      /// use central bx only muons
      bool centralBxOnly_;

      //TFileService
      edm::Service<TFileService> fs;

      ULong64_t Run, Event, Lumi, BX, Orbit;

      vector<float> muon_BX;
      vector<float> muon_hwPt;
      vector<float> muon_hwEta;
      vector<float> muon_hwPhi;
      vector<float> muon_hwCharge;
      vector<float> muon_hwChargeValid;
      vector<float> muon_hwQual;
   
      vector<float> muon_pt;
      vector<float> muon_eta;
      vector<float> muon_phi;
      vector<float> muon_charge;
   
      vector<float> muon_hwEtaAtVtx;
      vector<float> muon_hwPhiAtVtx;
      vector<float> muon_EtaAtVtx;
      vector<float> muon_PhiAtVtx;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
L1uGMTnanoDSTAnalyzer::L1uGMTnanoDSTAnalyzer(const edm::ParameterSet& iConfig)
 :
  candTag_( iConfig.getParameter<edm::InputTag>("CandTag") ),
  candToken_( consumes<l1t::MuonBxCollection>(candTag_)),
  centralBxOnly_( iConfig.getParameter<bool>("CentralBxOnly") )
{


    events = new TTree("events","events");

    //set the quality bit mask
    qualityBitMask_ = 0;
    vector<int> selectQualities = iConfig.getParameter<vector<int> >("SelectQualities");
    for(int selectQualitie : selectQualities){
//     if(selectQualities[i] > 7){  // FIXME: this will be updated once we have info from L1
//       throw edm::Exception(edm::errors::Configuration) << "QualityBits must be smaller than 8!";
//     }
        qualityBitMask_ |= 1<<selectQualitie;
    }

}


L1uGMTnanoDSTAnalyzer::~L1uGMTnanoDSTAnalyzer()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1uGMTnanoDSTAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace std;
   using namespace edm;
   using namespace trigger;
   using namespace l1t;


   Run = iEvent.id().run();
   Event = iEvent.id().event();
   Lumi = iEvent.id().luminosityBlock();
   BX = iEvent.bunchCrossing();
   Orbit = iEvent.orbitNumber();

   muon_BX.clear();
   muon_hwPt.clear();
   muon_hwEta.clear();
   muon_hwPhi.clear();
   muon_hwCharge.clear();
   muon_hwChargeValid.clear();
   muon_hwQual.clear();
   
   muon_pt.clear();
   muon_eta.clear();
   muon_phi.clear();
   muon_charge.clear();
   
   muon_hwEtaAtVtx.clear();
   muon_hwPhiAtVtx.clear();
   muon_EtaAtVtx.clear();
   muon_PhiAtVtx.clear();

   Handle< BXVector<l1t::Muon> > allMuons ;
   iEvent.getByToken(candToken_,allMuons);

   for (int ibx = allMuons->getFirstBX(); ibx <= allMuons->getLastBX(); ++ibx) {
       if (centralBxOnly_ && (ibx != 0)) continue;
       for (auto it = allMuons->begin(ibx); it != allMuons->end(ibx); it++){

           MuonRef muon(allMuons, distance(allMuons->begin(allMuons->getFirstBX()),it) );

           muon_BX.push_back(ibx);
           muon_hwPt.push_back(muon->hwPt());
           muon_hwEta.push_back(muon->hwEta());
           muon_hwPhi.push_back(muon->hwPhi());
           muon_hwCharge.push_back(muon->hwCharge());
           muon_hwChargeValid.push_back(muon->hwChargeValid());
           muon_hwQual.push_back(muon->hwQual());

           muon_pt.push_back(muon->pt());
           muon_eta.push_back(muon->eta());
           muon_phi.push_back(muon->phi());
           muon_charge.push_back(muon->charge());
           
           muon_hwEtaAtVtx.push_back(muon->hwEtaAtVtx());
           muon_hwPhiAtVtx.push_back(muon->hwPhiAtVtx());
           muon_EtaAtVtx.push_back(muon->etaAtVtx());
           muon_PhiAtVtx.push_back(muon->phiAtVtx());

       }
   }

   events->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void
L1uGMTnanoDSTAnalyzer::beginJob()
{

    events->Branch("Run",&Run,"Run/l");
    events->Branch("Event",&Event,"Event/l");
    events->Branch("Lumi",&Lumi,"Lumi/l");
    events->Branch("BX",&BX,"BX/l");
    events->Branch("Orbit",&Orbit,"Orbit/l");

    events->Branch("muon_BX",&muon_BX);
    events->Branch("muon_hwPt",&muon_hwPt);
    events->Branch("muon_hwEta",&muon_hwEta);
    events->Branch("muon_hwPhi",&muon_hwPhi);
    events->Branch("muon_hwCharge",&muon_hwCharge);
    events->Branch("muon_hwChargeValid",&muon_hwChargeValid);
    events->Branch("muon_hwQual",&muon_hwQual);
  
    events->Branch("muon_pt",&muon_pt);
    events->Branch("muon_eta",&muon_eta);
    events->Branch("muon_phi",&muon_phi);
    events->Branch("muon_charge",&muon_charge);
  
    events->Branch("muon_hwEtaAtVtx",&muon_hwEtaAtVtx);
    events->Branch("muon_hwPhiAtVtx",&muon_hwPhiAtVtx);
    events->Branch("muon_EtaAtVtx",&muon_EtaAtVtx);
    events->Branch("muon_PhiAtVtx",&muon_PhiAtVtx);

}

// ------------ method called once each job just after ending the event loop  ------------
void
L1uGMTnanoDSTAnalyzer::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1uGMTnanoDSTAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1uGMTnanoDSTAnalyzer);
