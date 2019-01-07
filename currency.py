import requests
from bs4 import BeautifulSoup
import json

CURRENCY_URL = 'https://www.pathofexile.com/item-data/currency'
EXCHANGE_URL = 'https://www.pathofexile.com/api/trade/exchange/Betrayal'
EXCH_N = 10

class Currencyerator(object):
    def __init__(self):
        pass

    def base_currency_list(self):
        #if there's no basic file, get a list of them
        r = requests.get(CURRENCY_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        raw_list = soup.find_all('tr')#, {'class': 'even'})
        names = []
        for item in raw_list[1:]:
            names.append(list(item.find('td', {'class': 'name'}).children)[0])
        return names

    def query_exch_api(self, qry):
        r = requests.post(QUERY_URL, json=qry)
        return r.json()

    def fetch_exch(self, idlist):
        max_n = min(EXCH_N, len(idlist))
        results = {}
        for i in range(0, max_n, 10):
            r = requests.get(FETCH_URL + '{' + ','.join(idlist[i:i+10]) + '}')
            res = r.json()['results']
            price = {} 
        return 
    
    def parse_result(self, results):
        for res in results:

if __name__ == '__main__':
    ccy = Currencyerator()
    nms = ccy.base_currency_list()
    smpl = {"exchange":{"status":{"option":"online"},"have":["chaos"],"want":["exa"]}}
    blah = ccy.query_exch_api(smpl)
    testc = ccy.fetch_exch(smpl)

