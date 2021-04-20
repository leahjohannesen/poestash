import json
import os
import datetime
import time

CACHE_FP = 'utils/cache.json'
SAVE_TIMEOUT = 30

def load_cache():
    try:
        with open(CACHE_FP, 'r') as f:
            print('cache - loaded')
            return json.load(f)
    except FileNotFoundError:
        print('cache - creating fresh')
        return {}

def get_now():
    return int(time.time())

CACHE = load_cache()
LAST_UPDATED = 0

def cacheable():
    def cache_func(func):
        def wrapped(*args, cache_key=None, force_skip=False):
            # if the cache key is provided, use it
            ck =  cache_key if cache_key is not None else args[0].cache_key
            timeout = args[0].timeout
            force_save = args[0].force_save
            now = get_now()
            reason = ''
            try:
                if force_skip:
                    reason = ' - force skip'
                    raise KeyError
                cached_val = CACHE[ck]
                if now - cached_val[0] > timeout:
                    reason = ' - stale'
                    raise KeyError
                #print(f'cache - {ck} - successful')
                return cached_val[1]
            except KeyError:
                #print(f'cache - {ck} - miss {reason}')
                pass
            CACHE[ck] = (now, func(*args))
            save_cache(force_save)
            return CACHE[ck][1]
        return wrapped
    return cache_func

# CAREFUL
def get_cache():
    return CACHE

def save_cache(force_save):
    now = get_now()
    global LAST_UPDATED
    if not force_save and now - LAST_UPDATED < SAVE_TIMEOUT:
        print('cache - save skipped')
        return False
    with open(CACHE_FP, 'w') as f:
        json.dump(CACHE, f)
    print(f'cache - save{" forced" if force_save else ""}')
    LAST_UPDATED = now
    return True

def restart_cache():
    print('cache - restarted')
    global CACHE
    os.remove(CACHE_FP)
    CACHE = load_cache()


if __name__ == '__main__':
    pass
