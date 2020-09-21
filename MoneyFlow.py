from binance.client import Client
from RSICalculation import RSICalc
from HistoricalKlines import GetHistoricalKlines
import Keys
import numpy as np

def MoneyFlowCalc(MFLength,Datapoints,HighPriceVector,LowPriceVector,ClosePriceVector,VolumeVector):

    Variable1=np.array(HighPriceVector,dtype=float)
    Variable2=np.array(LowPriceVector,dtype=float)
    Variable3=np.array(ClosePriceVector,dtype=float)
    Variable4=np.array(VolumeVector,dtype=float)
    hlc3 = (Variable1+Variable2+Variable3)/3
    upper=[]
    lower=[]
    change=[]
    for i in range(len(hlc3)-1):
        change.append(hlc3[i+1]-hlc3[i])
        if change[i]<0:
            upper.append(0)
            lower.append(hlc3[i+1]*Variable4[i+1])
        elif change[i]>0:
            upper.append(hlc3[i+1]*Variable4[i+1])
            lower.append(0)
        elif change[i]==0:
            upper.append(0)
            lower.append(0)

    upper1=[]
    lower1=[]

    for i in range(len(upper)-MFLength+1):
        upper1.append(sum(upper[i:MFLength+i]))
        lower1.append(sum(lower[i:MFLength+i]))
    
    MF = RSICalc(upper1,lower1)
    return MF

if __name__=="__main__":
    client = Client(Keys.APIKey,Keys.SecretKey)
    Symbol="BTCUSDT"
    Timeframe=client.KLINE_INTERVAL_1DAY
    Datapoints=270

    (ClosePriceVector,TimeVector,VolumeVector,HighPriceVector,LowPriceVector)=GetHistoricalKlines(client,Symbol,Timeframe,Datapoints)

    MFLength=12
    MF = MoneyFlowCalc(MFLength,Datapoints,HighPriceVector,LowPriceVector,ClosePriceVector,VolumeVector)
    print(MF)

    