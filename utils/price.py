
from datetime import datetime
import random, pandas as pd

def simulate_price_history(current_price: float, days: int = 60, seed=None):
    if seed is not None:
        random.seed(seed)
    prices = []
    p = current_price * random.uniform(0.92, 1.06)
    for _ in range(days):
        drift = random.uniform(-0.012, 0.012) * p
        p = max(5.0, p + drift)
        if random.random() < 0.05:
            p *= random.uniform(0.9, 0.97)
        prices.append(round(p, 2))
    idx = pd.date_range(end=datetime.today(), periods=days)
    return pd.Series(prices, index=idx)

def buy_or_wait_signal(series, current_price: float):
    last30 = series[-30:]
    min30 = last30.min()
    mean30 = last30.mean()
    slope = (last30.iloc[-1] - last30.iloc[0]) / max(1, len(last30)-1)
    score = 0
    if current_price <= min30 * 1.02:
        score += 2
    if current_price < mean30:
        score += 1
    if slope > 0:
        score -= 1
    else:
        score += 1

    if score >= 2:
        return "BUY", "Current price is at/near recent lows; good time to buy."
    elif score <= 0:
        return "WAIT", "Price trend is flat or rising; likely to drop later."
    else:
        return "CONSIDER", "Decent price; not the lowest, but reasonable."
