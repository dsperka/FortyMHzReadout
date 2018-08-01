from ROOT import *
from math import *

from tdrStyle import setTDRStyle
setTDRStyle()

f = {}
t = {}
h_os = {}
h_ss = {}
hstack = {}
diff = {}

#f[1] = TFile("ZeroBias17_v3.root","READ")
f[1] = TFile("ZeroBias18DST.root","READ")
t[1] = f[1].Get("dimu")

#9253600. pb, events = 15049463 w = 0.615
f[2] = TFile("Jpsi.root","READ")
t[2] = f[2].Get("dimu")

#430155. pb , events= 6919940 w = 0.062
f[3] = TFile("Upsilon.root","READ")
t[3] = f[3].Get("dimu")

#3336011. pb, 5748990 events w = 0.58
f[4] = TFile("QCD_15-20.root","READ")
t[4] = f[4].Get("dimu")
#3987854. pb, 28006402 events w = 0.14
f[5] = TFile("QCD_20-30.root","READ")
t[5] = f[5].Get("dimu")
#1705381. pb, 28667918 events w = 0.059
f[6] = TFile("QCD_30-50.root","READ")
t[6] = f[6].Get("dimu")

var = "mll"
varName = "mll_jun20"
varLabel = "M(#mu#mu) [GeV]"
cut = "mll<15 && dR>0.3 && abs(eta1)<0.7 && abs(eta2)<0.7"
bin = 60
low = 0.0
high = 15.0
massnorm = True

#var = "mll"
#varName = "mll_jun14_07toInf"
#varLabel = "M(#mu#mu) [GeV]"
##cut = "mll<15 && dR>0.3 && abs(eta1)>0.7 && abs(eta2)>0.7 && abs(eta1)<0.9 && abs(eta2)<0.9"
#cut = "mll<15 && dR>0.3 && abs(eta1)>0.7 && abs(eta2)>0.7"
#bin = 60
#low = 0.0
#high = 15.0
#massnorm = False

#var = "dPhi"
#varName = "dPhi_jun14"
#varLabel = "|#Delta#phi(#mu#mu)|"
#cut = "mll<15 && dR>0.3 && abs(eta1)<0.7 && abs(eta2)<0.7"
#bin = 32
#low = -3.2
#high = 3.2
#massnorm = False

#var = "dPhi"
#varName = "dPhi_jun14_07toInf"
#varLabel = "|#Delta#phi(#mu#mu)|"
##cut = "mll<15 && dR>0.3 && abs(eta1)>0.7 && abs(eta2)>0.7 && abs(eta1)<0.9 && abs(eta2)<0.9"
#cut = "mll<15 && dR>0.3 && abs(eta1)>0.7 && abs(eta2)>0.7"
#bin = 32
#low = -3.2
#high = 3.2
#massnorm = False


for i in range(1,7):

  if (i==2): weight = 0.615*.0317
  elif (i==3): weight = 0.062*.0317
  elif (i==4): weight = 0.58*.0317
  elif (i==5): weight = 0.14*.0317
  elif (i==6): weight = 0.059*.0317
  else: weight = 1.0

  h_os[i] = TH1F("h_"+varName+str(i)+"_os","h_"+varName+str(i)+"_os",bin,low,high)
  h_os[i].Sumw2()
  t[i].Draw(var+">>h_"+varName+str(i)+"_os",str(weight)+"*("+cut+" && q1q2<0)","goff")

  h_ss[i] = TH1F("h_"+varName+str(i)+"_ss","h_"+varName+str(i)+"_ss",bin,low,high)
  h_ss[i].Sumw2()
  t[i].Draw(var+">>h_"+varName+str(i)+"_ss",str(weight)+"*("+cut+" && q1q2>0)","goff")

  print h_os[i].Integral()

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
c1 = TCanvas("c1","c1",800,800)
#c1.SetLogy()
c1.cd()
c1.SetBottomMargin(0.5)
hdum = TH1F("","",bin,low,high)
hdum.SetMaximum(1.1*(h_os[1].GetMaximum()+h_ss[1].GetMaximum()))
hdum.GetXaxis().SetTitleSize(0)
hdum.GetXaxis().SetLabelSize(0)
hdum.Draw("hist")
leg = TLegend(0.7,0.8,0.9,0.9)

