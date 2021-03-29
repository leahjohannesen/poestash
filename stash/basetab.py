import requests
import json
import datetime
from utils.cache import Cacherator
from pricing.pricer import Pricer
from refs import tabconfig
from refs import credentials

#https://www.pathofexile.com/character-window/get-stash-items?league=BETRAYAL&tabIndex=5&accountName=PookieRoar

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

def get_cookie(cookie=None):
    #eventually we can maybe get this programmatically until then, hardcode
    #path = '~/Library/Application Support/Google/Chrome/Default/'
    if cookie is None:
        raise NotImplementedError
    else:
        return cookie

class BaseTab():
    tabkey = None
    cache_key = None
    cache_time = None
    force_on_update = False
    url = None

    def __init__(self):
        self.cache = Cacherator(purge=True)
        self.pricer = Pricer()
        self.last_updated = None
        self.tabidx = tabconfig[self.tabkey]
        self.values = None
        self.refresh_values()

    def refresh_values(self):
        try:
            self.values = self.cache.check(self.cache_key, self.cache_time)
            self.last_updated = self.now
            print(f'{self.cache_key} cache hit')
            return
        except KeyError:
            print(f'{self.cache_key} cache miss')
        values = self.get_new_values()
        self.last_updated = self.now
        self.cache.add_value(self.cache_key, values, force=self.force_on_update)
        self.values = values

    def get_new_values(self):
        raw = self.get_raw_tab(**credentials)
        return self.parse_values(raw)

    def get_raw_tab(self, league, acct, uagent, cookie):
        #automoate the cookie getting?
        r = requests.post(self.url.format(league, self.tabidx, acct), headers={'User-Agent': uagent, 'Cookie': 'POESESSID={}'.format(cookie)})
        return r.json()['items']

    def parse_values(self, raw_tab):
        raise NotImplementedError

    @property
    def now(self):
        return int(datetime.datetime.now().timestamp())

    def price_values(self):
        raise NotImplementedError


if __name__ == '__main__':
    tab = BaseTab('currency')
