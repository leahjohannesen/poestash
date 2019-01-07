import requests
import json
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
        #self.items = self.process_items()

    def get_raw_tab(self):
        #automoate the cookie getting?
        r = requests.post(RAW_URL.format(self.league, self.tabidx, self.acct), headers={'Cookie': 'POESESSID={}'.format(self.cookie)})
        return json.loads(r.text)

    def process_items(self):
        self.items = [BaseItem(itemtxt) for itemtxt in self._raw_tab['items']]

if __name__ == '__main__':
    from teststuff import test_stuff
    tab = BulkTab(**test_stuff)
    tab.process_items()

