import requests
import time
from refs import credentials

FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/'
QUERY_URL = f'https://www.pathofexile.com/api/trade/search/{credentials["league"]}'

class TradeError(Exception):
    pass

def get_listings(query, max_res=25):
        query_result = _query_trade_api(query)
        return _fetch_trades(query_result['result'], max_res)
    
def _query_trade_api(query):
        #hits the trade api
        uagent = credentials['uagent']
        cookie = credentials['cookie']
        r = requests.post(QUERY_URL, json=query, headers={'User-Agent': uagent, 'Cookie': 'POESESSID={}'.format(cookie)})
        time.sleep(1)
        if r.status_code != 200:
            print(f'query :: failed :: {r.status_code} :: {r.text}')
            print(query)
            if r.status_code == 400:
                raise TradeError
            raise
        return r.json()

def _fetch_trades(idlist, max_res=25):
    #fetches the results given the trade api ids
    uagent = credentials['uagent']
    cookie = credentials['cookie']
    max_n = min(max_res, len(idlist))
    output = []
    for i in range(0, max_n, 10):
        full_url = FETCH_URL + ','.join(idlist[i:i+10])
        r = requests.get(full_url, headers={'User-Agent': uagent, 'Cookie': 'POESESSID={}'.format(cookie)})
        results = r.json()['result']
        # if it's not priced in c/ex it's prob not relevant atm
        for res in results:
            if res is None:
                continue
            try:
                curr = res['listing']['price']['currency']
                if curr not in {'chaos', 'exalted'}:
                    continue
            except:
                print(res)
                raise
            output.append(res)
        # output += [res for res in results if res is not None 
        #             and res['price']['currency'] in {'chaos', 'exalted'}]
        time.sleep(0.5)
    return output
        
if __name__ == '__main__': 
    pass
    qry = {
        'query': {
            'status': {'option': 'online'},
            'type': 'Smite',
            'stats': [{'type': 'and', 'filters': []}],
            'filters': {'misc_filters': {'filters': {'gem_alternate_quality': {'option': '0'}}}}},
        'sort': {'price': 'asc'}
    }
    qres = _query_trade_api(qry)
    fres = _fetch_trades(qres['result'])

    
#     def process_prices(self, raw_prices):
#         #converts the prices and i think can be fancier later
#         #leave out the nones
#         clean_prices = [price for price in raw_prices if price]
#         if not clean_prices:
#             return (np.zeros(10), 0, 0)
#         prices = np.array(self.currency.convert(clean_prices))
#         prices = np.sort(prices)
#         output = np.pad(prices, (0, 10), 'constant', constant_values=np.nan)[:10].round(1)
#         return (output, np.nanmean(output), np.mean(prices))

#     def get_price_stats(self, hashkw, query):
#         now = datetime.datetime.now()
#         if hashkw not in self.cache:
#             return self.get_new_price_stats(hashkw, query)
#         cachetime = self.cache[hashkw]['updated']
#         FORCE = True
#         if FORCE or cachetime < (now - datetime.timedelta(STALETIME)).timestamp():
#             print('Found in cache, but old')
#             oldvals = self.cache[hashkw]['price']
#             return self.update_price_stats(hashkw, query, oldvals)
#         print('Price found in cache')
#         return self.cache[hashkw]['price']

#     def get_new_price_stats(self, hashkw, query):
#         outarr = np.zeros((3, 25))
#         #all the steps
#         print('Querying for price')
#         query_res = self.query_trade_api(query)
#         fetch_res = self.fetch_trade(query_res['result'])
#         newarr, rawarr, shortmean, longmean = self.process_prices(fetch_res)
#         outarr[0,:] = newarr
#         #todo: add to cache
#         self.cache[hashkw] = {
#                 'updated':datetime.datetime.now().timestamp(),
#                 'price': (outarr, rawarr, shortmean, longmean),
#             }
#         return (outarr, rawarr, shortmean, longmean)

#     def update_price_stats(self, hashkw, query, oldvals):
#         outarr = np.zeros((3, 25))
#         outarr[1:,] = oldvals[0][:2,]
#         #all the steps
#         print('Querying for price')
#         query_res = self.query_trade_api(query)
#         #print('Found {} results, fetching and converting'.format(query_res['total']))
#         fetch_res = self.fetch_trade(query_res['result'])
#         newarr, rawarr, shortmean, longmean = self.process_prices(fetch_res)
#         outarr[0,:] = newarr
#         #todo: add to cache
#         self.cache[hashkw] = {
#                 'updated':datetime.datetime.now().timestamp(),
#                 'price': (outarr, rawarr, shortmean, longmean),
#             }
#         return (outarr, shortmean, longmean)

#     def process_prices(self, raw_prices):
#         #converts the prices and i think can be fancier later
#         #leave out the nones
#         clean_prices = [price for price in raw_prices if price]
#         if not clean_prices:
#             return (np.zeros(25), 0, 0)
#         prices = np.array(self.currency.convert(clean_prices))
#         idxsort = np.argsort(prices)
#         prices = np.sort(prices)
#         rawarr = np.array(self.currency.fancy_raw(clean_prices))
#         rawsort = rawarr[idxsort][:10]
#         output = np.pad(prices, (0, 25), 'constant', constant_values=np.nan)[:25].round(1)
#         return (output, rawsort, np.nanmean(output), np.mean(prices))



