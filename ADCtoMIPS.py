result = 0.0


def getAdc2MipBoard(brd2Module_File,calib_File=None):
	brd = []
	ski={}
	for line in brd2Module_File:
		if line.split()[0]!="#":
			brd.append(line.split()[5])


	for line in calib_File:
		if line.split()[0][0]!="#":
			#finding out  which board is this module
			board =0

			for i in range(0,len(brd)):
				if(brd[i] == line.split()[0]):
					board = i
					break
				else:
					print "Didn't find the Board with the module number"
					print "Setting board to 100"
					board=100


			ski[4*board+int(line.split()[1])] = line.split()[2]
			# print str(board)+"\t" + str(int(line.split()[1])) +"\t"+ str(4*int(board) + int(line.split()[1])) + "\t" + line.split()[2]

	return ski






def ADCtoMIPS(a=None, b=None, c=None, d=None,e=None,lines=None,lines2=None,adc2Mip=None):
	if e==None: # hg lg totSlow opt
		# (hg, lg, totSlow, opt)
		ADC_per_Mips  = 50. # in HIGH Gain ADC
		ConvFac_LG2HG = 8.5
		ConvFac_TOT2LG = 2.8 # what we get from beam test
		ConvFac_TOT2LG_Exp =10. # One we expect...
		TP_LG2HG = 1500.
		TP_TOT2LG = 1200.
		hg=a;
		lg=b;
		totSlow=c;
		opt=d
		if opt == 1:
			if float(hg) <= float(TP_LG2HG):
				result=hg/ADC_per_Mips
				return result
			elif float(lg) <= float(TP_TOT2LG):
				result = (lg*ConvFac_LG2HG)/ADC_per_Mips
				return result
			else:
				result = (totSlow*ConvFac_TOT2LG_Exp*ConvFac_LG2HG)/ADC_per_Mips
				return result
		elif opt == 0:
			if float(hg) <= float(TP_LG2HG):
				result=hg/ADC_per_Mips
				return result
			elif float(lg) <= float(TP_TOT2LG):
				result = (lg*ConvFac_LG2HG)/ADC_per_Mips
				return result
			else:
				result = (totSlow*ConvFac_TOT2LG*ConvFac_LG2HG)/ADC_per_Mips
				return result

	if (e!=None and adc2Mip==None) : # board skiroc hg lg totSlow This is where the values are going to be taken from text file... //make sure board start from 0 onwards...
		board = a;
		skiroc = b;
		hg=c;
		lg=d;
		totSlow =e

		adc2Mip  = 0.02 # in HIGH Gain ADC
		ConvFac_LG2HG = 8.5
		ConvFac_TOT2LG = 2.8
		TP_LG2HG = 1500.0
		TP_TOT2LG = 1200.0
		#get 2 and 4 which are the CF and TP
		shift=2 #Adjusting for the new format
		ConvFac_LG2HG=lines[4*board+skiroc].split()[2+shift]
		TP_LG2HG =lines[4*board+skiroc].split()[6+shift]
		ConvFac_TOT2LG =  lines2[4*board+skiroc].split()[2+shift]
		# ConvFac_Intercept_TOT2LG = lines2[4*board+skiroc].split()[4+shift]
		ConvFac_TOT2LG =  3.
		TP_TOT2LG =1200. # lines2[4*board+skiroc].split()[6+shift]
		# print("These are the points for the particular board. \n"+str(ConvFac_LG2HG) + "\n"+str(TP_LG2HG) + "\n"+str(ConvFac_TOT2LG) + "\n"+str(TP_TOT2LG) + "\n")
		# print str(ConvFac_LG2HG) + "\t" +str(TP_LG2HG) + "\t" + str(board)+"\t" + str(skiroc)
		if float(hg) <= float(TP_LG2HG):
			result=float(hg)*float(adc2Mip)
			return result
		elif float(lg) <= float(TP_TOT2LG):
			result = (float(lg)*float(ConvFac_LG2HG))*float(adc2Mip)
			return result
		else:
			result = float(totSlow)*float(ConvFac_TOT2LG)*float(ConvFac_LG2HG)*float(adc2Mip)
			return result
	if (e!=None and adc2Mip!=None) :
			board = a;
			skiroc = b;
			hg=c;
			lg=d;
			totSlow =e

	 		# in HIGH Gain ADC
			ConvFac_LG2HG = 8.5
			ConvFac_TOT2LG = 2.8
			TP_LG2HG = 1500.0
			TP_TOT2LG = 1200.0
			#get 2 and 4 which are the CF and TP
			shift=2 #Adjusting for the new format
			ConvFac_LG2HG=lines[4*board+skiroc].split()[2+shift]
			TP_LG2HG =lines[4*board+skiroc].split()[6+shift]
			ConvFac_TOT2LG =  lines2[4*board+skiroc].split()[2+shift]
			# ConvFac_Intercept_TOT2LG = lines2[4*board+skiroc].split()[4+shift]
			ConvFac_TOT2LG =  10.


			TP_TOT2LG =1200. # lines2[4*board+skiroc].split()[6+shift]
			print hg
			print("These are the points for the particular board. \n"+str(ConvFac_LG2HG) + "\n"+str(TP_LG2HG) + "\n"+str(ConvFac_TOT2LG) + "\n"+str(TP_TOT2LG) + "\n" + str(adc2Mip) + "\n")
			if float(hg) <= float(TP_LG2HG):
				result=float(hg)*float(adc2Mip)
				return result
			elif float(lg) <= float(TP_TOT2LG):
				result = (float(lg)*float(ConvFac_LG2HG))*float(adc2Mip)
				return result
			else:
				result = float(totSlow)*float(ConvFac_TOT2LG)*float(ConvFac_LG2HG)*float(adc2Mip)
				print "hi"
				return result
