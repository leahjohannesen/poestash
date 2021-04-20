from utils import cacheable, get_listings
from utils.trade import TradeError
from functools import cached_property
from items.utils import get_base_query
from pricers import Exchange
from datetime import datetime, timedelta

def maybe_create(raw):
    basetype = raw['baseType']
    if 'jewel' in basetype:
        return
    if raw['frameType'] in [1, 2]:
        return CraftBase(raw)
    if raw['frameType'] == 3:
        if not raw.get('identified', False):
            print(f'Identify item: {raw["baseType"]}')
            return
        return Unique(raw)
    return

def valid_chaos(raw):
    try:
        is_rare = raw['frameType'] == 2
        is_ilvl = 60 <= raw['ilvl']
        is_unid = not raw['identified']
    except KeyError:
        return False
    return is_rare and is_ilvl and is_unid

class BaseItem():
    timeout = 8 * 60 * 60
    force_save = False

    def __init__(self, raw_item):
        #item['name'] or 'Nothing', ' - ', item['baseType'], item['frameType']
        self.name = (raw_item['name'] or '-')
        self.type = raw_item['baseType']
        self.ilvl = raw_item['ilvl']
        # get influence
        try:
            self.inf = next(iter(raw_item['influences'].keys()))
        except (KeyError, StopIteration):
            self.inf = 'normal'
        
        # get item type from img url jank af
        split = raw_item['icon'].split('/')
        category = split[6]
        self.iclass = category if category in ['Amulets', 'Rings', 'Belts'] else split[7]

        # store location in tab
        self.loc = (raw_item['x'], raw_item['y'])
        # TODO dimensions
        

    def get_trade_value(self):
        try:
            results = self.get_parsed_listings()
        except TradeError:
            print('Query error, try again')
            return
        srted = sorted(results, key=lambda x: x['price'])
        return ' '.join(f"{res['price']}" for res in srted)

    @cacheable()
    def get_parsed_listings(self):
        results = get_listings(self.query, 15)
        return self.parse_results(results)

    def parse_results(self, results):
        raise NotImplementedError

    @cached_property
    def cache_key(self):
        raise NotImplementedError

    @cached_property
    def formatted_query_name(self):
        raise NotImplementedError

    @cached_property
    def query(self):
        raise NotImplementedError


class CraftBase(BaseItem):
    timeout = 8 * 60 * 60
    force_save = False
    dkey = 'rare'

    def get_nkw(self):
        return self.cache_key

    @cached_property
    def cache_key(self):
        return f'{self.type}|{self.ilvl}|{self.inf}'

    def parse_results(self, results):
        exchange = Exchange().get_rates()
        output = []
        for result in results:
            output.append({'price': int(result['listing']['price']['amount'] * exchange[result['listing']['price']['currency']])})
        return output
    
    @cached_property
    def formatted_query_name(self):
        skips = ['and', 'of', 'to', 'when']
        return ' '.join(blah if blah in skips else blah.capitalize() for blah in self.type.split(' '))

    @cached_property
    def formatted_ilvl(self):
        if self.ilvl < 82:
            return { 'max': 82 }
        if self.ilvl > 86:
            return { 'min': 86 }
        return { 'min': self.ilvl, 'max': self.ilvl }

    @cached_property
    def query(self):
        query = get_base_query()
        query['query']['type'] = self.type
        query['query']['filters'] = {
            "misc_filters": {
                "filters": {
                    "corrupted": { "option": False },
                    "elder_item": { "option": False },
                    "hunter_item": { "option": False },
                    "shaper_item": { "option": False },
                    "warlord_item": { "option": False },
                    "crusader_item": { "option": False },
                    "redeemer_item": { "option": False },
                    "ilvl": self.formatted_ilvl,
                },
            },
        }
        if self.inf != 'normal':
            query['query']['filters']['misc_filters']['filters'][f'{self.inf}_item'] = True
        return query
    
    def __str__(self):
        return self.cache_key

    def __repr__(self):
        return self.cache_key

class Unique(BaseItem):
    timeout = 8 * 60 * 60
    force_save = False
    dkey = 'unique'

    def get_nkw(self):
        return self.cache_key

    @cached_property
    def cache_key(self):
        return f'{self.name} {self.type}'

    def parse_results(self, results):
        exchange = Exchange().get_rates()
        output = []
        for result in results:
            output.append({'price': int(result['listing']['price']['amount'] * exchange[result['listing']['price']['currency']])})
        return output
    
    @cached_property
    def formatted_query_name(self):
        skips = ['and', 'of', 'to', 'when']
        return ' '.join(blah if blah in skips else blah.capitalize() for blah in self.type.split(' '))

    @cached_property
    def query(self):
        return query
    
    def __str__(self):
        return self.cache_key

    def __repr__(self):
        return self.cache_key
    


if __name__ == '__main__':
    gem = SkillGem('a smite')
    qres = get_listings(gem.query)
    gem.show_value()

        