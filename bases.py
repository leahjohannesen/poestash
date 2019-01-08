import requests
from bs4 import BeautifulSoup
import json
import os
from refs.otherbases import others

def get_items_from_url(url):
    #TODO: might need to add icon to bases for ref
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_list = soup.find_all('tr')
    names = []
    for item in raw_list:
        search = item.find('td', {'class': 'name'})
        if search is None:
            continue
        weap_name = search.contents[0]
        names.append(weap_name)
    return names

def save_items(itemdict):
    fp = os.getcwd() + '/refs/bases.txt'
    with open(fp, 'w') as f:
        json.dump(itemdict, f)

if __name__ == '__main__':
    urls = {
        'weapons': 'https://www.pathofexile.com/item-data/weapon',
        'armour': 'https://www.pathofexile.com/item-data/armour',
        'accessories': 'https://www.pathofexile.com/item-data/jewelry',
        }

    item_dict = {itype: get_items_from_url(url) for itype, url in urls.items()}
    for k, v in others.items():
        item_dict[k] = v
    save_items(item_dict)
