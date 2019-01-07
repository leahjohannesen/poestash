import requests
import json
import os
import time
from currency import Currencyerator

CACHE_FP = os.getcwd() + '/refs/pricecache.json'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'
QUERY_URL = 'https://www.pathofexile.com/api/trade/search/Betrayal'
QUERY_N = 20

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

    def load_currency(self):

    def query_trade_api(self, qry):
        r = requests.post(QUERY_URL, json=qry)
        return r.json()

    def fetch_trade(self, idlist):
        max_n = min(QUERY_N, len(idlist))
        results = {}
        for i in range(0, max_n, 10):
            r = requests.get(FETCH_URL + '{' + ','.join(idlist[i:i+10]) + '}')
            res = r.json()['results']
            price = { 
        return 

if __name__ == '__main__':
    smpl = {"query":{"status":{"option":"online"},"type":"Exquisite Blade","stats":[{"type":"and","filters":[]}]},"sort":{"price":"asc"}}   
    trd = Traderator()
    qrys = trd.query_trade_api(smpl)
    trd = trd.fetch_trade(qrys['result'])

