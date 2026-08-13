def generate_signal(price, ema, rsi, upper_band, lower_band):

    # --------------------------------
    # Not enough Bollinger data
    # --------------------------------
    if upper_band is None or lower_band is None:
        return "🟡 HOLD", 50

    # --------------------------------
    # BUY confirmations
    # --------------------------------
    buy_score = 0

    # Price above EMA = bullish trend
    if price > ema:
        buy_score += 1

    # RSI bullish momentum
    if 50 < rsi < 70:
        buy_score += 1

    # Price near/below lower Bollinger Band
    if price <= lower_band:
        buy_score += 1

    # --------------------------------
    # SELL confirmations
    # --------------------------------
    sell_score = 0

    # Price below EMA = bearish trend
    if price < ema:
        sell_score += 1

    # RSI bearish momentum
    if 30 < rsi < 50:
        sell_score += 1

    # Price near/above upper Bollinger Band
    if price >= upper_band:
        sell_score += 1

    # --------------------------------
    # Determine signal
    # --------------------------------
    if buy_score >= 3:

        signal = "🟢 BUY"
        confidence = 90

    elif sell_score >= 3:

        signal = "🔴 SELL"
        confidence = 90

    elif buy_score == 2:

        signal = "🟢 BUY"
        confidence = 70

    elif sell_score == 2:

        signal = "🔴 SELL"
        confidence = 70

    else:

        signal = "🟡 HOLD"
        confidence = 50

    return signal, confidence