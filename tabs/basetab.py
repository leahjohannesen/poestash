import requests
import json
import datetime
from pricers import FullPricer
from utils.cache import cacheable
from refs import get_tabconfig, credentials

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

class BaseTab():
    cache_key = None
    timeout = None
    force_save = None
    tabkey = None
    pricer_config = None

    def __init__(self):
        self.pricer = FullPricer(self.pricer_config)
        self.tabidx = get_tabconfig()[self.tabkey]

    @cacheable()
    def get_values(self, force_skip=False):
        raw = self.get_raw_tab(**credentials)
        return self.parse_raw_values(raw)

    def get_raw_tab(self, league, acct, uagent, cookie):
        #automoate the cookie getting?
        r = requests.post(RAW_URL.format(league, self.tabidx, acct), headers={'User-Agent': uagent, 'Cookie': 'POESESSID={}'.format(cookie)})
        return r.json()['items']

    def parse_raw_values(self, raw_tab):
        raise NotImplementedError

    def display_prices(self, force_skip=False):
        raise NotImplementedError
        

if __name__ == '__main__':
    pass
