import pandas as pd

# A simple script to convert my excel file to be readable by YNAB.
# YNAB wants: Date,Payee,Category,Memo,Outflow,Inflow

__author__ = "Alex Johnstone <alexjj@gmail.com>"

import_csv = 'xacts.csv'

# read csv
df = pd.read_csv(import_csv, encoding = "ISO-8859-1", thousands=',')

# Build YNAB Category
df['Category'] = df['Master Category'] + ":" + df['Sub Category']

# Move column order
df = df[['Date',
 'Payee',
 'Category',
 'Memo',
 'Outflow',
 'Inflow',
 'Account']]

# Change Types
df['Outflow'] = pd.to_numeric(df['Outflow'])
df['Inflow'] = pd.to_numeric(df['Inflow'])
df['Date'] = pd.to_datetime(df['Date'])

# Group by accounts
gb = df.groupby('Account')

#Save csv for each account

for name, group in gb:
    group = group.drop(['Account'], axis=1).set_index('Date')                                  
    csvtosave = name + ".csv"
    group.to_csv(csvtosave, encoding='utf-8')
