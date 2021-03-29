import json
import os
import datetime
import time

CACHE_FP = 'utils/cache.json'

# TODO maybe db this at some point
# idea is one big cache, and each thing produces a unique id to ref against
class Cacherator():
    # min time to write cache to avoid spamming
    min_t = 5 * 60
    
    def __init__(self, purge=False):
        self.cache = None
        self.last_updated = None
        if purge:
            self.rem_cache()
        self.load_cache()

    def load_cache(self):
        try:
            with open(CACHE_FP, 'r') as f:
                self.cache = json.load(f)
                self.last_updated = self.now
                print('Cache loaded')
                return
        except FileNotFoundError as e:
            print('Cache file not found, creating')
        self.create_cache()

    def create_cache(self):
        self.cache = {}
        self.save_cache(True)

    def rem_cache(self):
        try:
            os.remove(CACHE_FP)
            print('Cache removed')
        except:
            pass

    def save_cache(self, force):
        delta = 0 if force else self.now - self.last_updated
        if not force and delta < self.min_t:
            print('Skipping save')
            return
        with open(CACHE_FP, 'w') as f:
            print('Saving cache')
            json.dump(self.cache, f)
        self.last_updated = self.now
        return

    def check(self, key, tstale):
        try:
            cache_val = self.cache[key]
            delta = self.now - cache_val['ts']
            if delta < tstale:
                return cache_val['value']
        except:
            raise

    def add_value(self, key, value, force=False):
        print(f'cache adding {key} to cache')
        self.cache[key] = {'ts': self.now, 'value': value}
        self.save_cache(force)

    @property
    def now(self):
        return int(datetime.datetime.now().timestamp())

    def __del__(self):
        pass
        #self.save_cache()

if __name__ == '__main__':
    tstale = 100
    cache = Cacherator(purge=True)
    cache.add_value('butts', 'spaghetti')
    print('butts check', cache.check('butts', tstale))
    print('farts check', cache.check('farts', tstale))
    time.sleep(2)
    cache.add_value('farts', 'banana')
    print(cache.cache)
    print('butts check', cache.check('butts', tstale))
    print('farts check', cache.check('farts', tstale))
    time.sleep(2)
    cache.add_value('butts', 'toot')
    print(cache.cache)
    print('butts check', cache.check('butts', tstale))
    print('farts check', cache.check('farts', tstale))


