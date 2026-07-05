import random


def get_market_data():
    """
    Simulates downloading market data.
    Later this will connect to a real broker API.
    """

    price = round(random.uniform(1.17000, 1.18000), 5)

    rsi = round(random.uniform(20, 80), 1)

    ema = round(random.uniform(1.17000, 1.18000), 5)

    signal = random.choice([
        "🟢 BUY",
        "🔴 SELL",
        "🟡 HOLD"
    ])

    return price, rsi, ema, signal