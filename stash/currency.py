from stash.basetab import BaseTab

class CurrencyTab(BaseTab):
    tabkey = 'currency'
    cache_key = 'tab|currency'
    cache_time = 60 * 60
    force_on_update = True

    def parse_values(self, raw_tab):
        return {curr['baseType']: curr['stackSize'] for curr in raw_tab}

    @property
    def price_values(self):
        output = []
        self.refresh_values()
        self.pricer.refresh_values()
        for item, count in self.values.items():
            try:
                ceq = self.pricer.lookup(item)
            except:
                print(f'{self.cache_key} cant price {item}, skipping')
                continue
            output.append((ceq, count, ceq * count, item))
        srted = sorted(output, key=lambda x: x[0], reverse=True)

        return [f'{val[0]:7.1f} | {val[1]:6} | {int(val[2]):6} | {val[3]}' for val in srted]


if __name__ == '__main__':
    tab = CurrencyTab()