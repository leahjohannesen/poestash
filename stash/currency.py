from stash.basetab import BaseTab
from utils.cache import cacheable, get_cache

class CurrencyTab(BaseTab):
    tabkey = 'currency'
    cache_key = 'tab|currency'
    timeout = 60 * 60
    force_save = True
    pricer_config = ['curr']

    def parse_raw_values(self, raw_tab):
        return {val['baseType']: val['stackSize'] for val in raw_tab}

    def price_tab(self, skip_cache=False):
        output = []
        prices = self.pricer.get_values()
        tab = self.get_values(skip_cache=skip_cache)
        for item, count in tab.items():
            try:
                ceq = self.pricer.lookup(prices, item)
            except:
                print(f'{self.cache_key} cant price {item}, skipping')
                continue
            output.append((ceq, count, ceq * count, item))
        srted = sorted(output, key=lambda x: x[0], reverse=True)

        return [f'{val[0]:7.1f} | {val[1]:6} | {int(val[2]):6} | {val[3]}' for val in srted]


if __name__ == '__main__':
    tab = CurrencyTab()
    prices = tab.price_tab()