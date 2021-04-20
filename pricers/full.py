from pricers.basics import CurrencyPricer, FragPricer, ScarabPricer, \
    DivPricer, EssencePricer, FossilPricer, OilPricer, DeliPricer
from pricers.uniques import UniquePricer
from utils.cache import cacheable
from refs import credentials
from functools import reduce

# we want to pull these together and cache them as one big entry
class FullPricer():
    refs = {
        'curr': CurrencyPricer,
        'frag': FragPricer,
        'scarab': ScarabPricer,
        'div': DivPricer,
        'ess': EssencePricer,
        'foss': FossilPricer,
        'oil': OilPricer,
        'deli': DeliPricer,
        'unique': UniquePricer,
    }
    def __init__(self, pricer_keys):
        self.pricers = {key: self.refs[key]() for key in pricer_keys}

    def get_values(self):
        return reduce(lambda x, y: {**x, **y}, [pricer.get_values() for pricer in self.pricers.values()])

    def lookup(self, values, key):
        try:
            return values[key]
        except:
            if key == 'Chaos Orb':
                return 1
            raise f'Pricing error, key not found: {key}'

if __name__ == '__main__':
    pricers = FullPricer(['curr'])
