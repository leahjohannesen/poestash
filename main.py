from misc.altgem import AltGemmer
from misc.chaos import ChaosRecipe
from tabs.dumptab import DumpTab
from misc.queries import QueryShower
from tabs.currency import CurrencyTab
from tabs.fragments import FragmentTab
from tabs.divination import DivinationTab
from tabs.essences import EssenceTab

class PoeHelper():
    def __init__(self):
        self.altgemmer = AltGemmer()
        self.chaoser = ChaosRecipe()
        self.dumptab = DumpTab()
        self.currtab = CurrencyTab()
        self.fragtab = FragmentTab()
        self.divtab = DivinationTab()
        self.esstab = EssenceTab()
        self.qshower = QueryShower()

    def eval_gem(self):
        self.altgemmer.display_value()

    def check_all(self):
        print('\n***Curr***\n')
        self.price_curr()
        print('\n***Frag***\n')
        self.price_frag()
        print('\n***Div***\n')
        self.price_div()
        print('\n***Ess***\n')
        self.price_ess()
        print('\n***Dump***\n')
        self.check_dump()

    def price_curr(self, force=False):
        self.currtab.display_price(force_skip=force)

    def price_frag(self, force=False):
        self.fragtab.display_price(force_skip=force)

    def price_div(self, force=False):
        self.divtab.display_price(force_skip=force)

    def price_ess(self, force=False):
        self.esstab.display_price(force_skip=force)

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