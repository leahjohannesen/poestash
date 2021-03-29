import requests
import json
import datetime
from pricing import FullPricer
from utils.cache import CachedBase
from refs import tabconfig
from refs import credentials

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

class BaseTab(CachedBase):
    tabkey = None
    pricer_config = None

    def __init__(self):
        super().__init__()
        self.pricer = FullPricer(self.pricer_config)
        self.tabidx = tabconfig[self.tabkey]
        self.refresh_values()

    def get_new_values(self):
        raw = self.get_raw_tab(**credentials)
        return self.parse_values(raw)

    def get_raw_tab(self, league, acct, uagent, cookie):
        #automoate the cookie getting?
        r = requests.post(RAW_URL.format(league, self.tabidx, acct), headers={'User-Agent': uagent, 'Cookie': 'POESESSID={}'.format(cookie)})
        return r.json()['items']

    def parse_values(self, raw_tab):
        raise NotImplementedError

    @property
    def price_values(self):
        raise NotImplementedError


if __name__ == '__main__':
    tab = BaseTab('currency')
