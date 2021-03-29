import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import time
from utils.cache import Cacherator
from refs import credentials


CURR_API = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'
EXCH_URL = 'https://www.pathofexile.com/api/trade/exchange/Synthesis'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'

# we want to pull these together and cache them as one big entry
class Pricer(object):
    cache_key = 'pricing|currency'
    cache_time = 60 * 60

    def __init__(self):
        self.cache = Cacherator()
        self.values = None
        self.refresh_values()

    def refresh_values(self):
        try:
            self.values = self.cache.check(self.cache_key, self.cache_time)
            print(f'{self.cache_key} cache hit')
            return
        except KeyError:
            print(f'{self.cache_key} cache miss')
        values = self.get_new_values()
        self.cache.add_value(self.cache_key, values, force=True)
        self.values = values

    def get_new_values(self):
        raw_values = self.get_raw_tab()
        return {curr['currencyTypeName']: curr['chaosEquivalent'] for curr in raw_values}

    def get_raw_tab(self):
        r = requests.get(CURR_API.format(credentials['league']))
        return r.json()['lines']
        
    def lookup(self, key):
        try:
            return self.values[key]
        except:
            if key == 'Chaos Orb':
                return 1
            raise f'Pricing error, key not found: {key}'

if __name__ == '__main__':
    curr = Currencyerator(config)
