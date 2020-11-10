import config
import numpy as np

# Example trading logic...
# Update with your own indicators/rules.

def get_latest_rsi(df):
    np.seterr(divide='ignore', invalid='ignore')

    try:
        periods = df[-14:]

        # calculate the daily percent price changes
        changes = periods[1:].Close.values - periods[0:13].Close.values
        changes = changes / periods[0:13].Close.values * 100

        # seperate percent changes into gains and loses
        gains = [change for change in changes if change >= 0]
        loses = [change for change in changes if change < 0]

        # average the gains and loses
        average_gain = sum(gains) / len(gains)
        average_loses = sum(gains) / len(loses)

        # calculate RS and RSI
        rs = average_gain / abs(average_loses)
        rsi = 100 - (100 / (1 + rs))

        return rsi
    except Exception:
        return 50 # default

def should_buy(price, history):
    # ignore penny stocks
    if price < 1:
        return False
    
    # buy if RSI indicates oversold
    rsi = get_latest_rsi(history)
    return rsi <= 35

def should_sell(original_price, market_price):
    ''' Decides if the bot should sell or not '''

    difference = market_price - original_price
    percent_change = (difference / original_price) * 100

    profit_margin = percent_change >= config.sell_profit_percent
    loss_margin = percent_change <= config.sell_loss_percent

    # sell if either of the margins are reached
    return profit_margin or loss_margin
