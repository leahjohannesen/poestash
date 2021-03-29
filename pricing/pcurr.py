from pricing.baseprice import BasePricer

# we want to pull these together and cache them as one big entry
class CurrencyPricer(BasePricer):
    cache_key = 'pricing|currency'
    cache_time = 60 * 60
    url = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Currency&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

if __name__ == '__main__':
    curr = CurrencyPricer()
