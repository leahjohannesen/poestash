import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import time
from utils.cache import CachedBase
from refs import credentials


NINJA_API = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type={}&language=en'
EXCH_URL = 'https://www.pathofexile.com/api/trade/exchange/Synthesis'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'

# we want to pull these together and cache them as one big entry
class BasePricer(CachedBase):
    cache_key = None
    cache_time = None
    url = None

    def __init__(self):
        super().__init__()
        self.refresh_values()

    def get_raw_values(self):
        r = requests.get(self.url.format(credentials['league']))
        return r.json()['lines']
        
    def lookup(self, key):
        try:
            return self.values[key]
        except:
            if key == 'Chaos Orb':
                return 1
            raise f'Pricing error, key not found: {key}'

if __name__ == '__main__':
    pass
