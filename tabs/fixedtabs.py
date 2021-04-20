from tabs.basetab import BaseTab

class FixedTab(BaseTab):
    def parse_raw_values(self, raw_tab):
        try:
            return {val['baseType']: val.get('stackSize', 1) for val in raw_tab}
        except:
            print(raw_tab)
            raise

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

class CurrencyTab(FixedTab):
    tabkey = 'currency'
    cache_key = 'tab|currency'
    timeout = 1 * 60
    force_save = True
    pricer_config = ['curr']

class FragmentTab(FixedTab):
    tabkey = 'frag'
    cache_key = 'tab|frag'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['frag', 'scarab']

class DivinationTab(FixedTab):
    tabkey = 'div'
    cache_key = 'tab|div'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['div']

class EssenceTab(FixedTab):
    tabkey = 'ess'
    cache_key = 'tab|ess'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['ess']

class FossilTab(FixedTab):
    tabkey = 'foss'
    cache_key = 'tab|foss'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['foss']

class BlightTab(FixedTab):
    tabkey = 'bli'
    cache_key = 'tab|bli'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['oil']

class DeliriumTab(FixedTab):
    tabkey = 'bli'
    cache_key = 'tab|bli'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['deli']

class MetamorphTab(FixedTab):
    tabkey = 'meta'
    cache_key = 'tab|meta'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['curr']

if __name__ == '__main__':
    tab = CurrencyTab()
    prices = tab.display_price()
