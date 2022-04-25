import pandas_datareader as pdr

key = '5f720dfea3e0674ae27e32936cb0f34cebebc46a'

df = pdr.get_data_tiingo('AAPL', api_key=key)
df.to_csv('APPL.csv')

import pandas as pd

df = pd.read_csv('APPL.csv')
df.head()

df.tail()

df1 = df.reset_index()['close']
df1
import matplotlib.pyplot as plt
plt.plot(df1)

