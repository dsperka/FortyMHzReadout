#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <TROOT.h>
#include "TMath.h"
#include "TLorentzVector.h"

using namespace std;

static const unsigned ptMask_ = 0x1FF;
static const unsigned ptShift_ = 10;
static const unsigned qualMask_ = 0xF;
static const unsigned qualShift_ = 19;
static const unsigned absEtaMask_ = 0xFF;
static const unsigned absEtaShift_ = 21;
static const unsigned absEtaAtVtxShift_ = 23;
static const unsigned etaSignShift_ = 29;
static const unsigned etaAtVtxSignShift_ = 31;
static const unsigned phiMask_ = 0x3FF;
static const unsigned phiShift_ = 11;
static const unsigned phiAtVtxShift_ = 0;
static const unsigned chargeShift_ = 2;
static const unsigned chargeValidShift_ = 3;
static const unsigned tfMuonIndexMask_ = 0x7F;
static const unsigned tfMuonIndexShift_ = 4;
static const unsigned isoMask_ = 0x3;
static const unsigned isoShift_ = 0;

struct muon_t {
    int qual;
    int charge;
    int chargeValid;
    int hwPt;
    int hwEta;
    int hwPhi;
    int hwEtaAtVtx;
    int hwPhiAtVtx;
};


int calcHwEta(const uint32_t& raw, const unsigned absEtaShift, const unsigned etaSignShift)
{
    // eta is coded as two's complement                                   
    int abs_eta = (raw >> absEtaShift) & absEtaMask_;
    if ((raw >> etaSignShift) & 0x1) {
        return abs_eta - (1 << (etaSignShift - absEtaShift));
    } else {
        return abs_eta;
    }
}


muon_t unpackmuon(uint32_t raw_data_00_31, uint32_t raw_data_32_63) {

    muon_t ret;

    ret.hwPt = (raw_data_00_31 >> ptShift_) & ptMask_;
    ret.qual = (raw_data_00_31 >> qualShift_) & qualMask_;
    //ret.iso = (raw_data_32_63 >> isoShift_) & isoMask_;
    // charge is coded as -1^chargeBit                           
    ret.charge = (raw_data_32_63 >> chargeShift_) & 0x1;
    ret.chargeValid = (raw_data_32_63 >> chargeValidShift_) & 0x1;
    //ret.tfMuonIndex = (raw_data_32_63 >> tfMuonIndexShift_) & tfMuonIndexMask_;

    // coordinates at the muon system
    ret.hwEta = calcHwEta(raw_data_32_63, absEtaShift_, etaSignShift_);
    ret.hwPhi = (raw_data_32_63 >> phiShift_) & phiMask_;
    
    // coordinates at the vertex                                                                                                                                                                     
    ret.hwEtaAtVtx = calcHwEta(raw_data_00_31, absEtaAtVtxShift_, etaAtVtxSignShift_);
    ret.hwPhiAtVtx = (raw_data_00_31 >> phiAtVtxShift_) & phiMask_;
    
    //ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > vec{(hwPt-1)*float(0.5), hwEta*float(0.010875), hwPhi*float(0.010908), 0.0};
    //TLorentzVector vec;
    //vec.SetPtEtaPhiM((hwPt-1)*float(0.5), hwEta*float(0.010875), hwPhi*float(0.010908), 0.0);
    
    //math::PtEtaPhiMLorentzVector vec{(hwPt-1)*0.5, hwEta*0.010875, hwPhi*0.010908, 0.0};
    //math::PtEtaPhiMLorentzVector vecAtVtx{(hwPt-1)*0.5, hwEtaAtVtx*0.010875, hwPhiAtVtx*0.010908, 0.0};
    //std::cout << "Mu" << ": eta " << hwEta << " phi " << hwPhi << " pT " << hwPt << " iso " << iso << " qual " << qual << " charge " << charge << " charge valid " << chargeValid << std::endl;
      
    return ret;

}




int main()
{

    std::vector<uint32_t> data;

    ifstream inFile ("uGMT_rawdata_onlyFinalMuons_BCOC.txt");
    char oneline[11];
    while (inFile)
    {
        inFile.getline(oneline, 11);

        uint32_t lineint;
        std::stringstream ss;
        ss << std::hex << oneline;
        ss >> lineint;

        if (lineint==0) continue;

        data.push_back(lineint);
    }
    inFile.close();


    int repeat=10000;
    //int repeat=1;
    std::cout<<"nmuons: "<<data.size()*repeat<<std::endl;

    std::vector<muon_t> bcmuons;

    uint32_t bc = data[0];
    uint32_t oc = data[1];

    for (int j=0; j<repeat+1; ++j) {
        
        // process data six frames at a time       
        for (int i=0; i<data.size(); i+=6) {

            // if this is a new bc or oc then do analysis and clear the bcmuon vector
            if (data[i]!=bc || data[i+1]!=oc) { 
                
                
                for (int m1=0; m1<bcmuons.size(); ++m1) {
                    if (!bcmuons[m1].chargeValid) continue;
                    if (bcmuons[m1].qual<12) continue;
                    for (int m2=m1+1; m2<bcmuons.size(); ++m2) {
                        if (!bcmuons[m2].chargeValid) continue;
                        if (bcmuons[m2].qual<12) continue;

                        //std::cout<<m1<<" "<<m2<<" "<<bcmuons[m1].hwPt<<" "<<bcmuons[m1].hwEta<<" "<<bcmuons[m2].hwPt<<" "<<bcmuons[m2].hwEta<<std::endl;
                        int sumpt = bcmuons[m1].hwPt+bcmuons[m2].hwPt;

                        //(hwPt-1)*0.5, hwEtaAtVtx*0.010875, hwPhiAtVtx*0.010908, 0.0

                        
                        float mass = sqrt(0.5*(bcmuons[m1].hwPt-1)*(bcmuons[m2].hwPt-1)*(cosh(0.010875*(bcmuons[m1].hwEtaAtVtx-bcmuons[m1].hwEtaAtVtx))-cos(0.010908*(bcmuons[m1].hwPhiAtVtx-bcmuons[m1].hwPhiAtVtx))));
                        int charge = bcmuons[m1].charge*bcmuons[m2].charge;
                            
                    }
                }

                bcmuons.clear();

            }

            bc = data[i];
            oc = data[i+1];

            muon_t muon1, muon2;
            muon1 = unpackmuon(data[i+2],data[i+3]);
            muon2 = unpackmuon(data[i+4],data[i+5]);

            if (muon1.hwPt>0) bcmuons.push_back(muon1);
            if (muon2.hwPt>0) bcmuons.push_back(muon2);

        }

    }

    return 0;

}
