from pricers.baseprice import BasePricer

influ_ref = {
    'Shaper': 0,
    'Elder': 1,
    'Crusader': 2,
    'Warlord': 3,
    'Hunter': 4,
    'Redeemer': 5,
}

class ItemBasePricer(BasePricer):
    cache_key = 'pricer|itembase'
    timeout = 60 * 60
    force_save = True
    url_info = ('item', 'BaseType')
    
    def parse_raw_values(self, raw_values):
        output = {}
        for val in raw_values:
            var = val['variant'] or 'normal'
            if '/' in var:
                continue
            basetype = val['baseType']
            ilvl = val['levelRequired']
            infl = var.lower()
            output[f'{basetype}|{ilvl}|{infl}'] = val['chaosValue']
        return output

if __name__ == '__main__':
    prices = ItemBasePricer().get_values(force_skip=True)