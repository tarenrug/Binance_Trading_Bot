import datetime as dt
import math

def CurrentPrice(symbol,Client):
    count=0
    key=[]
    values=[]
    for i in Client.get_all_tickers():
        key.append(i["symbol"])
        values.append(count)
        count += 1
    pricedict = {key[j]: values[j] for j in range(len(key))}
    for j in symbol:
        price = Client.get_all_tickers()[pricedict[j]]
        print(str(price)+" @Time: "+ str(dt.datetime.now().strftime("%H:%M:%S")))

def AllSymbols(Client):
    count=0
    Symbol=[]
    for i in Client.get_all_tickers():
        Symbol.append(i["symbol"])
    return Symbol

def quantity(asset,symbol,Client):
    balance = Client.get_asset_balance(asset=asset)
    step_size =float(Client.get_symbol_info(symbol=symbol)['filters'][2]['stepSize'])
    quantity = (float(balance['free']))*0.01
    precision = int(round(-math.log(step_size, 10), 0))
    quantity = float(round(quantity, precision))
    return quantity
