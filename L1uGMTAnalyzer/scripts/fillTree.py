from ROOT import *
from math import *
#!/usr/bin/python                                                                                                                                            
#-----------------------------------------------                                                                                                             
import sys, os, pwd, commands, glob
import optparse, shlex, re
import time
from time import gmtime, strftime
import math
from array import array

#define function for parsing options
def parseOptions():

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-i', '--input', dest='INPUT', type='string', help='input file')
    parser.add_option('-o', '--output', dest='OUTPUT', type='string', help='output file')
    parser.add_option('-n', '--njobs', dest='NJOBS', type=int, help='njobs')
    parser.add_option('-j', '--job', dest='JOB', type=int, help='job')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# define function for processing the external os commands
def processCmd(cmd, quite = 0):
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output

def fillTree():

  global opt, args
  parseOptions()

  f = TFile(opt.INPUT,"READ")
  t = f.Get("events")

  fout = TFile( opt.OUTPUT+'_'+str(opt.JOB)+'.root', 'recreate' )
  tout = TTree( 'dimu', 'dimuons' )

  mll = array( 'f', [ 0. ] )
  tout.Branch( 'mll', mll, 'mll/F' )

  ptll = array( 'f', [ 0. ] )
  tout.Branch( 'ptll', ptll, 'ptll/F' )

  dPhi = array( 'f', [ 0. ] )
  tout.Branch( 'dPhi', dPhi, 'dPhi/F' )

  dEta = array( 'f', [ 0. ] )
  tout.Branch( 'dEta', dEta, 'dEta/F' )

  dR = array( 'f', [ 0. ] )
  tout.Branch( 'dR', dR, 'dR/F' )

  q1q2 = array( 'i', [ 0 ] )
  tout.Branch( 'q1q2', q1q2, 'q1q2/I' )

  eta1 = array( 'f', [ 0. ] )
  tout.Branch( 'eta1', eta1, 'eta1/F' )

  eta2 = array( 'f', [ 0. ] )
  tout.Branch( 'eta2', eta2, 'eta2/F' )

  phi1 = array( 'f', [ 0. ] )
  tout.Branch( 'phi1', phi1, 'phi1/F' )

  phi2 = array( 'f', [ 0. ] )
  tout.Branch( 'phi2', phi2, 'phi2/F' )

  pt1 = array( 'f', [ 0. ] )
  tout.Branch( 'pt1', pt1, 'pt1/F' )

  pt2 = array( 'f', [ 0. ] )
  tout.Branch( 'pt2', pt2, 'pt2/F' )

  N = t.GetEntriesFast();

  first = int(float(N)/float(opt.NJOBS)*float(opt.JOB-1))
  last = int(float(N)/float(opt.NJOBS)*float(opt.JOB))

  print first,last

  for event in xrange(first,last-1):

    t.GetEntry(event)

    if (event<first or event>last): continue
    if (event%10000==0): print event,N
  
    if (t.muon_pt.size()<2): continue
  
    for m1 in range(t.muon_pt.size()):
      if (t.muon_hwQual[m1]<12): continue
      if (t.muon_hwChargeValid[m1]==0): continue
      #if (abs(t.muon_eta[m1])>0.9): continue      

      for m2 in range(m1,t.muon_pt.size()):
        if (m1==m2): continue
        if (t.muon_hwQual[m2]<12): continue
        if (t.muon_hwChargeValid[m2]==0): continue
        #if (abs(t.muon_eta[m2])>0.9): continue

        #if (t.muon_BX[m1]!=0): continue
        #if (t.muon_BX[m2]!=0): continue
        if ((t.muon_BX[m1]+t.BX)!=(t.muon_BX[m2]+t.BX)): continue 

        eta1[0] = t.muon_EtaAtVtx[m1]
        eta2[0] = t.muon_EtaAtVtx[m2]
        phi1[0] = t.muon_PhiAtVtx[m1]
        phi2[0] = t.muon_PhiAtVtx[m2]
        pt1[0] = t.muon_pt[m1]
        pt2[0] = t.muon_pt[m2]

        p4m1 = TLorentzVector()
        p4m1.SetPtEtaPhiM(t.muon_pt[m1],t.muon_EtaAtVtx[m1],t.muon_PhiAtVtx[m1],0.1056)

        p4m2 = TLorentzVector()
        p4m2.SetPtEtaPhiM(t.muon_pt[m2],t.muon_EtaAtVtx[m2],t.muon_PhiAtVtx[m2],0.1056)
        
        dPhi[0] = p4m1.DeltaPhi(p4m2)
        dEta[0] = t.muon_EtaAtVtx[m1]-t.muon_EtaAtVtx[m2]
        dR[0] = p4m1.DeltaR(p4m2)

        p4mm = p4m1+p4m2
        mll[0] = p4mm.M()
        ptll[0] = p4mm.Pt()
        
        if (t.muon_charge[m1]!=t.muon_charge[m2]):
          q1q2[0]=-1
        elif (t.muon_charge[m1]==t.muon_charge[m2]): 
          q1q2[0]=1

        tout.Fill()

  fout.Write()
  fout.Close()
    


if __name__ == "__main__":
  fillTree()
