import Keys
from binance.client import Client
import datetime as dt
import time
from RSICalculation import RSICalc
from RSIandStochRSI import RSIandStochRSICalc
from HistoricalKlines import GetHistoricalKlines
from MoneyFlow import MoneyFlowCalc
import Symbols
from AlertsClass import Alerts
import ExtraUsefulCode

if __name__=="__main__":

    tic=time.perf_counter()

    print(dt.datetime.now().strftime("%H:%M:%S - %d/%m/%Y"))
    print("")

    client = Client(Keys.APIKey,Keys.SecretKey)
    count=0
    for pairing in Symbols.FavouriteSymbols:
    #for pairing in ["BCCBTC"]:
        Symbol=pairing
        Timeframe=client.KLINE_INTERVAL_1DAY
        Datapoints=270

        (ClosePriceVector,TimeVector,VolumeVector,HighPriceVector,LowPriceVector)=GetHistoricalKlines(client,Symbol,Timeframe,Datapoints,0)

        if len(ClosePriceVector)==0:
            #print(str(pairing) + " has no data output from the GetHistoricalKlines function.")
            #print("")
            continue

        smoothK=3
        smoothD=4
        LengthRSI=14
        LengthStochRSI=14

        try:
            (RSI,StochRSIK,StochRSID) = RSIandStochRSICalc(smoothK,smoothD,LengthRSI,LengthStochRSI,Datapoints,ClosePriceVector,TimeVector)
        except IndexError:
            #print(str(pairing) + " has an Index Error, can investigate further.")
            #print("")
            continue
        except ZeroDivisionError:
            #print(str(pairing) + " has a Zero Division error, can investigate further.")
            #print("")
            continue

        MFLength=12
        MoneyFlow = MoneyFlowCalc(MFLength,Datapoints,HighPriceVector,LowPriceVector,ClosePriceVector,VolumeVector)

        Alert = Alerts(pairing,Timeframe,RSI,StochRSIK,StochRSID,MoneyFlow)
        if Alert.Buy() == 1 or Alert.Sell() == 1:
            print("For {Tradingpair} at time interval of {Timeinterval}".format(Tradingpair=Symbol, Timeinterval=Timeframe))
            print("Price = "+str(ClosePriceVector[-1]))
            print("RSI = "+str(RSI))
            print("StochRSIK = "+str(StochRSIK))
            print("StochRSID = "+str(StochRSID))
            print("Money Flow = "+str(MoneyFlow))
            print("Time = "+str(TimeVector[-1]))
            print("")
            count+=1
        
    if count==0:
        print("There are no Buy or Sell signals for the given set of parings.")

    toc=time.perf_counter()

    print("Time taken = " + str(toc-tic))



#Maybe seperate RSI - if doesn't take up too much computation