for i in range(1,5):
  if (i==1): 
    h_os[i].SetLineColor(1)    
    h_os[i].SetLineWidth(2)    
    h_ss[i].SetLineColor(1)    
    h_ss[i].SetLineWidth(2)    
    h_ss[i].SetLineStyle(2)    
    leg.AddEntry(h_os[i],"ZeroBias OS+SS")
    leg.AddEntry(h_ss[i],"ZeroBias SS")
  else: 
    h_os[i].SetLineColor(i)    
    h_os[i].SetLineWidth(2)    
    h_ss[i].SetLineColor(i)    
    h_ss[i].SetLineWidth(2)    
    h_ss[i].SetLineStyle(2)    

  hstack[i] = THStack()

  if (i==1): 

    hstack[i].Add(h_ss[i])
    hstack[i].Add(h_os[i])
    hstack[i].Draw("ehistsame")

    print "ZeroBias SS",h_ss[i].Integral()
    print "ZeroBias OS",h_os[i].Integral()
  if (i==4):

    h_ss[4].SetLineColor(4)
    h_ss[5].SetLineColor(4)
    h_ss[6].SetLineColor(4)
    h_os[4].SetLineColor(4)
    h_os[5].SetLineColor(4)
    h_os[6].SetLineColor(4)
    
    h_ss[i].Add(h_ss[5])
    h_ss[i].Add(h_ss[6])  
    h_os[i].Add(h_os[5])
    h_os[i].Add(h_os[6])

    #qcdscale = (h_os[1].Integral()+h_ss[1].Integral())/(h_os[i].Integral()+h_ss[i].Integral())
    qcdscale = (h_os[1].Integral())/(h_os[i].Integral())
    h_os[i].Scale(qcdscale)
    h_ss[i].Scale(qcdscale)

    print "QCD SS",h_ss[i].Integral()
    print "QCD OS",h_os[i].Integral()

    h_os[i].SetLineColor(4)
    h_ss[i].SetLineColor(4)
    h_ss[i].SetLineStyle(2)
    hstack[i].Add(h_ss[i])
    hstack[i].Add(h_os[i])
    leg.AddEntry(h_os[i],"QCD OS+SS")
    leg.AddEntry(h_ss[i],"QCD SS")
    hstack[i].Draw("histsame")

leg.Draw()

pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0);
#pad.SetLogx()
pad.SetTopMargin(0.5);
#pad.SetRightMargin(0.03);
pad.SetFillColor(0);
pad.SetGridy(1);
pad.SetFillStyle(0);
pad.Draw();
pad.cd(0);

leg2 = TLegend(0.7,0.35,0.9,0.45)

diff[1] = h_os[1].Clone("diff")
diff[1].Add(h_ss[1],-1)

hdum2 = TH1F("","",bin,low,high)
hdum2.SetMaximum(1.2*(diff[1].GetMaximum()))
hdum2.SetMinimum(1.2*(diff[1].GetMinimum()))
hdum2.GetXaxis().SetTitle(varLabel)
hdum2.Draw("hist")

for i in range(1,5):
  
  if (i==1):
    diff[1].SetMarkerStyle(20)
    diff[1].SetMarkerSize(1.2)
    diff[1].SetMarkerColor(1)
    diff[1].SetLineColor(1)
    diff[1].Draw("epsame")
    leg2.AddEntry(diff[1],"ZeroBias OS-SS")
  elif (i==2):
    diff[i] = h_os[i].Clone("diff")
    diff[i].Add(h_ss[i],-1)
    diff[i].SetMarkerStyle(20)
    diff[i].SetMarkerSize(1.2)
    diff[i].SetMarkerColor(i)
    diff[i].SetLineColor(i)
    if (diff[i].Integral()>0):
      if (massnorm):
        diff[i].Scale(diff[1].Integral(0,20)/diff[i].Integral(0,20))
      else:
        diff[i].Scale(0.25*diff[1].Integral()/diff[i].Integral())
    diff[i].Draw("histsame")
    leg2.AddEntry(diff[i],"J/#Psi MC OS-SS")
  elif (i==3):
    diff[i] = h_os[i].Clone("diff")
    diff[i].Add(h_ss[i],-1)
    diff[i].SetMarkerStyle(20)
    diff[i].SetMarkerSize(1.2)
    diff[i].SetMarkerColor(i)
    diff[i].SetLineColor(i)
    if (diff[i].Integral()>0):
      if (massnorm):
        diff[i].Scale(diff[1].Integral(36,44)/diff[i].Integral(36,44))
      else:
        diff[i].Scale(0.25*diff[1].Integral()/diff[i].Integral())
    diff[i].Draw("histsame")
    leg2.AddEntry(diff[i],"#Upsilon MC OS-SS")
  elif (i==4):
    diff[i] = h_os[i].Clone("diff")
    #diff[i].Add(h_os[5])
    #diff[i].Add(h_os[6])
    #diff[i].Add(h_ss[i],-1)
    #diff[i].Add(h_ss[5],-1)
    diff[i].Add(h_ss[i],-1)
    diff[i].SetMarkerStyle(20)
    diff[i].SetMarkerSize(1.2)
    diff[i].SetMarkerColor(4)
    diff[i].SetLineColor(4)
    if (diff[i].Integral()>0):
      if (massnorm):
        diff[i].Scale(diff[1].Integral()/diff[i].Integral())
      else:
        diff[i].Scale(diff[1].Integral()/diff[i].Integral())
    diff[i].Draw("histsame")
    leg2.AddEntry(diff[i],"QCD MC OS-SS")

diff[1].Draw("epsame")
leg2.Draw("same")


latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.6*c1.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right                                       
latex2.DrawLatex(0.92, 0.94," 31.7 nb^{-1} (13 TeV)")


c1.SaveAs(varName+".png")
c1.SaveAs(varName+".pdf")
c1.SaveAs(varName+".root")
      
