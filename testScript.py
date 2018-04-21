#!/usr/bin/python
import ADCtoMIPS as am
import ROOT
import sys
import os
import time

f=open("CalibrationInfo/layerGeom_oct2017_h6_20layers.txt")
a=f.readlines()
f=open("CalibrationInfo/hgcal_calibration.txt")
b=f.readlines()
ski_calib_data = am.getAdc2MipBoard(a,b)


for i in range(0,8):
    print str(i) + "\t" + str(ski[i])
    print
# print brd[6]
