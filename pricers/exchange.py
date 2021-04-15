from utils import cacheable
from pricers.basics import CurrencyPricer

# get this separately since it's essentially our exchange rate

FIX_EXA = 100

class Exchange():
    cache_key = 'exchange'
    timeout = 30 * 60
    force_save = False
    
    def __init__(self):
        pass

    @cacheable()
    def get_rates(self):
        return {
            'exalted': FIX_EXA or CurrencyPricer().get_values()['Exalted Orb'],
            'chaos': 1,
        }

    

if __name__ == '__main__':
    ex = Exchange()
    rates = ex.get_rates()