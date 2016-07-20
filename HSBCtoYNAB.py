import pandas as pd
import numpy as np

# A simple script to convert csv from us.hsbc.com Money Management Tools website to be readable by YNAB.
# YNAB wants: Date,Payee,Category,Memo,Outflow,Inflow

__author__ = "Alex Johnstone <alexjj@gmail.com>"

import_csv = 'ExportData.csv'
#Drop any transaction prior to this date
cutoffdate = '2015-01-01'


df = pd.read_csv(import_csv, encoding = "ISO-8859-1", thousands=',')

#Rename Columns
df = df.rename(columns={'Original Description':'Payee','Amount':'Outflow',})

#Swap payee with simple description if present
df['Payee'] = df['Simple Description'].where(df['Simple Description'].notnull(), other=df['Payee'])

#Delete unneeded columns
df = df.drop(['Status','Split Type','Currency','User Description','Classification','Simple Description'], axis=1)

#Clean up payee
df['Payee'] = df['Payee'].str.replace('PURCHASE - ','')
df['Payee'] = df['Payee'].str.replace('WAL-MART','Walmart')
df['Payee'] = df['Payee'].str.replace('BAKERSFIELD  CA','')

# move positive values in outflow to inflow
df['Outflow'] = df['Outflow'].convert_objects(convert_numeric=True)
df['Date'] = df['Date'].convert_objects(convert_dates='coerce')
df['Inflow'] = df['Outflow'].where(df['Outflow']>0,other=np.nan)

#Remove corresponding outflow value
df.ix[df.Inflow==df.Outflow, 'Outflow'] = np.nan
# Multiply outflows by -1
df.Outflow = df.Outflow * -1

#Move column order
df = df[['Date',
 'Payee',
 'Category',
 'Memo',
 'Outflow',
 'Inflow',
 'Account Name']]

#Filter Dates
df = df[df.Date > cutoffdate]

#Split dataframe by accounts
gb = df.groupby('Account Name')

#Save csv for each account

for name, group in gb:
    group = group.drop(['Account Name'], axis=1).set_index('Date')                                  
    csvtosave = name + ".csv"
    group.to_csv(csvtosave, encoding='utf-8')
