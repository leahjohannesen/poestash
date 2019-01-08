import requests
import json
from trade import Traderator
from items import BaseItem

#https://www.pathofexile.com/character-window/get-stash-items?league=BETRAYAL&tabIndex=5&accountName=PookieRoar

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

def get_cookie(cookie=None):
    #eventually we can maybe get this programmatically until then, hardcode
    #path = '~/Library/Application Support/Google/Chrome/Default/'
    if cookie is None:
        raise NotImplementedError
    else:
        return cookie

class BulkTab(object):
    def __init__(self, cookie, acct, league, tabidx):
        self.cookie = cookie
        self.tabidx = tabidx
        self.acct = acct
        self.league = league
        self._raw_tab = self.get_raw_tab()
        self.traderator = Traderator()
        self.priced_items = None

    def get_raw_tab(self):
        #automoate the cookie getting?
        r = requests.post(RAW_URL.format(self.league, self.tabidx, self.acct), headers={'Cookie': 'POESESSID={}'.format(self.cookie)})
        return r.json()['items']

    def process_items(self):
        print('Processing {} items'.format(len(self._raw_tab)))
        itemlist = []
        for i, item_txt in enumerate(self._raw_tab):
            if i % 10 == 0:
                self.traderator.save_cache()
            item = BaseItem.get_item_cls(item_txt)
            #quick skip for not implemented
            if item is None:
                continue
            print('Found item - {}'.format(item))
            price_stuff = self.traderator.get_price_stats(item.item_hash, item.item_query)
            itemtuple = (str(item), item.position, price_stuff)
            itemlist.append(itemtuple)
        self.priced_items = itemlist
        print('Pricing finished, writing cache')
        self.traderator.save_cache()

    def display_results(self):
        val_items = [(iname, ipos, ival, ival[1] or ival[0] or 0)
                        for iname, ipos, ival in self.priced_items]
        print('Displaying maybe valuable bases')
        for iname, ipos, ival, compval in val_items:
            if compval > 2:
                print('{} - {}\n{}\n------'.format(iname, ipos, ival))
        print('Finished')

if __name__ == '__main__':
    with open('teststuff.json', 'r') as f:
        test_stuff = json.load(f)
    tab = BulkTab(**test_stuff)
    tab.process_items()
    tab.display_results()
