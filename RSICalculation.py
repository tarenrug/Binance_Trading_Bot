from EMA import EMACalc

def RSICalc(values,timeframe):
    if type(timeframe)==int:
        change=[]
        gain=[]
        loss=[]
        for i in range(len(values)-1):
            change.append(values[i+1]-values[i])
            if change[i] >= 0:
                gain.append(change[i])
                loss.append(0)
            else:
                gain.append(0)
                loss.append((-1)*change[i])
        
        AverageGain = EMACalc(gain,timeframe,1)
        AverageLoss = EMACalc(loss,timeframe,1)

        RS=AverageGain[-1]/AverageLoss[-1]
        RSI = 100-(100/(1+RS))
        return RSI
    elif len(timeframe)>1:
        AverageGain = values
        AverageLoss = timeframe

        RS=AverageGain[-1]/AverageLoss[-1]
        RSI = 100-(100/(1+RS))
        return RSI
    else:
        print("Make sure second arument is either a list or integer for the legnth of the RSI.")

if __name__=="__main__":
    RSI = RSICalc([1,2,3,4,5,15,7,8,20],2)
    print(RSI)