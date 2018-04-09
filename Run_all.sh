#!/bin/bash


# Eng=(100 150 200 250 300 350)
Eng=(20 32 50 80 90)

# board=(0 1 2 3 4 5 6 7 8 9 11 14)

plotter="./EngReco.py"

line=9

# rm OutputForLinearPlot.txt
for eng in "${Eng[@]}"
do
  ./$plotter $eng
  # read -p "Press [Enter] key to start Continue..."


done
