import sharesies
import yfinance
import config
import logic
from datetime import datetime, timedelta


class PortfolioItem:
    def __init__(self, symbol, price, shares):
        self.symbol = symbol
        self.price = price
        self.shares = shares
        self.amount = price * shares
        self.amount *= 0.995 # transaction fee
    
    def get_profit(self, current_price):
        new_amount = current_price * self.shares
        return new_amount - self.amount


# get list of shares
client = sharesies.Client()
client = sharesies.Client()
if client.login(config.username, config.password):
    print('Connected to Sharesies')
else:
    print('Failed to login')
    exit(-1)

companies = client.get_companies()
print('> Retrieved list of shares')

# get their 5 year history
histories = {}
for company in companies:
    symbol = company['code'] + '.NZ'
    stock = yfinance.Ticker(symbol)

    history = stock.history(period='5y', interval='15m')
    history = history.groupby(history.index.date, group_keys=False)

    histories[company['code']] = history

# give yourself $1000
balance = 1000
portfolio = []
print('> Mock portfolio created')

# go from 2017 to 2018 in 30 min intervals
start_date = datetime(year=2017, month=1, day=1)
end_date = datetime(year=2018, month=1, day=1)
interval = timedelta(minutes=30)
print('> Running simulation...')

current_date = start_date
while current_date < end_date:
    # todo: get history up till current date

    # loop through each of the stocks
        # check if it should be bought
            # add to bought stocks
            # reduce from balance
    # loop through inventory
        # check if it should be sold

    pass

print(f'\nNew balance: ${balance}')
print(f'Total returns: {(balance - 1000) / 10}%')