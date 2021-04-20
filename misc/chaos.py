from utils import cacheable
from utils.lootfilter import adjust_filter
from tabs.chaostab import ChaosTab
from collections import Counter
from math import floor
from itertools import chain


class ChaosRecipe():
    recipe = [
        ('OneHandWeapons', 2),
        #('OneHandWeapons', 1),
        ('Helmets', 1), 
        ('BodyArmours', 1), 
        ('Gloves', 1),
        ('Belts', 1),
        ('Boots', 1),
        ('Amulets', 1),
        ('Rings', 2),
        #('Rings', 1)
        ]

    def __init__(self, n=10):
        self.n_sets = n
    
    def display_current(self):
        values = self.get_tab_values()
        status = self.get_status(values)
        nsets = self.calc_sets
        self.show_counts(status)
        counts = Counter(x.iclass for x in values)
        n_sets = self.calc_sets(counts)
        print(f'n_sets | {n_sets}')

    def adjust_current(self):
        values = self.get_tab_values()
        status = self.get_status(values)
        self.show_counts(status)
        self.adjust_filter(status)

    def get_tab_values(self):
        return ChaosTab().get_values()

    def get_status(self, values):
        counts = Counter(x.iclass for x in values)
        return [(icls, counts[icls], nset * self.n_sets, nset) for icls, nset in self.recipe]

    def show_counts(self, status):
        print('current counts')
        for st in status:
            print(f'{st[0].ljust(15)} | {st[1]:2d} / {st[2]:2d} ({st[3]})')
        print('\n')

    def adjust_filter(self, status):
        to_hide = []
        for icls, ct, nmax, _ in status:
            # this prob wont happen
            if icls in ['Belts', 'Rings', 'Amulets'] or ct < nmax:
                continue
            to_hide.append(icls)
        print(f'hiding | {" ".join(to_hide)}')
        adjust_filter(to_hide)

    def cash_in(self):
        values = ChaosTab().get_values()
        status = self.get_status(values)
        self.show_counts(status)
        counts = Counter(x.iclass for x in values)
        n_sets = self.calc_sets(counts)
        print(f'n_sets | {n_sets}')
        optimal = self.get_optimal(values, n_sets)
        self.show_optimal(optimal)

    def calc_sets(self, counts):
        return min(floor(counts[icls] / nset) for icls, nset in self.recipe)

    def get_optimal(self, values, n):
        ordered = {}
        for icls, nset in self.recipe:
            matches = [val for val in values if val.iclass == icls]
            srtd = sorted(matches, key=lambda x: x.ilvl)
            ordered[icls] = [srtd[i * nset: i * nset + nset] for i in range(0, n)]
        return [chain.from_iterable(rawset) for rawset in zip(*ordered.values())]

    def show_optimal(self, optimal):
        for i, cset in enumerate(optimal):
            print(f'set {i}')
            for item in cset:
                print(f'{str(item).ljust(30)} | {item.loc[0]:2d}  {item.loc[1]:2d}')
            print('\n')



if __name__ == '__main__':
    cr = ChaosRecipe(4)
    #cr.display_status()
    #cr.show_counts(st)
    #cr.adjust_filter(st)
    blah = cr.cash_in()
    #values = ChaosTab().get_values()




