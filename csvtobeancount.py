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
