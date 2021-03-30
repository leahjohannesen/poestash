from pricers.baseprice import BasePricer

# we want to pull these together and cache them as one big entry
class CurrencyPricer(BasePricer):
    cache_key = 'pricer|currency'
    timeout = 60 * 60
    force_save = True
    url = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'

    def parse_raw_values(self, raw_values):
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

class FragPricer(BasePricer):
    cache_key = 'pricer|frag'
    timeout = 60 * 60
    force_save = True
    url = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Fragment&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

class DivPricer(BasePricer):
    cache_key = 'pricer|div'
    timeout = 60 * 60
    force_save = True
    url = 'https://poe.ninja/api/data/ItemOverview?league={}&type=DivinationCard&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['name']: val['chaosValue'] for val in raw_values}

class ScarabPricer(BasePricer):
    cache_key = 'pricer|scarab'
    timeout = 60 * 60
    force_save = True
    url = 'https://poe.ninja/api/data/ItemOverview?league={}&type=Scarab&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['name']: val['chaosValue'] for val in raw_values}

if __name__ == '__main__':
    pricer = CurrencyPricer()
    vals = pricer.get_values()