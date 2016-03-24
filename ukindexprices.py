#!/usr/bin/python
import datetime
from selenium import webdriver
from time import sleep

'''
Index fund scraper.

This python script will take a list of funds and look up their price from
iii.co.uk, then write them to a pricesdb file for ledger-cli's usage.

Run cron daily/weekly/monthly

python ukfundprices.py
'''
__author__ = "Alex Johnstone <alexjj@gmail.com>"

# List of funds to look up.
funds = ('FIAAGY',
         'VVDVWE',
         'VVFUSI',
         'MYKAAS',
         'VIUKGO',
         'VIGSCA',
         'VVUILG')

# FIAAGY and MYKAAS prices are in p
penny_funds = ('FIAAGY', 'MYKAAS')

base_url = 'http://www.iii.co.uk/investment/detail?code=mex:'
end_url = '&it=ukut'

pricedb_file = '/home/alex/money/prices.beancount'

# ledger or beancount

program = 'beancount'
#program = 'ledger'

# Make the ledger string

def make_ledger_str(fund, price):
    now = datetime.datetime.today()

    if program == 'ledger':
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
        string = "P {} {}                            {} GBP".format(timestamp, fund, price)
    elif program == 'beancount':
        timestamp = now.strftime("%Y-%m-%d")
        string = "{} price {}                            {} GBP".format(timestamp, fund, price)
    else:
        print("Only ledger or beancount")
        quit()
    return string


def get_prices():
    price_list = []
    for fund in funds:
        browser = webdriver.PhantomJS()
        browser.get(base_url + fund + end_url)
        price = browser.find_element_by_class_name('price').text
        if fund in penny_funds:
            price = float(price) / 100
        string = make_ledger_str(fund, price)
        price_list.append(string)
        browser.quit()
        sleep(1)  # Kept getting connection refused
    return price_list


def write_prices(price_list):
    with open(pricedb_file, 'a') as text_file:
        for string in price_list:
            print(string, file=text_file)


if __name__ == "__main__":
    price_list = get_prices()
    write_prices(price_list)
