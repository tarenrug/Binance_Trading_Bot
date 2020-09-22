from binance.client import Client
import Keys

class Alerts:
    def __init__(self,TradingPair,Timeframe,RSI,StochRSIK,StochRSID,MoneyFlow):
        self.TradingPair = TradingPair
        self.TimeFrame = Timeframe
        self.RSI=RSI
        self.StochRSIK=StochRSIK
        self.StochRSID=StochRSID
        self.MoneyFlow=MoneyFlow

    def Buy(self):
        variablebuy=1
        if self.RSI <= 90 and self.StochRSIK <= 90 and self.MoneyFlow <= 90:
            print("There is an BUY Signal with {v1} on the {v2} chart.".format(v1=self.TradingPair,v2=self.TimeFrame))
        else:
            #print("There are no buy signals with {v1} on the {v2} chart.".format(v1=self.TradingPair,v2=self.TimeFrame))
            variablebuy=2
        return variablebuy

    def Sell(self):
        variablesell=1
        if 80<= self.RSI and 80 <= self.StochRSIK and 80 <= self.MoneyFlow:
            print("There is a SELL Signal with {v1} on the {v2} chart.".format(v1=self.TradingPair,v2=self.TimeFrame))
        else:
            #print("There are no sell signals with {v1} on the {v2} chart.".format(v1=self.TradingPair,v2=self.TimeFrame))
            variablesell=2
        return variablesell

if __name__=="__main__":
    client=Client(Keys.APIKey,Keys.SecretKey)
    BTCUSDT = Alerts("BTCUSDT",client.KLINE_INTERVAL_1DAY,11,22,33,44)

    list1=["ABC","DEF","HIJ"]
    for i in list1:
        Alert = Alerts(i,client.KLINE_INTERVAL_1DAY,11,22,33,44)
        Alert.Buy()





