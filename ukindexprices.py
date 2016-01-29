"""
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

"""

import requests, bs4, datetime

# List of funds to look up. Tuple as names are never going to change
funds = ('FIAAGY', 
'VVDVWE', 
'VVFUSI',
'MYKAAS', 
'VIUKGO', 
'VIGSCA')

base_url = 'http://www.iii.co.uk/investment/detail?code=mex:'
end_url = '&it=ukut'

ledger_pricedb_file ='/home/alex/money/ledger.pricedb.test'


#Process url via BeautifulSoup
def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

#Make the ledger string

def make_ledger_str(fund, price):
    now = datetime.today()
    timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
    string = "P " + timestamp + " " + fund + 10 * " " + str(price) + " GBP"
    return string



def get_prices():
#Iterate over all funds to generate dictionary of fund and price
    prices = {}
    for fund in funds:
        url = base_url + fund + end_url
        soup = make_soup(url)
        price = soup.select('.price')
        prices[fund] = price
    return prices


    with open (ledger_pricedb_file, 'w') as text_file:
            print(price_string, file=text_file)








if __name__ == "__main__":
    get_prices()