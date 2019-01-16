import requests
import json
import os
import time
import datetime
import numpy as np
import pickle
from currency import Currencyerator

CACHE_FP = os.getcwd() + '/refs/pricecache.pkl'
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
        self.item_stats = 'min, n5, low10, fullavg, max, n'

    def load_cache(self):
        if 'pricecache.pkl' not in os.listdir('refs'):
            return {}
        with open(CACHE_FP, 'rb') as f:
            return pickle.load(f)

    def save_cache(self):
        with open(CACHE_FP, 'wb') as f:
            pickle.dump(self.cache, f)

    def purge_item(self, hashkw):
        self.cache.pop(hashkw)
        self.save_cache()

    def get_price_stats(self, hashkw, query):
        now = datetime.datetime.now()
        if hashkw not in self.cache:
            return self.get_new_price_stats(hashkw, query)
        cachetime = self.cache[hashkw]['updated']
        if cachetime < (now - datetime.timedelta(1)).timestamp():
            print('Found in cache, but old')
            return self.get_new_price_stats(hashkw, query)
        print('Price found in cache')
        return self.cache[hashkw]['price']

    def get_new_price_stats(self, hashkw, query):
        #all the steps
        print('Querying for price')
        query_res = self.query_trade_api(query)
        #print('Found {} results, fetching and converting'.format(query_res['total']))
        fetch_res = self.fetch_trade(query_res['result'])
        output = self.process_prices(fetch_res)
        #todo: add to cache
        self.cache[hashkw] = {
                'updated':datetime.datetime.now().timestamp(),
                'price': output,
            }
        return output

    def query_trade_api(self, qry):
        #hits the trade api
        r = requests.post(QUERY_URL, json=qry)
        time.sleep(1)
        if r.status_code != 200:
            print('Query failed with error {}\n{}\n{}'.format(
                r.status_code, r.text, qry))
            raise
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
        #leave out the nones
        clean_prices = [price for price in raw_prices if price]
        if not clean_prices:
            return (0, 0, 0, 0, 0 ,0)
        prices = np.array(self.currency.convert(clean_prices))
        prices = np.sort(prices)
        full_avg = prices.mean()
        min_val = prices[0]
        max_val = prices[-1]
        if prices.size < 10:
            return (min_val, None, None, full_avg, max_val, prices.size)
        n_5 = prices[5]
        low_10_avg = prices[:10].mean()
        return (min_val, n_5, low_10_avg, full_avg, max_val, prices.size)


if __name__ == '__main__':
    smpl = {"query":{"status":{"option":"online"},"type":"Exquisite Blade","stats":[{"type":"and","filters":[]}]},"sort":{"price":"asc"}}   
    trd = Traderator()
    test = trd.get_pricing('blah', smpl)

