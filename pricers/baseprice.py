import requests
from utils.cache import cacheable
from refs import credentials

URLS = {
    'curr': 'https://poe.ninja/api/data/CurrencyOverview?league={}&type={}&language=en',
    'item': 'https://poe.ninja/api/data/ItemOverview?league={}&type={}&language=en',
}

class BasePricer():
    cache_key = None
    timeout = None
    force_save = None
    url_info = None

    def __init__(self):
        pass

    @cacheable()
    def get_values(self, force_skip=False):
        raw_values = self.get_raw_values()
        return self.parse_raw_values(raw_values)

    def get_raw_values(self):
        url = URLS[self.url_info[0]]
        r = requests.get(url.format(credentials['league'], self.url_info[1]))
        return r.json()['lines']

    def parse_raw_values(self, raw_values):
        raise NotImplementedError

if __name__ == '__main__':
    pass
