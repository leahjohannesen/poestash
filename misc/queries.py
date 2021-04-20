from refs.rawqueries import raw_queries
from refs import credentials

RAW_URL = 'https://www.pathofexile.com/trade/search/{}/{}'

class QueryShower():
    def __init__(self):
        pass

    def show_queries(self):
        for k, vdict in raw_queries.items():
            print(f'{k.ljust(12)} | {(" ".join(vdict.get("tags", ""))).ljust(20)} | {RAW_URL.format(credentials["league"], vdict["qstr"])}')
    

if __name__ == '__main__':
    qs = QueryShower()
    qs.show_queries()
    #qs.show_fullstr('gv')




