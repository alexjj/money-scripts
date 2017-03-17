# Littlefinger

## Overview

This document describes the design for a new money script. It will read the spreadsheet of transactions and then compute various statistics and plot graphs to then send periodically to the owner.

It will mostly be crude and selfish, i.e. it'll just do what I want and no more. Maybe I'll tidy it up one day.

## Outputs

Here is a list of items I'd like it to generate:

### Weekly

* Top 10 expenses that week
* Balance of main accounts
* Week on week change
* Date of last update (or most recent transaction)

### Monthly

* Top 10 (maybe 10 exclusive of rent/mortgage) expenses that month
* Summary of all spending on top level categories year to date
* Table of all spending categories
* Change month on month
* Balance on all accounts

### Quarterly

* Change in net worth

### Yearly

* Summary of all spending
* Change in net worth (plot?)
* Total saved
* Various comparisons against previous year

## Dual Currencies

What should be done with the handling of multiple currencies in the reports.
