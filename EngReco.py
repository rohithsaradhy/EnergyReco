#!/usr/bin/python
from ADCtoMIPS import ADCtoMIPS
import ROOT
import sys
import os
import time


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptFit(1110)
energy = 50

if len(sys.argv) > 1:
    energy = int(sys.argv[1])




F_Input_Name = "/home/rsaradhy/Work/Output/TransitionH_L/New_Data/Oct_NTuple/Electron/"+str(energy)+"GeV.root"
print "Opening File: " + F_Input_Name
F_Input = ROOT.TFile(F_Input_Name)
Tree_Input = F_Input.Get("pulseshapeplotter/T")#


# for ADCtoMIPs ...
f=open("Final_Oct_H6_HG_LG_Datbase.txt")
lines=f.readlines()
f2=open("Final_Oct_H6_LG_TOT_Datbase.txt")
lines2=f2.readlines()
# print ADCtoMIPS(0,0,2700,2500,376,lines,lines2)
'''
Reference branches available...

  T->Branch("Hit_Sensor_Channel", &Hit_Sensor_Channel);
  T->Branch("Hit_Sensor_Layer", &Hit_Sensor_Layer);
  T->Branch("Hit_Sensor_Skiroc", &Hit_Sensor_Skiroc);

  T->Branch("Hit_Sensor_Cell_X", &Hit_Sensor_Cell_X);
  T->Branch("Hit_Sensor_Cell_Y", &Hit_Sensor_Cell_Y);
  T->Branch("Hit_Sensor_Cell_HG", &Hit_Sensor_Cell_HG); //time sample 3
  T->Branch("Hit_Sensor_Cell_HG_Sub", &Hit_Sensor_Cell_HG_Sub); //time sample 3
  T->Branch("Hit_Sensor_Cell_LG", &Hit_Sensor_Cell_LG); //time sample 3
  T->Branch("Hit_Sensor_Cell_LG_Sub", &Hit_Sensor_Cell_LG_Sub); //time sample 3
  T->Branch("Hit_Sensor_Cell_ToT_Slow", &Hit_Sensor_Cell_ToT_Slow);
  T->Branch("Hit_Sensor_Cell_ToA_Fall", &Hit_Sensor_Cell_ToA_Fall);
  T->Branch("Hit_Sensor_Cell_ToA_Rise", &Hit_Sensor_Cell_ToA_Rise);

  T->Branch("Hit_Sensor_Cell_HG_Amplitude", &Hit_Sensor_Cell_HG_Amplitude);
  T->Branch("Hit_Sensor_Cell_HG_Amplitude_Error", &Hit_Sensor_Cell_HG_Amplitude_Error);
  T->Branch("Hit_Sensor_Cell_HG_Tmax", &Hit_Sensor_Cell_HG_Tmax);
  T->Branch("Hit_Sensor_Cell_HG_Tmax_Error", &Hit_Sensor_Cell_HG_Tmax_Error);
  T->Branch("Hit_Sensor_Cell_HG_Chi2", &Hit_Sensor_Cell_HG_Chi2);
  T->Branch("Hit_Sensor_Cell_HG_Status", &Hit_Sensor_Cell_HG_Status);
  T->Branch("Hit_Sensor_Cell_HG_NCalls", &Hit_Sensor_Cell_HG_NCalls);

  T->Branch("Hit_Sensor_Cell_LG_Amplitude", &Hit_Sensor_Cell_LG_Amplitude);
  T->Branch("Hit_Sensor_Cell_LG_Amplitude_Error", &Hit_Sensor_Cell_LG_Amplitude_Error);
  T->Branch("Hit_Sensor_Cell_LG_Tmax", &Hit_Sensor_Cell_LG_Tmax);
  T->Branch("Hit_Sensor_Cell_LG_Tmax_Error", &Hit_Sensor_Cell_LG_Tmax_Error);
  T->Branch("Hit_Sensor_Cell_LG_Chi2", &Hit_Sensor_Cell_LG_Chi2);
  T->Branch("Hit_Sensor_Cell_LG_Status", &Hit_Sensor_Cell_LG_Status);
  T->Branch("Hit_Sensor_Cell_LG_NCalls", &Hit_Sensor_Cell_LG_NCalls);
'''

EnergyDeposited_LayerHist = []
Canvas = []
histogram_name = "EnergyDeposited_Layer_"
name = "Energy All Layers for Energy " + str(energy) + " GeV"
Total_Energy_Hist = ROOT.TH1F(name,name,100,0,2500)
for iii in range(0,17):
    name = histogram_name + str(iii)
    Histogram = ROOT.TH1F(name, name, 200, 0, 2000)
    EnergyDeposited_LayerHist.append(Histogram)

# creating and array of sums for energies deposited...
sumLayer=[]
for i in range(0,17):
	sumLayer.append(0.0)

