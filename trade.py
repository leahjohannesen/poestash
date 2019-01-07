import requests
import json
import os
import time
import datetime
from currency import Currencyerator

CACHE_FP = os.getcwd() + '/refs/pricecache.json'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'
QUERY_URL = 'https://www.pathofexile.com/api/trade/search/Betrayal'
QUERY_N = 50

class Traderator(object):
    '''
    This guy will hang out and recieve query requests. It will attempt to hit a cache,
    for an item base, if not there, it'll query for it.
    '''
    def __init__(self):
        self.cache = self.load_cache()
        self.currency = Currencyerator()

    def load_cache(self):
        if 'pricecache.json' not in os.listdir('refs'):
            return {}
        with open(CACHE_FP, 'r') as f:
            return json.load(f)

    def get_pricing(self, hashkw, query):
        now = datetime.datetime.now()
        if hashkw not in self.cache:
            return self.get_new_pricing(hashkw, query)
        cachetime = self.cache[hashkw]['updated']
        if now.timestamp - cachetime > (now - datetime.timedelta(2)).timestamp():
            return self.get_new_pricing(hashkw, query)
        return self.cache[hashkw]

    def get_new_pricing(self, hashkw, query):
        #all the steps
        query_res = self.query_trade_api(query)
        print('Found {} results, fetching and converting'.format(query_res['total']))
        fetch_res = self.fetch_trade(query_res['result'])
        output = self.process_prices(fetch_res)
        #todo: add to cache
        return output

    def query_trade_api(self, qry):
        #hits the trade api
        r = requests.post(QUERY_URL, json=qry)
        return r.json()

    def fetch_trade(self, idlist):
        #fetches the results given the trade api ids
        max_n = min(QUERY_N, len(idlist))
        raw_prices = []
        for i in range(0, max_n, 10):
            r = requests.get(FETCH_URL + '{' + ','.join(idlist[i:i+10]) + '}')
            results = r.json()['result']
            raw_prices += [res['listing']['price'] for res in results if res]
            time.sleep(0.5)
        return raw_prices

    def process_prices(self, raw_prices):
        #converts the prices and i think can be fancier later
        prices = self.currency.convert(raw_prices)
        return sum(prices) / len(prices)


if __name__ == '__main__':
    smpl = {"query":{"status":{"option":"online"},"type":"Exquisite Blade","stats":[{"type":"and","filters":[]}]},"sort":{"price":"asc"}}   
    trd = Traderator()
    test = trd.get_pricing('blah', smpl)

