#!/usr/bin/python
import ROOT
from array import array

ROOT.gROOT.SetBatch(ROOT.kTRUE)
fitName = 'CF13'
filename = "Analysed/OutputForLinearPlot_"+fitName+".txt"
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
    shift =1
    eng.append(float(line.split()[0+shift]))
    engErr.append(0.001*float(line.split()[0+shift]))
    mean.append(float(line.split()[1+shift]))
    meanErr.append(float(line.split()[2+shift]))
    sig.append(float(line.split()[3+shift]))
    sigErr.append(float(line.split()[4+shift]))
    mvp.append(float(line.split()[5+shift]))
    res.append(float(line.split()[3+shift])/float(line.split()[1]))

Canvas1 = ROOT.TCanvas("LinearGraph","LinearGraph",1366,768)
Canvas1.cd()


LGrp = ROOT.TGraphErrors(int(len(eng)),eng,mean,engErr,sig)

LGrp.SetMarkerStyle(20)
LGrp.SetMarkerSize(2)
LGrp.SetMarkerColor(ROOT.kRed)


f = LGrp.Fit("pol1","QMES","",20,50)

y=array('f')
x=array('f')
for i in range(20,90):
    y.append(f.Parameter(1)*float(i) + f.Parameter(0))
    x.append(float(i))

LGrph = ROOT.TGraph(int(len(x)),x,y)
# LGrph.SetMarkerStyle(20)
LGrph.SetLineColor(ROOT.kRed)
LGrph.SetLineStyle(5)
# LGrph.SetMarkerSize(2)

MGrp = ROOT.TMultiGraph()

MGrp.Add(LGrp,"AP")
MGrp.Add(LGrph,"AL")

MGrp.Draw("A")

MGrp.SetTitle("")
MGrp.GetXaxis().SetTitle("Beam Energy (GeV)");
MGrp.GetXaxis().SetLabelFont(62);
MGrp.GetXaxis().SetTitleFont(62);
MGrp.GetXaxis().SetTitleOffset(1.0);
MGrp.GetXaxis().SetTitleSize(0.048);

MGrp.GetYaxis().SetTitle("Mean MIPS");
MGrp.GetYaxis().SetLabelFont(62);
MGrp.GetYaxis().SetTitleFont(62);
MGrp.GetYaxis().SetTitleOffset(1.0);
MGrp.GetYaxis().SetTitleSize(0.048);


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
label1.AddText("HGCAL test beam, Oct 2017");
label1.Draw("same");
Canvas1.SetGridx();
Canvas1.SetGridy();
Canvas1.Update()
name = "Analysed/LinearPlot_"+fitName+".png"
Canvas1.SaveAs(name)

# raw_input("Enter to exit")
