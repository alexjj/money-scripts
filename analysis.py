import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# read Excel
df = pd.read_excel('xacts.xlsx', sheetname='All Transactions')

# Sort types
df['Date'] = pd.to_datetime(df['Date'])
df['Inflow'] = pd.to_numeric(df['Inflow'])
df['Outflow'] = pd.to_numeric(df['Outflow'])
df['Net'] = pd.to_numeric(df['Net'])
df['Net (GBP)'] = pd.to_numeric(df['Net (GBP)'])

# Create Year/Month columns
df['Year'], df['Month'] = df['Date'].dt.year, df['Date'].dt.month

df.head()

table = pd.pivot_table(df,index=["Currency","Master Category","Sub Category"], columns=["Year","Month"], values=["Net"],aggfunc=np.sum,fill_value=0,margins=True)

table.query('Currency == ["GBP"]')
