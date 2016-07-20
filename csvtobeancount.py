# Convert Citi credit card CSV to beancount structure.
# Todo
'''
Refunds and payments
'''

import csv

citi_csv = 'MC_709_CURRENT_VIEW.CSV'
beancount_account = 'Liabilities:US:Citi'
output_file = 'citi.beancount'

def extract(filename):
    xacts = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                xacts.append([row[1],row[2],row[3]])
        return xacts

'''
beancount format:

YYYY-MM-DD * "Payee"
    Expenses:Category:Subcategory      99.99 USD
    Liabilities:US:Citi
'''
    
    
def make_beancount_string(date, payee, amount):
    # format date to be in beancount format
    bean_date = date.strftime("%Y-%m-%d")
    payee_line = '{} * "{}"'.format(bean_date, payee)
    expense_line = 'Expenses:                     {} USD'.format(amount)
    return payee_line, expense_line
    
def write_beancount_file(output, lines):
    with open(output, 'w') as o:
        o.writelines(lines)



### Probably use pandas

import pandas as pd

citi_csv = 'MC_709_CURRENT_VIEW.CSV'
beancount_account = 'Liabilities:US:Citi'
output_file = 'citi.beancount'

# read csv
df = pd.read_csv(citi_csv, encoding = "ISO-8859-1", thousands=',')

# Drop unnecessary columns

df = df.drop(['Status'], axis=1)

# Remove \n

df['Description'] = df['Description'].str.replace('\n','')

# Move credits to negative debits
df['Debit'] = df['Debit'].convert_objects(convert_numeric=True)
df['Credit'] = df['Credit'].convert_objects(convert_numeric=True)
df.Credit = df.Credit * -1
df['Debit'] = df['Credit'].where(df['Credit']<0,other=df['Debit'])
df = df.drop(['Credit'], axis=1)

# Date format
df['Date'] = df['Date'].convert_objects(convert_dates='coerce')

# Check
print(df)

#xacts = df.values.tolist()
#print(xacts)
