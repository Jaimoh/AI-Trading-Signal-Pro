def generate_signal(price, ema, rsi):

    confidence = 50

    if price > ema:
        confidence += 20
    else:
        confidence -= 20

    if rsi < 30:
        confidence += 25

    elif rsi > 70:
        confidence -= 25

    confidence = max(0, min(100, confidence))

    if confidence >= 70:
        signal = "🟢 BUY"

    elif confidence <= 30:
        signal = "🔴 SELL"

    else:
        signal = "🟡 HOLD"

    return signal, confidence