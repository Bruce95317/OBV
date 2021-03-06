# This programme use on-balance Volume (OBV) to determien when to buy or sell stocks

# Import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Store the data
df = pd.read_csv('AAPL.csv')
# Set the date to be the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

# Visually shoe the stock price
# plt.figure(figsize=(12.2, 4.5))
# plt.plot(df['Close'], label='Close')
# plt.title('Close Price ')
# plt.xlabel('Date', fontsize=18)
# plt.ylabel('Price USD', fontsize=18)
# plt.show()

# Calcualte the on Blaance Volume (OBV)
OBV = []
OBV.append(0)

# Loop throught the data set (close proce) from the second row (index 1) to the end of the data set
for i in range(1, len(df.Close)):
    if df.Close[i] > df.Close[i-1]:
        OBV.append(OBV[-1]+df.Volume[i])
    elif df.Close[i] < df.Close[i-1]:
        OBV.append(OBV[-1]-df.Volume[i])
    else:
        OBV.append(OBV[-1])

# Store the OBV and OBV Exponential Moving Average (EMA) into new column
df['OBV'] = OBV
df['OBV_EMA'] = df['OBV'].ewm(span=20).mean()


# Create and plot the graph
#plt.figure(figsize=(12.2, 4.5))
#plt.plot(df['OBV'], label='OBV', color='orange')
#plt.plot(df['OBV_EMA'], label='EMA', color='purple')
#plt.title('OBV/OBV EMA Chart')
#plt.xlabel('Date', fontsize=18)
#plt.ylabel('Price USD', fontsize=18)
# plt.show()

# Createa a function ot signal when to buy and sell the stock
# If OBV > OBV_EMA Then Buy
# If OBV < OBV_EMA Then Sell
# Else Do Nothing


def buy_sell(signal, col1, col2):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1


# Loop through the length of the data set
    for i in range(0, len(signal)):
        # If OBV > OBV_EMA Then Buy--> col1 =>'OBV' and col2 => 'OBV_EMA'
        if signal[col1][i] > signal[col2][i] and flag != 1:
            sigPriceBuy.append(signal['Close'][i])
            sigPriceSell.append(np.nan)
            flag = 1
        # If OBV < OBV_EMA Then Sell
        elif signal[col1][i] < signal[col2][i] and flag != 0:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(signal['Close'][i])
            flag = 0
        else:
            sigPriceSell.append(np.nan)
            sigPriceBuy.append(np.nan)

    return(sigPriceBuy, sigPriceSell)


# Create buy and sell columns
x = buy_sell(df, 'OBV', 'OBV_EMA')
df['Buy_Signal_Price'] = x[0]
df['Sell_Signal_Price'] = x[1]

# Plot the buy and sell prices

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label='Close', alpha=0.35)
plt.scatter(df.index, df['Buy_Signal_Price'],
            label='Buy_signal', marker='^', alpha=1, color='green')
plt.scatter(df.index, df['Sell_Signal_Price'],
            label='Sell_signal', marker='v', alpha=1, color='red')
plt.title('Apple Buy and Sell Signal')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Price USD', fontsize=18)
plt.legend(loc='upper left')
plt.show()
