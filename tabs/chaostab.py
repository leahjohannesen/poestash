from tabs.basetab import BaseTab
from items.itembase import valid_chaos, maybe_create
from refs import credentials
import requests

RAW_URL = 'https://www.pathofexile.com/character-window/get-stash-items?league={}&tabIndex={}&accountName={}'

class ChaosTab(BaseTab):
    tabkey = 'chaos'
    pricer_config = []

    def get_values(self, debug=False):
        raw_items = self.get_raw_tab(**credentials)
        return [maybe_create(raw) for raw in raw_items if valid_chaos(raw)]


if __name__ == '__main__':
    ct = ChaosTab()
    blah = ct.get_values()