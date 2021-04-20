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

class FixedTab(BaseTab):
    def parse_raw_values(self, raw_tab):
        return {val['baseType']: val['stackSize'] for val in raw_tab}

    def display_price(self, force_skip=False, debug=False):
        output = []
        prices = self.pricer.get_values()
        tab = self.get_values(force_skip=force_skip)
        for item, count in tab.items():
            try:
                ceq = self.pricer.lookup(prices, item)
            except:
                if debug:
                    print(f'{self.cache_key} cant price {item}, skipping')
                continue
            output.append((ceq, count, ceq * count, item))
        srted = sorted(output, key=lambda x: x[0], reverse=True)
        for val in srted:
            if val[0] <= 1 and val[2] < 20:
                continue
            print(f'{val[0]:7.1f} | {val[1]:6} | {int(val[2]):6} | {val[3]}')

if __name__ == '__main__':
    pass
