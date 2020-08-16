# Programmatic Cryptocurrency Price History Extraction from Kraken

## Overview
This project automates the extraction of cryptocurrency price history from Kraken using Kraken's API based on the Python 
API client `krakenex`.

## Dependencies
### Compatibility
Python 3.6 or higher.

### First set-up
1. Download `virtualenv` if you do not alread have it
```bash
pip install virtualenv
```
2. Create virtual environment in your folder of interest
```bash
virtualenv crypto-extraction
```
3. Activate the virtual environment
```bash
source crypto-extraction/bin/activate
```
4. Install the libraries of interest in the virtual environment based on the `requirements.txt` file
```bash
pip install -r requirements.txt
```

### Re-activate virtual environment every time you need to extract data
```bash
source crypto-extraction/bin/activate
```


## Instructions
### Configuring the input parameters
The configuration of the input parameters is made with the file `config.txt`:
* The time frame for data extraction
* The list of cryptocurrency symbol pairs
* The base currency The base currency

Please examine the file `config.txt` for a concrete example.

### Extract the price history
Once the configuration file is ready, the following command will launch the history extraction:
```bash
python3 extract_history.py
```
Please note that the process can take several hours / days / weeks depending on the number of cryptocurrencies extracted 
and the number of years of history that you want to extract.

## Results
### Output files
Extracted data is saved in the `history_data` folder as `$PAIR_close_price.txt`.

#### Example output format
```
price   volume  time    buy/sell        market/limit    miscellaneous   Since
1.114431        18.07332223     1606777316.4328 b       l               1606777200.0
1.121256        17.96331051     1606777381.7706 b       l               1606777200.0
1.125000        998.40255591    1606777840.5439 b       m               1606777200.0
...
```

## Project Timeline
- Start Date: July 2020
- Completion Date: August 2020
- Maintenance status: Inactive
