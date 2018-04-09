result = 0.0

def ADCtoMIPS(a=None, b=None, c=None, d=None,e=None,lines=None,lines2=None):
	if e==None: # hg lg totSlow opt
		# (hg, lg, totSlow, opt)
		ADC_per_Mips  = 50 # in HIGH Gain ADC
		ConvFac_LG2HG = 8.5
		ConvFac_TOT2LG = 2.8 # what we get from beam test
		ConvFac_TOT2LG_Exp =10 # One we expect...
		TP_LG2HG = 1500
		TP_TOT2LG = 1200
		hg=a;lg=b;totSlow=c;opt=d
		if opt == 1:
			if hg <= TP_LG2HG:
				result=hg/ADC_per_Mips
				return result
			elif lg <= TP_TOT2LG:
				result = (lg*ConvFac_LG2HG)/ADC_per_Mips
				return result
			else:
				result = (totSlow*ConvFac_TOT2LG_Exp*ConvFac_LG2HG)/ADC_per_Mips
				return result
		elif opt == 0:
			if hg <= TP_LG2HG:
				result=hg/ADC_per_Mips
				return result
			elif lg <= TP_TOT2LG:
				result = (lg*ConvFac_LG2HG)/ADC_per_Mips
				return result
			else:
				result = (totSlow*ConvFac_TOT2LG*ConvFac_LG2HG)/ADC_per_Mips
				return result
	if e!=None: # board skiroc hg lg totSlow This is where the values are going to be taken from text file... //make sure board start from 0 onwards...
		board = a; skiroc = b; hg=c;lg=d;totSlow =e
		ADC_per_Mips  = 50 # in HIGH Gain ADC
		ConvFac_LG2HG = 8.5
		ConvFac_TOT2LG = 2.8
		TP_LG2HG = 1500
		TP_TOT2LG = 1200
		#get 2 and 4 which are the CF and TP
		ConvFac_LG2HG = lines[4*board+skiroc].split()[2]
		TP_LG2HG = lines[4*board+skiroc].split()[6]
		ConvFac_TOT2LG =  lines2[4*board+skiroc].split()[2]
		# ConvFac_Intercept_TOT2LG = lines2[4*board+skiroc].split()[4]
		TP_TOT2LG = lines2[4*board+skiroc].split()[6]
		# print("These are the points for the particular board. \n"+str(ConvFac_LG2HG) + "\n"+str(TP_LG2HG) + "\n"+str(ConvFac_TOT2LG) + "\n"+str(TP_TOT2LG) + "\n")
		if hg <= TP_LG2HG:
			result=hg/ADC_per_Mips
			return result
		elif lg <= TP_TOT2LG:
			result = (lg*ConvFac_LG2HG)/ADC_per_Mips
			return result
		else:
			result = (totSlow*ConvFac_TOT2LG*ConvFac_LG2HG)/ADC_per_Mips
			return result
