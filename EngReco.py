#!/usr/bin/python
from ADCtoMIPS import ADCtoMIPS
from ADCtoMIPS import getAdc2MipBoard
import ROOT
import sys
import os
import time


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptFit(1110)
energy = 90

if len(sys.argv) > 1:
    energy = int(sys.argv[1])





# For Here
F_Input_Name = "/home/rsaradhy/Work/Output/TransitionH_L/Data/data_27_3_2018/H2/Electron/"+str(energy)+"GeV.root"
# F_Input_Name = "/home/rsaradhy/Work/Output/TransitionH_L/Data/data_27_3_2018/H2/Pion/"+str(energy)+"GeV.root"

# For Zeb
# F_Input_Name = "/local/cms/user/saradhy/public/data/data_27_3_2018/H2/Pion/"+str(energy)+"GeV.root"
# F_Input_Name = "/local/cms/user/saradhy/public/data/data_27_3_2018/H2/Electron/"+str(energy)+"GeV.root"

print "Opening File: " + F_Input_Name
F_Input = ROOT.TFile(F_Input_Name)
Tree_Input = F_Input.Get("pulseshapeplotter/T")#

fitName = 'CrazyValue'
# for ADCtoMIPs ...
f=open("CalibrationInfo/Oct_H2_PFA_HG_LG_Datbase.txt")
# f=open("CalibrationInfo/Oct_H2_TS3_HG_LG_Datbase.txt")
# f=open("CalibrationInfo/Oct_H2_TS3_CM_HG_LG_Datbase.txt")
HG2LG_Calib=f.readlines()
f=open("CalibrationInfo/Final_Oct_H2_PFA_LG_TOT_Datbase.txt")
# f=open("CalibrationInfo/Oct_H2_PFA_LG_TOT_Datbase.txt")
# f=open("CalibrationInfo/Oct_H2_TS3_LG_TOT_Datbase.txt")
# f=open("CalibrationInfo/Oct_H2_TS3_CM_LG_TOT_Datbase.txt")
LG2TOT_Calib=f.readlines()


f=open("CalibrationInfo/layerGeom_oct2017_h2_17layers.txt")
a=f.readlines()
# f=open("CalibrationInfo/TS3_SkirocAverages_MIPs.txt")
f=open("CalibrationInfo/defaultPS_SkirocAverages_MIPs.txt")
b=f.readlines()
ski_calib_data = getAdc2MipBoard(a,b)
sum = 0.0
for i in range(0,len(ski_calib_data)):
    sum += float(ski_calib_data[i])


print sum/len(ski_calib_data)
# # print ADCtoMIPS(0,0,1661.95,1200.1,170,HG2LG_Calib,LG2TOT_Calib,ski_calib_data[0])
# raw_input("enter to continue")


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

name = "Energy All Layers for Energy " + str(energy) + " GeV"

bin = {90:80,80:90,50:110,32:120,20:130}

print bin[energy]
Total_Energy_Hist = ROOT.TH1F(name,name,bin[energy],0,4000)

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

    ii=0
    for Layer in event.Hit_Sensor_Layer:
        skiroc = (event.Hit_Sensor_Skiroc)[Count]
        # HG = (event.Hit_Sensor_Cell_HG)[Count]  - (event.Hit_Sensor_Cell_HG_Sub)[Count]
        # LG = (event.Hit_Sensor_Cell_LG)[Count] - (event.Hit_Sensor_Cell_LG_Sub)[Count]
        HG = (event.Hit_Sensor_Cell_HG_Amplitude)[Count]
        LG = (event.Hit_Sensor_Cell_LG_Amplitude)[Count]
        TOT = (event.Hit_Sensor_Cell_ToT_Slow)[Count]
        Count +=1 # Don't forget this guy.
        # MIP = ADCtoMIPS(HG,LG,TOT,1)
        skiIndex = Layer*4 + skiroc
        MIP = ADCtoMIPS(Layer,skiroc,HG,LG,TOT,HG2LG_Calib,LG2TOT_Calib,ski_calib_data[skiIndex])
        if (MIP > 2): #NTuple only records MIP > 2
            totalSum += MIP
            if (Layer < 7):
                EnergySUM_EE_Layers += MIP
            else:
                EnergySUM_FH_Layers += MIP

    if (EnergySUM_EE_Layers >0.0):
        if (EnergySUM_EE_Layers/(EnergySUM_EE_Layers+EnergySUM_FH_Layers) > 0.92): # Pion veto...
            if totalSum > 50.0:
                if energy > 49:
                    if(totalSum > 500.0):
                        Total_Energy_Hist.Fill(totalSum)
                else:
                    Total_Energy_Hist.Fill(totalSum)






print

MPV = Total_Energy_Hist.GetBinLowEdge(Total_Energy_Hist.GetMaximumBin())+ Total_Energy_Hist.GetBinWidth(Total_Energy_Hist.GetMaximumBin())/2

Fit = Total_Energy_Hist.Fit("gaus","QSM","",MPV-200,MPV + 200) #,"QM",1000,2250)

GausMean = Fit.Parameter(1)
GausMeanErr = Fit.ParError(1)
GausSig = Fit.Parameter(2)
GausSigErr = Fit.ParError(2)
ROOT.gStyle.SetOptFit(0000)
print str(GausMean) + "\t" + str(GausSig)+ "\t" + str(MPV)

filename = "Analysed/OutputForLinearPlot_"+fitName+".txt"
file = open(filename,'a')
outText = fitName + "\t" + str(energy) + "\t"+str(GausMean)+ "\t"+str(GausMeanErr) + "\t" + str(GausSig)+ "\t"+str(GausSigErr)+ "\t" + str(MPV) +"\n"
file.write(outText)
file.close()


print
name = "./Analysed/AllLayer_"+str(energy)+"GeV_"+fitName+".png"
Total_Energy_Hist.Draw()
Total_Energy_Hist.GetYaxis().SetTitle("Counts");
Total_Energy_Hist.GetXaxis().SetTitle("Energy Deposited in All Layers(MIPS)");
ROOT.gPad.SaveAs(name)

# raw_input("Enter to exit")
