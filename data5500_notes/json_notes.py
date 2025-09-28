'''
This program queries coingecko for ethereum prices in USD
It only runs for one coin, ethereum
The urls require a specific date, and are generated using the datetime timedelta library, to handle things like leap year(s)
The data is written to a csv
'''

import requests
import json
import time
import os
from datetime import datetime, timedelta


# example url for coingecko.com
example_url = "https://api.coingecko.com/api/v3/coins/ethereum/history?date=24-09-2025&localization=false"

# variables to pull coingecko data
key_md = 'market_data'
key_prc = 'current_price'
key_cad = 'cad'
key_gbp = 'gbp'

dt = datetime(2025, 9, 24)
dt_s = dt.strftime('%d-#m-%y')

coin = 'ethereum'

req = requests.get(example_url)

dict_eth_prc = json.loads(req.text)

print(dict_eth_prc[key_md][key_prc][key_cad])
print(dict_eth_prc[key_md][key_prc][key_gbp])
