import Keys
from binance.client import Client
from RSICalculation import RSICalc
from HistoricalKlines import GetHistoricalKlines
from SMA import SMACalc
import datetime as dt

def RSIandStochRSICalc(smoothK,smoothD,LengthRSI,LengthStochRSI,Datapoints,ClosePriceVector,TimeVector):

    FixedPriceVector=ClosePriceVector
    FixedTimeVector=TimeVector

    StochVector=[]
    Datapoints=len(ClosePriceVector)

    for j in range(2*(smoothK+smoothD)):
        RSIVector=[]
        TimeRSIVector=[]
        for i in range(LengthStochRSI):
            ClosePriceVector=FixedPriceVector[:Datapoints-i-j]
            TimeVector=FixedTimeVector[:Datapoints-i-j]
            RSIVector.append(RSICalc(ClosePriceVector,LengthRSI))
            TimeRSIVector.append(TimeVector[-1])
            if i==0 and j==0:
                RSI=RSIVector[0]
        StochVector.append(100*((RSIVector[0] - min(RSIVector))/(max(RSIVector)-min(RSIVector))))

    FixedStochVector=StochVector
    KVector=[]

    for i in range(smoothK+smoothD):
        K=SMACalc(FixedStochVector[i:],smoothK,1)
        KVector.append(K)

    FixedKVector=KVector
    DVector=[]

    for i in range(smoothD):
        D=SMACalc(FixedKVector[i:],smoothD,1)
        DVector.append(D)

    StochRSIK=KVector[0] #Less smoothing
    StochRSID=DVector[0] #More Smoothing

    return RSI, StochRSIK, StochRSID

if __name__ == "__main__":
    client = Client(Keys.APIKey,Keys.SecretKey)
    Symbol="BTCUSDT"
    Timeframe=client.KLINE_INTERVAL_1DAY
    Datapoints=270

    (ClosePriceVector,TimeVector,VolumeVector,HighPriceVector,LowPriceVector)=GetHistoricalKlines(client,Symbol,Timeframe,Datapoints)
    
    smoothK=3
    smoothD=4
    LengthRSI=14
    LengthStochRSI=14
    (RSI, StochRSI) = RSIandStochRSICalc(smoothK,smoothD,LengthRSI,LengthStochRSI,Datapoints,ClosePriceVector,TimeVector)
    print(RSI)
    print(StochRSI)
