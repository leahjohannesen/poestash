import requests
import json
from pricing.baseprice import BasePricer
from refs import credentials

# we want to pull these together and cache them as one big entry
class DivPricer(BasePricer):
    cache_key = 'pricing|div'
    cache_time = 60 * 60
    url = 'https://poe.ninja/api/data/ItemOverview?league={}&type=DivinationCard&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['name']: val['chaosValue'] for val in raw_values}

if __name__ == '__main__':
    pricer = DivPricer()
