import requests
import json
from trade import MapTraderator
from items import BaseMap
from collections import defaultdict

#https://www.pathofexile.com/character-window/get-stash-items?league=BETRAYAL&tabIndex=5&accountName=PookieRoar

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

def get_cookie(cookie=None):
    #eventually we can maybe get this programmatically until then, hardcode
    #path = '~/Library/Application Support/Google/Chrome/Default/'
    if cookie is None:
        raise NotImplementedError
    else:
        return cookie

class BulkMapTab(object):
    def __init__(self, cookie, acct, league, tabidx):
        self.cookie = cookie
        self.tabidx = tabidx
        self.acct = acct
        self.league = league
        self._raw_tab = self.get_raw_tab()
        self.traderator = MapTraderator()
        self.priced_items = None

    def get_raw_tab(self):
        #automoate the cookie getting?
        r = requests.post(RAW_URL.format(self.league, self.tabidx, self.acct), headers={'Cookie': 'POESESSID={}'.format(self.cookie)})
        rawtab = r.json()['items']
        return sorted(rawtab, key=lambda x: (x['x'], x['y']))

    def process_items(self):
        print('Processing {} items'.format(len(self._raw_tab)))
        itemlist = []
        mapdict = defaultdict(list)
        for i, item_txt in enumerate(self._raw_tab):
            item = BaseMap(item_txt)
            mapdict[str(item)].append(item)
        for mapn, maplist in mapdict.items():
            item = maplist[0]
            price_stuff = self.traderator.get_price_stats(item.item_hash, item.item_query)
            itemtuple = (mapn, len(maplist), price_stuff)
            itemlist.append(itemtuple)
        self.priced_items = itemlist
        print('Pricing finished, writing cache')
        self.traderator.save_cache()

    def display_results(self):
        print('Rough Map Values')
        for iname, ipos, ival in self.priced_items:
                print('{} - {}\n{}\n------'.format(iname, ipos, ival))
        print('Finished')

if __name__ == '__main__':
    with open('teststuff.json', 'r') as f:
        test_stuff = json.load(f)
    test_stuff['tabidx'] = 4
    tab = BulkMapTab(**test_stuff)
    tab.process_items()
    tab.display_results()
