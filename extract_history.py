# -*- coding: utf-8 -*-
"""
This script extracts historical trade data for cryptocurrencies traded with a given base currency
from the Kraken database. It fetches data for a specified list of cryptocurrency pairs over a user-defined
time range. The extracted data includes price, volume, timestamp, trade type (buy/sell), order type (market/limit),
and miscellaneous information. Data is saved to text files in the "history_data" directory.

Features:
- Configurable start and end dates, base currency, and list of cryptocurrency pairs via `config.txt`.
- Implements rate limiting and error handling for API calls to Kraken.

Created on: Sun Aug 16 15:28:53 2020

Author: Boris
"""

#### Import built-in and third-party modules and packages ####
import krakenex
import decimal
import time
import datetime
import statistics
import os
####

#### Import home-made modules and packages ####
from utils import *
####

#### Load configuration and initialize variables ####
k = krakenex.API()  # Initialize Kraken API instance
get_info = query_public_info.Query_public_info()  # Custom module for querying public API information

# Configuration variables defined in config.txt
CONFIG_FILE = 'config.txt'
config = {}
with open(CONFIG_FILE, 'r') as f:
    for line in f:
        key, value = line.strip().split('=')
        config[key] = value

# Convert start and end dates from human-readable format to Unix timestamps
START_TIME = config['start_date']
END_TIME = config['end_date']
start_date = time.mktime(datetime.datetime.strptime(START_TIME, "%d/%m/%Y %H:%M:%S").timetuple())
end_date = time.mktime(datetime.datetime.strptime(END_TIME, "%d/%m/%Y %H:%M:%S").timetuple())
####


#### Fetch all available currency pair names from Kraken API ####
all_pairs = get_info.get_all_info_assetPairs()["result"].keys()
####

#### Define base currency and list of cryptocurrencies to extract ####
BASE_CURRENCY = config['base_currency']  # Base currency, e.g. "EUR"
EXTRACT_CRYPTO = config['pairs'].split(',')  # List of cryptocurrency pairs to extract, defined in config
####

# Record the start time of the script
time_start = time.time()

# Loop through all currency pairs to extract data
for pair in all_pairs:

    if BASE_CURRENCY in pair and pair in EXTRACT_CRYPTO:  # Focus only on a list of selected cryptos and one base currency
        print(f"Processing pair: {pair}")
        i = 0  # Counter to track consecutive API calls
        since = start_date
        OHLC_data = 0  # Counter for the number of trades fetched

        # Open a new file to store trade data for the current pair
        with open("history_data/{}_close_price.txt".format(pair), "w") as price_file:
            price_file.write("price\tvolume\ttime\tbuy/sell\tmarket/limit\tmiscellaneous\tSince\n")

        # Fetch data in a loop until the end timestamp is reached
        while int(since)/10**9 < end_date:
            try:
                if i < 20:  # Limit the number of consecutive API calls to avoid rate limits
                    # Fetch trade data from Kraken API
                    extracted_data = k.query_public("Trades", data = {'pair': pair, 'since': since})

                    # Append fetched data to the output file
                    with open("history_data/{}_close_price.txt".format(pair), "a") as price_file:
                        for trade in extracted_data["result"][pair]:
                            price_file.write("{}\t{}\n".format("\t".join([str(i) for i in trade]), since))

                    # Update the number of trades fetched and the 'since' timestamp
                    OHLC_data  += len(extracted_data["result"][pair])
                    since = extracted_data["result"]["last"]

                    # Increment API call counter and pause briefly to avoid hitting rate limits
                    i += 1
                    time.sleep(0.1)
                else:
                    # Reset counter and pause longer to respect Kraken's rate limits
                    i = 0
                    time.sleep(40)
            except Exception as E:
                # Handle exceptions and pause before retrying
                print(f"Exception occurred: {E}")
                time.sleep(20)
        print(f"Total trades fetched for {pair}: {OHLC_data}")
        print(f"Time elapsed for {pair}: {(time.time() - time_start) / 60:.2f} minutes")
