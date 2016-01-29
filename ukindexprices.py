'''
Index fund scraper.

This python script will take a list of funds and look up their price from iii.co.uk,
then write them to a pricesdb file for ledger-cli's usage.

Process:
For each fund in a list/tuple:

Go to iii.co.uk website, find the span class=price and get the value
Append to ledger.pricedb in format:
P date {y}-{m}-{d} {hh}:{mm}:{ss} fund   price GBP

Run cron daily/weekly/monthly

python ukfundprices.py
'''

#TODO
'''
Use selenium or maybe phantom.js

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://www.iii.co.uk/investment/detail?code=mex:VIUKGO&it=ukut')
price = browser.find_element_by_class_name('price').text
#print(elem.text)
print(price)
browser.quit()

'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime

# List of funds to look up. Tuple as names are never going to change
funds = ('FIAAGY',
         'VVDVWE',
         'VVFUSI',
         'MYKAAS',
         'VIUKGO',
         'VIGSCA')

base_url = 'http://www.iii.co.uk/investment/detail?code=mex:'
end_url = '&it=ukut'

ledger_pricedb_file = '/home/alex/money/ledger.pricedb.test'


# Make the ledger string

def make_ledger_str(fund, price):
    now = datetime.today()
    timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
    string = "P " + timestamp + " " + fund + 10 * " " + str(price) + " GBP"
    return string


def get_prices():
    price_list = []
    for fund in funds:
        url = requests.get(base_url + fund + end_url)
        soup = BeautifulSoup(url.text, "lxml")
        prices_span = soup.select('.price')
        string = make_ledger_str(fund, prices_span[0].gettext())
        price_list.append(string)
    return price_list


def write_prices(price_list):
    with open(ledger_pricedb_file, 'a') as text_file:
        for string in price_list:
            print(string, file=text_file)




if __name__ == "__main__":
    price_list = get_prices()
    write_prices(price_list)


