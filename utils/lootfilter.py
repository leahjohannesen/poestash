import re

FILTER_FOLDER = 'C:/Users/zbebb/Documents/My Games/Path of Exile/{}'
BASE_FILE = 'basechaos.filter'
FANCY_FILE = 'fancychaos.filter'

overrides = {
    'BodyArmours': 'Body Armours',
    'OneHandWeapons': 'Daggers',
}

def load_base_filter():
    with open(FILTER_FOLDER.format(BASE_FILE), 'r') as f:
        return f.read()

def save_new_filter(text):
    with open(FILTER_FOLDER.format(FANCY_FILE), 'w') as f:
        f.write(text)

def adjust_filter(hide=None):
    text = load_base_filter()
    if hide is None:
        return
    for rawkey in hide:
        key = overrides.get(rawkey, rawkey)
        text = rem_from_filter(key, text)
    save_new_filter(text)

# def add_to_filter(key, text):
#     rawtxt, start, end = find_entry(key, text)
#     newtxt = '\n'.join(ln[1:] for ln in rawtxt.split('\n'))
#     print('old\n', rawtxt)
#     print('new')
#     print(newtxt)
#     return newtxt

def rem_from_filter(key, text):
    rawtxt, start, end = find_entry(key, text)
    newtxt = '\n'.join(f'#{ln}'for ln in rawtxt.split('\n'))
    return text[:start] + newtxt + text[end:]

def find_entry(key, text):
    fstr = '# FilterBlade: Conditional Entry'
    results = re.finditer(fstr, text)
    for res in results:
        startidx = res.start()
        if text[startidx - 1] == '#':
            startidx -= 1
        padded = text[startidx:startidx + 500]
        endmatch = re.search('\n\n', padded)
        endidx = startidx + endmatch.start()
        fullstr = text[startidx:endidx]
        if key in fullstr:
            return fullstr, startidx, endidx
    raise
        

if __name__ == '__main__':
    test = ['Boots']
    adjust_filter(test)

