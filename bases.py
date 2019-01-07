import requests
from bs4 import BeautifulSoup
import json
import os

def get_items_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_list = soup.find_all('tr', {'class': 'even'})
    names = []
    for item in raw_list:
        names.append(list(item.find('td', {'class': 'name'}).children)[0])
    return names
        
def save_items(urls):
    itemdict = {itype: get_items_from_url(url) for itype, url in urls.items()}
    fp = os.getcwd() + '/refs/bases.txt'
    with open(fp, 'w') as f:
        json.dump(itemdict, f)

if __name__ == '__main__':
    urls = {
        'weapon': 'https://www.pathofexile.com/item-data/weapon',
        'armour': 'https://www.pathofexile.com/item-data/armour',
        'jewelry': 'https://www.pathofexile.com/item-data/jewelry',
        }

    save_items(urls)
