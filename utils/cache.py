import json
import os
import datetime
import time

CACHE_FP = 'utils/cache.json'
SAVE_TIMEOUT = 5 * 60

def load_cache():
    try:
        with open(CACHE_FP, 'r') as f:
            print('Cache loaded from file')
            return json.load(f)
    except FileNotFoundError:
        print('Creating fresh cache')
        return {}

def get_now():
    return int(time.time())

CACHE = load_cache()
LAST_UPDATED = get_now()

def cacheable():
    def cache_func(func):
        def wrapped(*args, skip_cache=False):
            cache_key = args[0].cache_key
            timeout = args[0].timeout
            force_save = args[0].force_save
            print(args)
            now = get_now()
            try:
                if skip_cache:
                    print(f'cache | {cache_key} | force skip')
                    raise KeyError
                cached_val = CACHE[cache_key]
                if now - cached_val[0] > timeout:
                    print(f'cache | {cache_key} | stale')
                    raise KeyError
                print(f'cache | {cache_key} | successful')
                return cached_val[1]
            except KeyError:
                print(f'cache | {cache_key} | miss')
                CACHE[cache_key] = (now, func(*args))
                save_cache(force_save)
                return CACHE[cache_key][1]
        return wrapped
    return cache_func

# CAREFUL
def get_cache():
    return CACHE

def save_cache(force_save):
    now = get_now()
    global LAST_UPDATED
    if not force_save and now - LAST_UPDATED < SAVE_TIMEOUT:
        print('cache | save skipped')
        return False
    with open(CACHE_FP, 'w') as f:
        json.dump(CACHE, f)
    print(f'cache | save | force : {force_save}')
    LAST_UPDATED = now
    return True

def restart_cache():
    print('Restarting the cache')
    global CACHE
    os.remove(CACHE_FP)
    CACHE = load_cache()


if __name__ == '__main__':
    pass
