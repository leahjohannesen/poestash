from pricing.baseprice import BasePricer

# we want to pull these together and cache them as one big entry
class FragPricer(BasePricer):
    cache_key = 'pricing|frag'
    cache_time = 60 * 60
    url = 'https://poe.ninja/api/data/CurrencyOverview?league={}&type=Fragment&language=en'

    def get_new_values(self):
        raw_values = self.get_raw_values()
        return {val['currencyTypeName']: val['chaosEquivalent'] for val in raw_values}

if __name__ == '__main__':
    pricer = FragmentPricer()
