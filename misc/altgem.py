from utils import cacheable
from items.skillgem import SkillGem

class AltGemmer():
    def __init__(self):
        pass
            
    def display_value(self):
        gemstr = input('Enter the gemstr: ')
        gem = SkillGem(gemstr)
        print(f'altgem :: {gem}')
        gem.show_value()

if __name__ == '__main__':
    gemmer = AltGemmer()
    # raw = ['a summon skitterbots']
    # gemmer.display_gems(raw)




