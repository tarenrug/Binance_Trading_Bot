import datetime as dt
from binance.client import Client
from RSICalculation import RSICalc
import Keys

def GetHistoricalKlines(Client,Symbol,Timeframe,Datapoints,Historical=0):
    ClosePriceVector=[]
    TimeVector=[]
    VolumeVector=[]
    HighPriceVector=[]
    LowPriceVector=[]

    if Timeframe[1]=="m":
        length = "minutes"
    elif Timeframe[1]=="h":
        length = "hours"
    elif Timeframe[1]=="d":
        length = "days"
    elif Timeframe[1]=="w":
        length = "weeks"
    elif Timeframe[1]=="M":
        length="months"
    else:
        print("Please check the Timeframe Variable is correct")
        return
    for kline in Client.get_historical_klines_generator(Symbol, Timeframe, "{v1} {v2} ago UTC".format(v1=(int(Timeframe[0]))*Datapoints,v2=length),"{v1} {v2} ago UTC".format(v1=Historical, v2=length)):
        kline[0]=dt.datetime.fromtimestamp(kline[0]/1000)
        kline[6]=dt.datetime.fromtimestamp(kline[6]/1000)
        ClosePriceVector.append(float(kline[4])) #Close Price
        TimeVector.append(kline[0])         #Open Time
        VolumeVector.append(kline[5])       #Volume
        HighPriceVector.append(kline[2])
        LowPriceVector.append(kline[3])
            
            #kline columns = [Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, 
            #                 Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore]
    return ClosePriceVector, TimeVector, VolumeVector, HighPriceVector, LowPriceVector

if __name__ == "__main__":
    client=Client(Keys.APIKey,Keys.SecretKey)
    (ClosePriceVector,TimeVector,VolumeVector,HighPriceVector,LowPriceVector) = GetHistoricalKlines(client,"SNGLSETH",client.KLINE_INTERVAL_1DAY,270)
    #print(RSICalc(ClosePriceVector,2))
    print(len(TimeVector))