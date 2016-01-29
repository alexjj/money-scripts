#!/usr/bin/env python 
# must be run via `ledger python <thisfile>.py <journalfile>`

import ledger
import sys

journal = ledger.read_journal(sys.argv[1])

# create a USD commodity
comms = ledger.commodities
usd = comms.find_or_create('$')

# return an amount for the balance
def balance_for_account(acctname):
    account = journal.find_account_re(acctname)
    return balance_posts_subaccts(account)

# recursively determine the balance for all posts/subaccounts in given account
def balance_posts_subaccts(account):
    total = ledger.Balance()
    for post in account.posts():
        total += post.amount
    for subacct in account.accounts():
        total += balance_posts_subaccts(subacct)
    return total

print balance_for_account("Equity:Accounts").value(usd);