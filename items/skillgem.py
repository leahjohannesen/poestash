from utils import cacheable, get_listings
from utils.trade import TradeError
from functools import cached_property
from items.utils import get_base_query
from pricers import Exchange
from datetime import datetime, timedelta

class SkillGem():
    option_map = {
        's': {'lookup': '0', 'cache': 'def', 'name': 'default'},
        'a': {'lookup': '1', 'cache': 'ano', 'name': 'anomalous'},
        'd': {'lookup': '2', 'cache': 'div', 'name': 'divergent'},
        'p': {'lookup': '3', 'cache': 'phn', 'name': 'phantasmal'},
    }
    timeout = 8 * 60 * 60
    force_save = False

    def __init__(self, gemstr):
        self.name = gemstr[2:]
        self.qual = gemstr[0]

    def show_value(self):
        try:
            results = self.get_parsed_listings()
        except TradeError:
            print('Query error, try again')
            return
        srted = sorted(results, key=lambda x: x['price'])
        printval = '\n'.join(f"{res['price']:4d}  ::  {res['level']:2d} | {res['qual']:2d}  ::  {res['age']:.2f}" for res in srted)
        print(printval)

    @cacheable()
    def get_parsed_listings(self):
        results = get_listings(self.query)
        return self.parse_results(results)

    def parse_results(self, results):
        exchange = Exchange().get_rates()
        output = []
        for result in results:
            try:
                qual = int(next(prop for prop in result['item']['properties'] if prop['name'] == 'Quality')['values'][0][0][1:-1])
            except StopIteration:
                qual = 0
            output.append({
                'price': int(result['listing']['price']['amount'] * exchange[result['listing']['price']['currency']]),
                'age': (datetime.now() - datetime.fromisoformat(result['listing']['indexed'][:-1])) / timedelta(seconds=60 * 60 * 24),
                'level': int(next(prop for prop in result['item']['properties'] if prop['name'] == 'Level')['values'][0][0].split(' ')[0]),
                'qual': qual, 
            })
        return output


    @cached_property
    def cache_key(self):
        return f'{self.name}|{self.option_map[self.qual]["cache"]}'

    @cached_property
    def formatted_query_name(self):
        skips = ['and', 'of', 'to', 'when']
        return ' '.join(blah if blah in skips else blah.capitalize() for blah in self.name.split(' '))

    @cached_property
    def query(self):
        query = get_base_query()
        query['query']['type'] = self.formatted_query_name
        query['query']['filters'] = {
            "misc_filters": {
                "filters": {
                    "corrupted": { "option": False },
                    "gem_alternate_quality": { 
                        "option": self.option_map[self.qual]['lookup'],
                    },
                },
            },
        }
        return query

    def __str__(self):
        return f'{self.name}|{self.option_map[self.qual]["name"]}'


if __name__ == '__main__':
    gem = SkillGem('a smite')
    qres = get_listings(gem.query)
    gem.show_value()

        