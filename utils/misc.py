import requests
from refs import credentials


def get_data_from_url(url):
    r = requests.post(url, headers={'User-Agent': credentials['uagent'], 'Cookie': 'POESESSID={}'.format(credentials['cookie'])})
    return r.json()['items']
    

if __name__ == '__main__':
    blah = None

