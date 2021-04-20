from tabs.basetab import BaseTab
from pricers.bases import ItemBasePricer
from pricers.uniques import UniquePricer
from items.itembase import maybe_create
from refs import credentials
import requests

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

class DumpTab(BaseTab):
    tabkey = 'dump'
    pricer_config = []

    def display_price(self):
        output = []
        tab = self.get_values()
        self.print_rares(tab['rare'])
        self.print_uniques(tab['unique'])

    def get_values(self):
        raw_items = self.get_raw_tab(**credentials)
        parsed = {'rare': [], 'unique': []}
        for raw in raw_items:
            item = maybe_create(raw)
            if item is None:
                continue
            parsed[item.dkey].append(item)
        return parsed

    def print_rares(self, rares):
        print('Rares')
        nprices = ItemBasePricer().get_values()
        for item in rares:
            nprice = nprices.get(item.get_nkw(), 0)
            if nprice < 5:
                #print('Skipping u: ', item)
                continue
            val = item.get_trade_value()
            print(item)
            print(f'{nprice:5.0f} | {val}')

    def print_uniques(self, uniques):
        print('Uniques')
        nprices = UniquePricer().get_values()
        for item in uniques:
            try:
                nprice = nprices[item.get_nkw()]
            except KeyError:
                print('Bad unique: ', item)
            if nprice < 5:
                #print('Skipping r: ', item)
                continue
            #val = item.get_trade_value()
            print(item)
            print(f'{nprice:5.0f} | None')



if __name__ == '__main__':
    dt = DumpTab()
    dt.display_price()