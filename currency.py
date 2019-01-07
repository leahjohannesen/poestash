import requests
from bs4 import BeautifulSoup
import json
import os
import datetime

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
            return self.create_new_exchange()
        with open(CACHE_FP, 'r') as f:
            crncy = json.load(f)
        now = datetime.datetime.now()
        if crncy['updated'] - now > 2:
            return self.create_new_exchange()
        return crncy
            
    def create_new_exchange(self):
        output = {'updated': datetime.datetime.now(), 'rate':{}}
        with open(CURRENCY_REF_FP, 'r') as f:
            crncydict = json.load(f)
        import pdb;pdb.set_trace()
        for currname, curr in crncydict.items():
            qry = {"exchange": {"status": {"option":"online"}, "have": ["chaos"], "want": [curr]}}
            qrys = query_exch_api(qry)
            result = fetch_exch(qrys)
            output['rate'][curr] = result
        return output

    def query_exch_api(self, qry):
        r = requests.post(EXCH_URL, json=qry)
        return r.json()['result']

    def fetch_exch(self, idlist):
        max_n = min(EXCH_N, len(idlist))
        output = []
        for i in range(0, max_n, 10):
            r = requests.get(FETCH_URL + '{' + ','.join(idlist[i:i+10]) + '}')
            results = r.json()['result']
            output += [res['listing']['price']['amount'] for res in results if res]
        return sum(output) / float(len(output))
    

if __name__ == '__main__':
    ccy = Currencyerator()

