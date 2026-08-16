def generate_signal(price, ema, rsi, upper_band=None, lower_band=None):

    # --------------------------------
    # STRONG BUY
    # --------------------------------
    if (
        price > ema
        and 55 <= rsi < 70
        and (upper_band is None or price < upper_band)
    ):
        signal = "🟢 BUY"
        confidence = 80

    # --------------------------------
    # STRONG SELL
    # --------------------------------
    elif (
        price < ema
        and 30 < rsi <= 45
        and (lower_band is None or price > lower_band)
    ):
        signal = "🔴 SELL"
        confidence = 80

    # --------------------------------
    # OVERSOLD REVERSAL
    # --------------------------------
    elif (
        rsi <= 30
        and price > ema
        and (lower_band is None or price <= lower_band * 1.01)
    ):
        signal = "🟢 BUY"
        confidence = 75

    # --------------------------------
    # OVERBOUGHT WARNING
    # --------------------------------
    elif (
        rsi >= 70
        and price < ema
        and (upper_band is None or price >= upper_band * 0.99)
    ):
        signal = "🔴 SELL"
        confidence = 75

    # --------------------------------
    # TREND BUY
    # --------------------------------
    elif price > ema and rsi >= 50:
        signal = "🟢 BUY"
        confidence = 70

    # --------------------------------
    # TREND SELL
    # --------------------------------
    elif price < ema and rsi <= 50:
        signal = "🔴 SELL"
        confidence = 70

    # --------------------------------
    # EVERYTHING ELSE
    # --------------------------------
    else:
        signal = "🟡 HOLD"
        confidence = 50

    return signal, confidence