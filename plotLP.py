#!/usr/bin/python
import ROOT
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
filename = "OutputForLinearPlot.txt"
f=open(filename)
lines=f.readlines()

eng=array( 'f' )
engErr=array( 'f' )
mean=array( 'f' )
meanErr=array( 'f' )
sig=array( 'f' )
sigErr=array( 'f' )
mvp=array( 'f' )
res=array( 'f' )




for line in lines:
    eng.append(float(line.split()[0]))
    engErr.append(0.001*float(line.split()[0]))
    mean.append(float(line.split()[1]))
    meanErr.append(float(line.split()[2]))
    sig.append(float(line.split()[3]))
    sigErr.append(float(line.split()[4]))
    mvp.append(float(line.split()[5]))
    res.append(float(line.split()[3])/float(line.split()[1]))

Canvas1 = ROOT.TCanvas("LinearGraph","LinearGraph",1366,768)
Canvas1.cd()
LGrp = ROOT.TGraphErrors(int(len(eng)),eng,mean,engErr,meanErr)
LGrp.SetTitle("")
LGrp.GetXaxis().SetTitle("Beam Energy (GeV)");
LGrp.GetXaxis().SetLabelFont(62);
LGrp.GetXaxis().SetTitleFont(62);
LGrp.GetXaxis().SetTitleOffset(1.0);
LGrp.GetXaxis().SetTitleSize(0.048);

LGrp.GetYaxis().SetTitle("Mean MIPS");
LGrp.GetYaxis().SetLabelFont(62);
LGrp.GetYaxis().SetTitleFont(62);
LGrp.GetYaxis().SetTitleOffset(1.0);
LGrp.GetYaxis().SetTitleSize(0.048);

LGrp.SetMarkerStyle(20)
LGrp.SetMarkerSize(2)
LGrp.SetMarkerColor(ROOT.kRed)
LGrp.Draw("AP")
LGrp.Fit("pol1","QME")
# ROOT.gStyle.SetOptFit(1111)

label2  = ROOT.TPaveText(0.09278351,0.9077253,0.3048601,0.9663805,"brNDC");
label2.SetBorderSize(0);
label2.SetFillStyle(0);
label2.SetTextAlign(12);
label2.SetTextSize(0.080);
label2.SetTextFont (62);
label2.AddText("CMS Preliminary");
label2.Draw("same");

label1=ROOT.TPaveText(0.5434462,0.9077253,0.6358763,0.9663805,"brNDC");
label1.SetBorderSize(0);
label1.SetFillStyle(0);
label1.SetTextAlign(12);
label1.SetTextSize(0.059);
label1.SetTextFont (62);
label1.AddText("HGCAL test beam, Sept 2017");
label1.Draw("same");
Canvas1.SetGridx();
Canvas1.SetGridy();
Canvas1.Update()
Canvas1.SaveAs("LinearPlot.png")


raw_input("Enter to exit")
