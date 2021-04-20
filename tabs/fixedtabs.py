from tabs.basetab import FixedTab

class CurrencyTab(FixedTab):
    tabkey = 'currency'
    cache_key = 'tab|currency'
    timeout = 1 * 60
    force_save = True
    pricer_config = ['curr']

class FragmentTab(BaseTab):
    tabkey = 'frag'
    cache_key = 'tab|frag'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['frag', 'scarab']

class DivinationTab(BaseTab):
    tabkey = 'div'
    cache_key = 'tab|div'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['div']

class EssenceTab(BaseTab):
    tabkey = 'ess'
    cache_key = 'tab|ess'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['ess']

class FossilTab(BaseTab):
    tabkey = 'foss'
    cache_key = 'tab|foss'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['foss']

class BlightTab(BaseTab):
    tabkey = 'bli'
    cache_key = 'tab|bli'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['oil']

class DeliriumTab(BaseTab):
    tabkey = 'bli'
    cache_key = 'tab|bli'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['deli']

class MetamorphTab(BaseTab):
    tabkey = 'meta'
    cache_key = 'tab|meta'
    timeout = 1 * 60
    force_on_update = True
    pricer_config = ['curr']

if __name__ == '__main__':
    tab = CurrencyTab()
    prices = tab.display_price()
