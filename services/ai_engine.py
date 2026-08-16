def generate_signal(price, ema, rsi, upper_band=None, lower_band=None):

    score = 0

    # =================================
    # 1. EMA TREND
    # =================================

    if price > ema:
        score += 1

    elif price < ema:
        score -= 1


    # =================================
    # 2. RSI MOMENTUM
    # =================================

    if 55 <= rsi < 70:
        score += 1

    elif 30 < rsi <= 45:
        score -= 1

    elif rsi <= 30:
        score += 1

    elif rsi >= 70:
        score -= 1


    # =================================
    # 3. BOLLINGER BANDS
    # =================================

    if upper_band is not None and lower_band is not None:

        if price <= lower_band:
            # Price near/below lower band
            score += 1

        elif price >= upper_band:
            # Price near/above upper band
            score -= 1


    # =================================
    # FINAL SIGNAL
    # =================================

    if score >= 2:

        signal = "🟢 BUY"
        confidence = 70

    elif score <= -2:

        signal = "🔴 SELL"
        confidence = 70

    else:

        signal = "🟡 HOLD"
        confidence = 50


    return signal, confidence