from tabs.basetab import BaseTab

class DivinationTab(BaseTab):
    tabkey = 'div'
    cache_key = 'tab|div'
    timeout = 60 * 60
    force_on_update = True
    pricer_config = ['div']

    def parse_raw_values(self, raw_tab):
        return {val['baseType']: val['stackSize'] for val in raw_tab}

    def display_price(self, force_skip=False, debug=False):
        output = []
        prices = self.pricer.get_values()
        tab = self.get_values(force_skip=force_skip)
        for item, count in tab.items():
            try:
                ceq = self.pricer.lookup(prices, item)
            except:
                if debug:
                    print(f'{self.cache_key} cant price {item}, skipping')
                continue
            output.append((ceq, count, ceq * count, item))
        srted = sorted(output, key=lambda x: x[0], reverse=True)
        for val in srted:
            if val[0] <= 1 and val[2] < 20:
                continue
            print(f'{val[0]:7.1f} | {val[1]:6} | {int(val[2]):6} | {val[3]}')


if __name__ == '__main__':
    tab = DivinationTab()