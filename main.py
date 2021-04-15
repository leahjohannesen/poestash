from misc.altgem import AltGemmer
from tabs.currency import CurrencyTab
from tabs.fragments import FragmentTab
from tabs.divination import DivinationTab

class PoeHelper():
    def __init__(self):
        self.altgemmer = AltGemmer()
        self.currtab = CurrencyTab()
        self.fragtab = FragmentTab()
        self.divtab = DivinationTab()

    def eval_gem(self):
        self.altgemmer.display_value()

    def price_curr(self, force=False):
        self.currtab.display_price(force_skip=force)

    def price_frag(self, force=False):
        self.fragtab.display_price(force_skip=force)

    def price_div(self, force=False):
        self.divtab.display_price(force_skip=force)
        

if __name__ == '__main__':
    poe = PoeHelper()