check = 0.0
maxEvents = Tree_Input.GetEntries()
vetoCount =0

for event in Tree_Input:
    Count = 0 #Index of the vector
    totalSum=0.0
    EnergySUM_EE_Layers = 0.0
    EnergySUM_FH_Layers = 0.0
    if(check%100 == 0):
        progress = check*100/maxEvents
        sys.stdout.write("\r %d" % progress )
        sys.stdout.flush()

    check +=1


    for Layer in event.Hit_Sensor_Layer:
        skiroc = (event.Hit_Sensor_Skiroc)[Count]
        HG = (event.Hit_Sensor_Cell_HG)[Count]  - (event.Hit_Sensor_Cell_HG_Sub)[Count]
        LG = (event.Hit_Sensor_Cell_LG)[Count] - (event.Hit_Sensor_Cell_LG_Sub)[Count]
        # HG = (event.Hit_Sensor_Cell_HG_Amplitude)[Count]
        # LG = (event.Hit_Sensor_Cell_LG_Amplitude)[Count]
        TOT = (event.Hit_Sensor_Cell_ToT_Slow)[Count]
        Count +=1 # Don't forget this guy.
        # MIP = ADCtoMIPS(HG,LG,TOT,1)
        MIP = ADCtoMIPS(Layer,skiroc,HG,LG,TOT,lines,lines2)
        if (MIP > 2): #NTuple only records MIP > 2
            totalSum += MIP
            sumLayer[Layer] += MIP
            if (Layer < 7):
                EnergySUM_EE_Layers += MIP
            else:
                EnergySUM_FH_Layers += MIP

    if (EnergySUM_EE_Layers >0):
        if (EnergySUM_EE_Layers/(EnergySUM_EE_Layers+EnergySUM_FH_Layers) > 0.98): # Pion veto...
            if totalSum > 50:
                Total_Energy_Hist.Fill(totalSum)
            for i in range(0,17):
                if sumLayer[i]>0 :
                    EnergyDeposited_LayerHist[i].Fill(sumLayer[i])
                sumLayer[i] = 0






print

mini = 100000000000000
selected_FitRangeMin = 0
selected_FitRangeMax = 0
# Try till the most probable value...
# MPV = Total_Energy_Hist.GetBinLowEdge(Total_Energy_Hist.GetMaximumBin())

increment =50
width =200
NDF = {20:16, 32: 20,50:30,80:30,90:30} #Can be optimised dictionary {key:value}
for upperRange in range(100,2500,increment):
    for lowerRange in range(150,upperRange,increment):
        Total_Energy_Hist.Fit("gaus","QM","",lowerRange,upperRange) #,"QM",1000,2250)
        if Total_Energy_Hist.GetFunction("gaus").GetNDF() ==0 or Total_Energy_Hist.GetFunction("gaus").GetNDF() < NDF[energy]:
            continue
        Chi =(Total_Energy_Hist.GetFunction("gaus").GetChisquare()/Total_Energy_Hist.GetFunction("gaus").GetNDF())
        value = abs( Chi- 1 )
        # print str(upperRange)+"\t"+ str(lowerRange) +"\t"+ str(Chi)+"\t"+ str(value) + "\t" + str(Total_Energy_Hist.GetFunction("gaus").GetNDF())
        if value < mini:
            mini = value
            selected_FitRangeMin = lowerRange
            selected_FitRangeMax = upperRange


print "Selected Lower Fit Range is " +str(selected_FitRangeMin)+"\t"+ str(selected_FitRangeMax) + " and correspoding closeness is " + str(mini)

Fit = Total_Energy_Hist.Fit("gaus","QSM","",selected_FitRangeMin,selected_FitRangeMax) #,"QM",1000,2250)
GausMean = Fit.Parameter(1)
GausMeanErr = Fit.ParError(1)
GausSig = Fit.Parameter(2)
GausSigErr = Fit.ParError(2)
MPV = Total_Energy_Hist.GetBinLowEdge(Total_Energy_Hist.GetMaximumBin())
print str(GausMean) + "\t" + str(GausSig)+ "\t" + str(MPV)
filename = "OutputForLinearPlot.txt"
file = open(filename,'a')
outText = str(energy) + "\t"+str(GausMean)+ "\t"+str(GausMeanErr) + "\t" + str(GausSig)+ "\t"+str(GausSigErr)+ "\t" + str(MPV) +"\n"
file.write(outText)
file.close()


print
name = "./Analysed/AllLayer_"+str(energy)+"GeV.png"
Total_Energy_Hist.Draw()
ROOT.gPad.SaveAs(name)


# F_Output = ROOT.TFile(name, "UPDATE") ## To store some histograms from the Tree
for i in range(0,17):
    name = "./Analysed/layer"+str(i)+".png"
    EnergyDeposited_LayerHist[i].Draw()
    ROOT.gPad.SaveAs(name)


# raw_input("Enter to Exit")
