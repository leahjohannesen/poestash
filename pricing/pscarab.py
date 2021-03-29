import requests
import json
from pricing.baseprice import BasePricer
from refs import credentials

# we want to pull these together and cache them as one big entry
class ScarabPricer(BasePricer):
    cache_key = 'pricing|scarab'
    cache_time = 60 * 60
    url = 'https://poe.ninja/api/data/ItemOverview?league={}&type=Scarab&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['name']: val['chaosValue'] for val in raw_values}

if __name__ == '__main__':
    pricer = ScarabPricer()
