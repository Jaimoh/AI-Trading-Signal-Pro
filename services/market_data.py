import random
from socket import close

last_close = 1.17500


def get_market_data():
    global last_close

    open_price = last_close

    movement = random.uniform(-0.0030, 0.0030)

    close_price = round(open_price + movement, 5)

    high_price = round(max(open_price, close_price) + 
                       random.uniform(0.0005, 0.0025), 5)
    low_price = round(min(open_price, close_price) - 
                      random.uniform(0.0005, 0.0025), 5)

    


   

    ema = close_price


    signal = random.choice([
        "🟢 BUY",
        "🔴 SELL",
        "🟡 HOLD"
    ])

    last_close = close_price

    return {
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "ema": ema,
        "signal": signal
    }













   # """
    #Simulates downloading market data.
    #Later this will connect to a real broker API.
   # """

   # price = round(random.uniform(1.17000, 1.18000), 5)

   # rsi = round(random.uniform(20, 80), 1)

    #ema = round(random.uniform(1.17000, 1.18000), 5)

   #signal = random.choice([
    #    "🟢 BUY",
    #    "🔴 SELL",
    #    "🟡 HOLD"
    #])

    #return price, rsi, ema, signal

