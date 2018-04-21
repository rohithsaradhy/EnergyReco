#!/bin/bash

adcFile="ADCtoMIPS.py"
energyFile="EngReco.py"
for i in {3..20}
do
sed -i '115s/.*/'"			ConvFac_TOT2LG =  "$i"."'/' $adcFile
sed -i '146s/.*/'"fitName = 'CF"$i"'"'/' $energyFile
sed -i '7s/.*/'"fitName = 'CF"$i"'"'/' plotRes.py
sed -i '6s/.*/'"fitName = 'CF"$i"'"'/' plotLP.py

./Run_all.sh
./plotLP.py
./plotRes.py


read -p "Press [Enter] key to start Continue..."
done
