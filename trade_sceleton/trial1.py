import MetaTrader5 as mt
import pandas as pd
import plotly.express as px
from datetime import datetime

#start the platform
mt.initialize()

login = 5002528742
password = "rrh4ddlp"
server = "MetaQuotes-Demo"

mt.login(login, password, server)

account_info = mt.account_info()
print(account_info)

login_number = account_info.login
balance = account_info.balance
equity = account_info.equity

print()
print('login: ', login_number)
print('balance: ', balance)
print('equity: ', equity)

#Get number of symbols with symbols_total()
num_symbols = mt.symbols_total()
num_symbols

#Get all symbols and their specifications
symbols = mt.symbols_get()
symbols

#Get symbol specifications
symbol_info = mt.symbol_info("EURUSD")._asdict()
symbol_info

#Get current symbol price
symbol_price = mt.symbol_info_tick("EURUSD")._asdict()
symbol_price

#ohlc_data
ohlc_data = pd.DataFrame(mt.copy_rates_range("EURUSD", mt.TIMEFRAME_D1, datetime(2021, 1, 1), datetime.now()))

fig = px.line(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
fig.show()

ohlc_data

#Requesting tick data
tick_data = pd.DataFrame(mt.copy_ticks_range("EURUSD", datetime(2021, 10, 4), datetime.now(), mt.COPY_TICKS_ALL))

fig = px.line(tick_data, x=tick_data['time'], y=tick_data['close'])
fig.show()

tick_data

#Total number of orders
num_orders = mt.orders_total()
num_orders

#Lsit of orders
orders = mt.orders_get()
orders

#Total number of positions
num_positions = mt.positions_total()
num_positions

positions = mt.positions_get()
positions

num_order_history = mt.history_orders_total(datetime(2021, 1, 1), datetime.now())
num_order_history

order_history = mt.history_orders_get(datetime(2021, 1, 1), datetime(2021, 10, 6))
order_history

num_deal_history = mt.history_deals_total(datetime(2021, 1, 1), datetime.now())
num_deal_history

deal_history = mt.history_deals_get(datetime(2021, 1, 1), datetime.now())
deal_history




#Send order to teh market
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": "EURUSD",
    "volume": 2.0, #Float
    "type": mt.ORDER_TYPE_BUY,
    "price": mt.symbol_info_tick("EURUSD").ask,
    "sl": 0.0, #Float
    "tp": 0.0, #Float
    "deviation": 20, #Integer
    "magic": 234000, #Integer
    "comment": "python script open",
    "type_time":mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)

#Close position
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": "EURUSD",
    "volume": 1.0, #Float
    "type": mt.ORDER_TYPE_SELL,
    "price": mt.symbol_info_tick("EURUSD").ask,
    "sl": 0.0, #Float
    "tp": 0.0, #Float
    "deviation": 20, #Integer
    "magic": 234000, #Integer
    "comment": "python script open",
    "type_time":mt.ORDER_TIME_GTC,
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)

