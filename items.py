from collections import Counter

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
        self.name = self._raw_val['name']
        self.type = self._raw_val['typeLine']
        #TODO: type is gross if it's a magic item, compare it to normal shit

    def proc_special_info(self):
        #special?
        self.elder = self._raw_val.get('elder', False)
        self.shaper = self._raw_val.get('shaper', False)
        self.rarity = self._raw_val['frameType']
        self.corrupted = self._raw_val.get('corrupted', False)

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

    def check_base_value(self):
        raise NotImplementedError

    def check_fancy_value(self):
        raise NotImplementedError

    def __repr__(self):
        special = 'Unique' if self.rarity == 3 else 'Elder' if self.elder else 'Shaper' if self.shaper else 'Normal'
        #links = self.n_links if self.n_links >= 5 else 'NoL'
        return ''' {} | {} | {} | {} '''.format(self.name, self.type, self.ilvl, special)

    def __str__(self):
        special = 'Unique' if self.rarity == 3 else 'Elder' if self.elder else 'Shaper' if self.shaper else 'Normal'
        return '''
            {} | {} | {}
            {}
            '''.format(self.name, self.type, self.ilvl, special)
 
class TempItem(BaseItem):
    def __init__(self, raw_val):
        super(TempItem, self).__init__(raw_val)
        self.proc_special_info()

    def check_base_value(self):
        pass
