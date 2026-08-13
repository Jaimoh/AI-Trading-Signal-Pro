def generate_signal(price, ema, rsi):

    # --------------------------------
    # STRONG BUY
    # --------------------------------

    if price > ema and 55 <= rsi < 70:

        signal = "🟢 BUY"
        confidence = 80


    # --------------------------------
    # STRONG SELL
    # --------------------------------

    elif price < ema and 30 < rsi <= 45:

        signal = "🔴 SELL"
        confidence = 80


    # --------------------------------
    # OVERSOLD REVERSAL
    # --------------------------------

    elif rsi <= 30 and price > ema:

        signal = "🟢 BUY"
        confidence = 70


    # --------------------------------
    # OVERBOUGHT REVERSAL WARNING
    # --------------------------------

    elif rsi >= 70 and price < ema:

        signal = "🔴 SELL"
        confidence = 70


    # --------------------------------
    # EVERYTHING ELSE
    # --------------------------------

    else:

        signal = "🟡 HOLD"
        confidence = 50


    return signal, confidence