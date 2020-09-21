from SMA import SMACalc

def EMACalc(values,timeframe,switch=0):
    EMA=[]
    fixedvalues=values
    if len(values)>=(timeframe+1):
        SMA = SMACalc(values,timeframe,1)
        values = values[timeframe:]
        if switch == 0:
            alpha = (2/(float(timeframe+1)))
        elif switch == 1:
            alpha = (1/(float(timeframe)))
        else:
            print("Please choose last variable in EMACalc to be either 0 or 1. Default is 0 for EMA and 1 is for RMA")
            return
        for i in range(len(values)):
            if i==0:
                EMA.append((values[i])*alpha+(1-alpha)*SMA)
            else:
                EMA.append((values[i])*alpha+(1-alpha)*EMA[i-1])
        return EMA
    else:
        if switch == 0:
            alpha = (2/(float(timeframe+1)))
        elif switch == 1:
            alpha = (1/(float(timeframe)))
        else:
            print("Please choose last variable in EMACalc to be either 0 or 1. Default is 0 for EMA and 1 is for RMA")
            return
        for i in range(len(values)):
            if i==0:
                EMA.append((values[i])*alpha+(1-alpha)*fixedvalues[0])
            else:
                EMA.append((values[i])*alpha+(1-alpha)*EMA[i-1])
        return EMA

if __name__ == "__main__":
    Values = [22.27340,22.19400,22.08470,22.17410,22.18400,22.13440,22.23370,22.43230,22.24360,22.29330,22.15420,22.39260,22.38160,22.61090,23.35580,
    24.05190,23.75300,23.83240,23.95160,23.63380,23.82250,23.87220,23.65370,23.18700,23.09760,23.32600,22.68050,23.09760,22.40250,22.17250]
    Values=[11,12,14,18,12,15,13,16,10]
    Output = EMACalc(Values,2,0)
    print(Output)