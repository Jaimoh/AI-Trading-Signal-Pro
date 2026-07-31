import random
from socket import close

last_close = 1.17500


def get_market_data():
    global last_close

    open_price = last_close

    high_price = round(open_price + random.uniform(0.0001, 0.0010), 5)
    low_price = round(open_price - random.uniform(0.0001, 0.0010), 5)
    close_price = round(random.uniform(low_price, high_price), 5)

    rsi = round(random.uniform(20, 80), 1)

    ema = round(random.uniform(low_price, high_price), 5)

    signal = random.choice([
        "🟢 BUY",
        "🔴 SELL",
        "🟡 HOLD"
    ])

    last_close = close_price

    return (
        round(open_price, 5),
        round(high_price, 5),
        round(low_price, 5),
        round(close_price, 5),
        rsi,
        ema,
        signal      
    )













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

