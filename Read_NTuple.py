#!/usr/bin/python

from ADCtoMIPS import ADCtoMIPS
import ROOT
import sys
import time

energy = 90
if len(sys.argv) > 1:
    energy = str(sys.argv[1])

F_Input_Name = "/home/rsaradhy/Work/Output/TransitionH_L/New_Data/Oct_NTuple/Electron/"+str(energy)+"GeV.root"
print "Opening File: " + F_Input_Name


F_Input = ROOT.TFile(F_Input_Name)
Tree_Input = F_Input.Get("pulseshapeplotter/T")# The tree is named "T" in the folder "rawhitplotter" for the Input file


# for ADCtoMIPs ...
f=open("Oct_H2_TS3_HG_LG_Datbase.txt")
f2=open("Oct_H2_TS3_LG_TOT_Datbase.txt")
lines=f.readlines()
lines2=f2.readlines()
# ADCtoMIPS(0,0,2700,2500,376,lines,lines2)


# Output folder
F_OutputFolder ="./Analysed/"

#Demo purposes for the function ADCtoMIPS
# print ADCtoMIPS(1,1,10,10,10)


'''
The Branches currently available:-
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

histogram_name = "EnergyDeposited_Layer_"
List_of_Energy_HistogramsOption0 = [] # just an empty array which he will fill....
List_of_Energy_HistogramsOption1 = [] # just an empty array which he will fill....
# Total_Energy_Option0 # just an empty array which he will fill....
# Total_Energy_Option1 # just an empty array which he will fill....



# name = "Total"+histogram_name + "_Option0"
# Total_Energy_Option0= ROOT.TH1F(name, name, 500, 1, 10000)
# name ="Total" + histogram_name +"_Option1"
# Total_Energy_Option1= ROOT.TH1F(name, name, 500, 1, 10000)

name = "Total"+histogram_name + "_Option0"
Total_Energy_Option0= ROOT.TH1F(name, name, 650, 1, 6000)
name ="Total" + histogram_name +"_Option1"
Total_Energy_Option1= ROOT.TH1F(name, name, 650, 1, 6000)

for iii in range(1,18):#17 single sensor layers
	name = histogram_name + str(iii)+"_Option0"
	Histogram = ROOT.TH1F(name, name, 200, 0, 2000)
	List_of_Energy_HistogramsOption0.append(Histogram)
	name = histogram_name + str(iii)+"_Option1"
	Histogram = ROOT.TH1F(name, name, 200, 0, 2000)
	List_of_Energy_HistogramsOption1.append(Histogram)




# creating and array of sums for energies deposited...
sum0=[]
sum1=[]
for i in range(0,17):
	sum0.append(0.0)
	sum1.append(0.0)


check=0
maxEvents = Tree_Input.GetEntries()
CountTimesThorben = 0
# print maxEvents
for event in Tree_Input: #taking the entries in the tree... Here they are events.
	Count = 0 #Index of the vector
	EnergySUM_EE_Layers = 0.0
	EnergySUM_FH_Layers = 0.0
	progress = check*100/maxEvents
	sys.stdout.write("\r %d" % progress )
	sys.stdout.flush()
	# print str(check)
	check +=1
	# print len(event.Hit_Sensor_Layer)
	for Layer in event.Hit_Sensor_Layer: # Note here that there are hit loop number of events.
		HG	= (event.Hit_Sensor_Cell_HG)[Count]
		LG  = (event.Hit_Sensor_Cell_LG)[Count]
		TOT = (event.Hit_Sensor_Cell_ToT_Slow)[Count]
		X  = (event.Hit_Sensor_Cell_X)[Count]
		Y  = (event.Hit_Sensor_Cell_Y)[Count]
		SB_HG =(event.Hit_Sensor_Cell_HG_Sub)[Count]
		SB_LG =(event.Hit_Sensor_Cell_LG_Sub)[Count]
		HG = HG - SB_HG
		LG = LG - SB_LG
        # HG = (event.Hit_Sensor_Cell_HG_Amplitude)[Count]
        # LG = (event.Hit_Sensor_Cell_LG_Amplitude)[Count]
        Count += 1
        MIP0 = ADCtoMIPS(HG,LG,TOT,0)
        # ADCtoMIPS(board,skiroc,HG,LG,TOTSlow,lines,lines2)
        # ADCtoMIPS(HG,LG,TOTSlow,Option)# Option 0 => ConvFac_TOT2LG=2.8 and 1:=>ConvFac_TOT2LG_Exp=10
        # MIP1 = ADCtoMIPS(HG,LG,TOT,1) # Currently Not Used...
        if MIP0 >= 4 :
            if Layer < 7: # For EE layers...
                EnergySUM_EE_Layers += MIP0
            else:
                EnergySUM_FH_Layers += MIP0


	# if ((EnergySUM_EE_Layers+EnergySUM_FH_Layers) > 400 and energy <50) or ((EnergySUM_EE_Layers+EnergySUM_FH_Layers) > 1000 and energy >=50) : # Make sure that there is some deposition happeing...
	if (EnergySUM_EE_Layers+EnergySUM_FH_Layers) > 150 :
		# if EnergySUM_EE_Layers/(EnergySUM_EE_Layers+EnergySUM_FH_Layers) >=.8 : #Thorbens Filling Criteria
			Total_Energy_Option0.Fill(EnergySUM_EE_Layers+EnergySUM_FH_Layers)
			CountTimesThorben+=1




# F_Input.Close()
print
print("Thorben's conditions met this many times :: "+ str(CountTimesThorben))
name = "Opt0_ThorbenCut_Energy_"+str(energy)

F_Output_Name = "./Analysed/all.root"
print "Data saved in :: "+F_Output_Name
F_Output = ROOT.TFile(F_Output_Name, "UPDATE") ## To store some histograms from the Tree
F_Output.cd()

# c1 = ROOT.TCanvas(name,name,1366,768)
# c1.cd()
Total_Energy_Option0.Write(name)

# MeanTE =  Total_Energy_Option0.GetMean()
MeanTE = Total_Energy_Option0.GetBinLowEdge(Total_Energy_Option0.GetMaximumBin())

filename = "LP.txt"
file = open(filename,'a')
outText = str(energy)+"\t" + str(MeanTE)+"\n"  # +"\t"+ str(ModeTE1)
print outText
file.write(outText)
file.close()

#  Pausing Script!!!
# try:
# 	a = input("Enter  to Close")
# except:
# 	print "Closing"
