from pricers.baseprice import BasePricer

BASE_DELAY = 15 * 60

# we want to pull these together and cache them as one big entry
class CurrencyPricer(BasePricer):
    cache_key = 'pricer|currency'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('curr', 'Currency')

    def parse_raw_values(self, raw_values):
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

class FragPricer(BasePricer):
    cache_key = 'pricer|frag'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('curr', 'Fragment')

    def parse_raw_values(self, raw_values):
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

class DivPricer(BasePricer):
    cache_key = 'pricer|div'
    timeout = BASE_DELAY 
    force_save = True
    url_info = ('item', 'DivinationCard')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}

class ScarabPricer(BasePricer):
    cache_key = 'pricer|scarab'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('item', 'Scarab')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}

class EssencePricer(BasePricer):
    cache_key = 'pricer|ess'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('item', 'Essence')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}

class FossilPricer(BasePricer):
    cache_key = 'pricer|foss'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('item', 'Fossil')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}

class OilPricer(BasePricer):
    cache_key = 'pricer|oil'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('item', 'Oil')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}

class DeliPricer(BasePricer):
    cache_key = 'pricer|deli'
    timeout = BASE_DELAY
    force_save = True
    url_info = ('item', 'DeliriumOrb')

    def parse_raw_values(self, raw_values):
        return {val['name']: val['chaosValue'] for val in raw_values}


if __name__ == '__main__':
    pricer = CurrencyPricer()
    vals = pricer.get_values()