from collections import Counter
import json

class BaseItem(object):
    '''
    Base item for some of the gruntwork, but considering the variability in items and stats, gonna write a class by class eval probably
    TODO: Break these out by type for better searching, but yolo for now
    '''

    def __init__(self, raw_val):
        #basic stuff
        self._raw_val = raw_val
        self.position = (self._raw_val['x'], self._raw_val['y'], self._raw_val['w'])
        #item independently mostly
        self.ilvl = self._raw_val['ilvl']
        self.identified = self._raw_val['identified']
        self.category = list(self._raw_val['category'].keys())[0]
        self.itemtype = list(self._raw_val['category'].values())
        self.rarity = self._raw_val['frameType']
        self.name = self._raw_val['name']
        self.type = self._raw_val['typeLine']
        self._raw_type = self.type
        if self.rarity == 1:
            self.overwrite_type()

        #special?
        self.elder = self._raw_val.get('elder', False)
        self.shaper = self._raw_val.get('shaper', False)
        self.unique = self.rarity == 3
        self.corrupted = self._raw_val.get('corrupted', False)
        self._base_query = {
            "status":{"option":"online"},
            "stats":[{"type":"and","filters":[]}]
            }

    def overwrite_type(self):
        with open('refs/bases.txt', 'r') as f:
            bases = json.load(f)
        for item in bases[self.category]:
            if item in self.type:
                self.type = item
                return
        raise Exception

    @classmethod
    def get_item_cls(cls, raw_val):
        item_info = raw_val['category']
        item_type = list(item_info.keys())[0]
        item_subtype = list(item_info.values())[0]
        #trt the subtype, if it's not there, default to type class
        if item_type == 'gems':
            return
        try:
            return ITEM_REF[item_subtype[0]](raw_val)
        except (KeyError, IndexError):
            return ITEM_REF[item_type](raw_val)

    def proc_mod_info(self):
        #general quality?
        self.mods = {
            'implicit': self._raw_val.get('implicitMods'),
            'explicit': self._raw_val.get('explicitMods'),
            }

    def proc_socket_info(self):
        #might do more fancy stuff with linking later
        raw_sock = self._raw_val['sockets']
        self.n_sockets = len(raw_sock)
        self.n_links = Counter([sock['group'] for sock in raw_sock]).most_common()[0][1]

    @property
    def item_query(self):
        if self.unique:
            return self.item_query_unique
        else:
            return self.item_query_basic

    @property
    def item_hash(self):
        if self.unique:
            return self.item_hash_unique
        else:
            return self.item_hash_basic

    @property
    def item_query_basic(self):
        query = self._base_query
        query['type'] = self.type
        query['filters'] = {
                'misc_filters': {
                    'disabled': False,
                    'filters': {
                        'elder_item': {'option': self.elder},
                        'shaper_item': {'option': self.shaper},
                        'ilvl': {'max': self.ilvl, 'min': self.ilvl},
                        },
                    },
                'type_filters': {
                    'disabled': False,
                    'filters': {
                        'rarity': {'option': 'nonunique'},
                        },
                    }
                }
        return {'query': query, 'sort': {'price': 'asc'}}

    @property
    def item_hash_basic(self):
        return (self.type, self.ilvl, self.elder, self.shaper)

    @property
    def item_query_unique(self):
        #eventually i should be able to process uniques without id, but for now i need to
        query = self._base_query
        query['type'] = self.type
        query['name'] = self.name
        #query['filters'] = {
        #        'type_filters': {
        #            'disabled': False,
        #            'filters': {
        #                'rarity': {'option': 'unique'},
        #                },
        #            }
        #        }
        return {'query': query, 'sort': {'price': 'asc'}}

    @property
    def item_hash_unique(self):
        return (self.name, self.type, 'unique')

    def __repr__(self):
        special = 'Unique' if self.rarity == 3 else 'Elder' if self.elder else 'Shaper' if self.shaper else 'Normal'
        #links = self.n_links if self.n_links >= 5 else 'NoL'
        return '''{} | {} | {} | {}'''.format(self.name, self.type, self.ilvl, special)

class BaseWeapon(BaseItem):
    def __init__(self, raw_val):
        super(BaseWeapon, self).__init__(raw_val)

class BaseArmor(BaseItem):
    def __init__(self, raw_val):
        super(BaseArmor, self).__init__(raw_val)

class BaseAccessory(BaseItem):
    def __init__(self, raw_val):
        super(BaseAccessory, self).__init__(raw_val)

class BaseJewel(BaseItem):
    def __init__(self, raw_val):
        super(BaseJewel, self).__init__(raw_val)

#eventually i can do item specific queries
ITEM_REF = {
    'weapons': BaseWeapon,
    'armour': BaseArmor,
    'accessories': BaseAccessory,
    'jewels': BaseJewel,
    'abyss': BaseJewel,
    }

if __name__ == '__main__':
    with open('teststuff.json', 'r') as f:
        test_stuff = json.load(f)
