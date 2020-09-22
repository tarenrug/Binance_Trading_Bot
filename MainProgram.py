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
    
    LiveTrades=1
    #LiveTrades: OFF = 0 or ON = 1
    #change line 89 and 91 to create_order (also be careful with the except condition - line 91 - this will execute an order of 1000*(stepSize))

    tic=time.perf_counter()

    print(dt.datetime.now().strftime("%H:%M:%S - %d/%m/%Y"))
    print("")

    client = Client(Keys.APIKey,Keys.SecretKey)

    info = client.get_account()
    key=[]
    values=[]
    for i in range(len(info['balances'])):
        if float(info['balances'][i]['free']) > 0:
            key.append(info['balances'][i]['asset'])
            values.append(float(info['balances'][i]['free']))
    AccountBalance = {key[j]: values[j] for j in range(len(key))}
    print(AccountBalance)

    count=0
    for pairing in Symbols.FavouriteSymbols:
    #for pairing in ["BTCUSDT"]:
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
        BuyVariable = Alert.Buy()
        SellVarible = Alert.Sell()

        if BuyVariable == 1 or SellVarible == 1:
            print("For {Tradingpair} at time interval of {Timeinterval}".format(Tradingpair=Symbol, Timeinterval=Timeframe))
            print("Price = "+str(ClosePriceVector[-1]))
            print("RSI = "+str(RSI))
            print("StochRSIK = "+str(StochRSIK))
            print("StochRSID = "+str(StochRSID))
            print("Money Flow = "+str(MoneyFlow))
            print("Time = "+str(TimeVector[-1]))
            print("")
            if BuyVariable==1 and  LiveTrades==1:
                for i in key:
                    if i==Symbol[:len(i)]:
                        print("Buy Order Placed")
                        try:
                            order = client.create_test_order(symbol=Symbol,side=Client.SIDE_BUY,type=client.ORDER_TYPE_MARKET,quantity=ExtraUsefulCode.quantity(Symbol[:len(i)],Symbol,client))
                            print("Quantity being bought: "+ExtraUsefulCode.quantity(Symbol[:len(i)],Symbol,client))
                        except:
                            order = client.create_test_order(symbol=Symbol,side=Client.SIDE_BUY,type=client.ORDER_TYPE_MARKET,quantity=1000*float(client.get_symbol_info(symbol=Symbol)['filters'][2]['stepSize']))
                            print("Quantity being bought: "+1000*float(client.get_symbol_info(symbol=Symbol)['filters'][2]['stepSize']))
                        print(order)
            if SellVarible == 1 and LiveTrades==1:
                for i in key:
                    if i==Symbol[:len(i)]:
                        print("Sell Order Placed")
                        try:
                            order = client.create_test_order(symbol=Symbol,side=Client.SIDE_SELL,type=client.ORDER_TYPE_MARKET,quantity=ExtraUsefulCode.quantity(Symbol[:len(i)],Symbol,client))
                            print("Quantity being sold: "+ExtraUsefulCode.quantity(Symbol[:len(i)],Symbol,client))
                        except:
                            order = client.create_test_order(symbol=Symbol,side=Client.SIDE_SELL,type=client.ORDER_TYPE_MARKET,quantity=1000*float(client.get_symbol_info(symbol=Symbol)['filters'][2]['stepSize']))
                            print("Quantity being sold: "+1000*float(client.get_symbol_info(symbol=Symbol)['filters'][2]['stepSize']))
                        print(order)
            count+=1

    if count==0:
        print("There are no Buy or Sell signals for the given set of parings.")

    toc=time.perf_counter()

    print("Time taken = " + str(toc-tic))



#Maybe seperate RSI - if doesn't take up too much computation
