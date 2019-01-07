import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import time

CACHE_FP = os.getcwd() + '/refs/currency.json'
CURRENCY_REF_FP = os.getcwd() + '/refs/currency.txt'
CURRENCY_URL = 'https://www.pathofexile.com/item-data/currency'
EXCH_URL = 'https://www.pathofexile.com/api/trade/exchange/Betrayal'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'
EXCH_N = 20

class Currencyerator(object):
    def __init__(self):
        self.exchange = self.load_exchange()

    def load_exchange(self):
        if 'currency.json' not in os.listdir('refs'):
            print('No cache file found, creating new exch rates')
            return self.create_new_exchange()
        with open(CACHE_FP, 'r') as f:
            crncy = json.load(f)
        now = datetime.datetime.now()
        if now.timestamp() - crncy['updated'] > (now - datetime.timedelta(days=2)).timestamp():
            print('Currency rates stale (probably), fetching new ones')
            return self.create_new_exchange()
        print('Using cached rates')
        return crncy
            
    def create_new_exchange(self):
        output = {'updated': datetime.datetime.now().timestamp(), 'rate':{'chaos': 1}}
        with open(CURRENCY_REF_FP, 'r') as f:
            crncydict = json.load(f)
        for currname, curr in crncydict.items():
            qry = {"exchange": {"status": {"option":"online"}, "have": ["chaos"], "want": [curr]}}
            qrys = self.query_exch_api(qry)
            result = self.fetch_exch(qrys)
            output['rate'][curr] = result
            time.sleep(0.5)
        with open(CACHE_FP, 'w') as f:
            print('Writing cache')
            json.dump(output, f)
        return output

    def query_exch_api(self, qry):
        r = requests.post(EXCH_URL, json=qry)
        if r.status_code != 200:
            print(qry)
            print(r.text)
            raise
        return r.json()['result']

    def fetch_exch(self, idlist):
        max_n = min(EXCH_N, len(idlist))
        amts = []
        for i in range(0, max_n, 10):
            r = requests.get(FETCH_URL + '{' + ','.join(idlist[i:i+10]) + '}')
            results = r.json()['result']
            amts += [res['listing']['price']['amount'] for res in results if res]
        if len(amts) == 0:
            return None
        return sum(amts) / float(len(amts))

    def convert(self, pricedicts):
        return [self.exchange['rate'][prd['currency']] * prd['amount'] for prd in pricedicts]

if __name__ == '__main__':
    ccy = Currencyerator()

