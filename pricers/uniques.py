from pricers.baseprice import BasePricer, URLS
from utils.cache import cacheable
from refs import credentials
import requests
import time

class UniquePricer(BasePricer):
    raw_key = 'pricer|{}'
    timeout = 15 * 60
    force_save = True

    urls = {
        'uweap': 'UniqueWeapon',
        'uarm': 'UniqueArmour',
        'uacc':' UniqueAccessory',
        'uflask': 'UniqueFlask',
        'ujewel': 'UniqueJewel',
    }

    def __init__(self):
        pass

    def get_values(self, force_skip=False):
        return self.get_raw_values()

    def get_raw_values(self):
        output = {}
        for ckey, nkey in self.urls.items():
            vals = self.get_single_value(nkey, cache_key=self.raw_key.format(ckey))
            for k, v in vals.items():
                output[k] = v
        return output

    @cacheable()
    def get_single_value(self, nkey, cache_key=None):
        r = requests.get(URLS['item'].format(credentials['league'], nkey))
        res = r.json()['lines']
        time.sleep(1)
        return self.parse_single_value(res)

    def parse_single_value(self, raw_values):
        output = {}
        for raw in raw_values:
            output[f'{raw["name"]} {raw["baseType"]}'] = raw['chaosValue']
        return output

if __name__ == '__main__':
    prices = UniquePricer().get_values(force_skip=True)
    pass