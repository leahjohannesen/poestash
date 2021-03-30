import requests
from utils.cache import cacheable
from refs import credentials

class BasePricer():
    cache_key = None
    timeout = None
    force_save = None
    url = None

    def __init__(self):
        pass

    @cacheable()
    def get_values(self):
        raw_values = self.get_raw_values()
        return self.parse_raw_values(raw_values)

    def get_raw_values(self):
        r = requests.get(self.url.format(credentials['league']))
        return r.json()['lines']

    def parse_raw_values(self):
        raise NotImplementedError

if __name__ == '__main__':
    pass
