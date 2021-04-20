from misc.altgem import AltGemmer
from misc.chaos import ChaosRecipe
from tabs.dumptab import DumpTab
from misc.queries import QueryShower
from tabs import FIXED_REF

class PoeHelper():
    def __init__(self):
        self.altgemmer = AltGemmer()
        self.chaoser = ChaosRecipe()
        self.dumptab = DumpTab()
        self.qshower = QueryShower()
        self.fixed = {k: tabcls() for k, tabcls in FIXED_REF.items()}

    def eval_gem(self):
        self.altgemmer.display_value()

    def check_all(self):
        self.price_fixed()
        print('\n***Dump***\n')
        self.check_dump()

    def price_fixed(self, force=False):
        for tabn, tab in self.fixed.items():
            print(f'*** {tabn} ***')
            tab.display_price()

    def check_dump(self, force=False):
        self.dumptab.display_price()

    def crecipe_show(self):
        self.chaoser.display_current()

    def crecipe_adjust(self):
        self.chaoser.adjust_current()
    
    def crecipe_cash(self):
        self.chaoser.cash_in()

    def show_queries(self):
        self.qshower.show_queries()
        

if __name__ == '__main__':
    poe = PoeHelper()