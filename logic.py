import config
import numpy as np

# Example trading logic...
# Update with your own indicators/rules.

def get_changes(data, step):
    normals = []

    for i in range(0, len(data), step):
        periods = data[i:i+step]

        changes = periods[1:]['Close'].values - periods[:-1]['Close'].values
        changes = changes / periods[:-1]['Close'].values * 100

        try:
            avg_change = sum(changes) / len(changes)
        except ZeroDivisionError:
            avg_change = 0

        normals.append(avg_change)
    
    return normals

def get_latest_change(data, step):
    recent = data[-3:]
    changes = get_changes(recent, 3)
    latest = changes[0]

    return latest

def get_dates(data, step):
    dates = []

    for i in range(0, len(data), step):
        dates.append(data.index.values[i])

    return dates

def get_bounds(data):
    mean = sum(data) / len(data)

    totals = [(x - mean) ** 2 for x in data]
    sd = (sum(totals) / len(totals)) ** 0.5

    interval = 0.608 * sd # 25% interval

    lower_bounds = mean - interval
    upper_bounds = mean + interval

    return (lower_bounds, mean, upper_bounds)

def should_buy(price, history, bounds):
    # ignore penny stocks
    if price < 1:
        return False

    latest = get_latest_change(history, 3)

    has_decreased_recently = latest < bounds[0]
    is_increasing_overall = bounds[1] > 0

    return has_decreased_recently and is_increasing_overall

def should_sell(original_price, market_price, history, bounds):
    difference = market_price - original_price
    percent_change = (difference / original_price) * 100

    latest = get_latest_change(history, 3)

    has_reached_loss_margin = percent_change <= config.sell_loss_percent
    has_increased_recently = latest >= bounds[2]

    return has_reached_loss_margin or has_increased_recently
