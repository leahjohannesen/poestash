import requests
import json
import os
import datetime
import time
from pricing import CurrencyPricer, FragPricer, ScarabPricer, DivPricer
from utils.cache import CachedBase
from refs import credentials
from functools import reduce

# we want to pull these together and cache them as one big entry
class FullPricer():
    refs = {
        'curr': CurrencyPricer,
        'frag': FragPricer,
        'scarab': ScarabPricer,
        'div': DivPricer,
    }
    def __init__(self, pricer_keys):
        self.pricers = {key: self.refs[key]() for key in pricer_keys}
        self.values = None
        self.refresh_values()

    def refresh_values(self):
        for pricer in self.pricers.values():
            pricer.refresh_values() 
        self.values = reduce(lambda x, y: {**x, **y}, [pricer.values for pricer in self.pricers.values()])

    def lookup(self, key):
        try:
            return self.values[key]
        except:
            if key == 'Chaos Orb':
                return 1
            raise f'Pricing error, key not found: {key}'

if __name__ == '__main__':
    pricers = FullPricer(['curr', 'frag'])
