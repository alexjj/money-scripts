import pandas as pd


'''
A simple script to convert transactions from my Citi credit card to beancount format.
It does no smart matching or any magic, purely text manipulation.
I still have to go through and assign expense categories. This may seem lazy (and it is)
but the benefit of looking at each transaction is I understand where my money went.

If I wanted super automagic finance team monkey wrench go!, I'd just use Mint.com

beancount format:

YYYY-MM-DD * "Payee"
    Expenses:Category:Subcategory         99.99 USD
    Liabilities:US:Citi
'''

__author__ = "Alex Johnstone <alexjj@gmail.com>"

citi_csv = 'MC_709_CURRENT_VIEW.CSV'
beancount_account = 'Liabilities:US:Citi'
output_file = 'citi.beancount'
liability_line = '    ' + beancount_account + '\n'

# read csv
df = pd.read_csv(citi_csv, encoding = "ISO-8859-1", thousands=',')

# Drop unnecessary columns

df = df.drop(['Status'], axis=1)

# Remove \n and whitespaces
df['Description'] = df['Description'].str.strip()

# Set types
df['Debit'] = pd.to_numeric(df['Debit'])
df['Credit'] = pd.to_numeric(df['Credit'])
df['Date'] = pd.to_datetime(df['Date'])

# Move credits to negative debits
df.Credit = df.Credit * -1
df['Debit'] = df['Credit'].where(df['Credit']<0,other=df['Debit'])
df = df.drop(['Credit'], axis=1)

with open(output_file, 'w') as o:
    for index, row in df.iterrows():
        payee_line = '{:%Y-%m-%d} * "{}"\n'.format(row['Date'], row['Description'])
        expense_line = '    Expenses: {:>45.2f} USD\n'.format(row['Debit'])
        o.writelines([payee_line, expense_line, liability_line, '\n'])   
