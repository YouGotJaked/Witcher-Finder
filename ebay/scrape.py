import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_listings(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features='html.parser')
    return soup.find_all('li', attrs={'class': 's-item'})

def listings_to_df(listings, columns=['Title', 'Price', 'Date Added', 'Condition', 'Shipping', 'Link', 'Image']):
    rows = []
    for lst in listings:
        for name in lst.find_all('h3', attrs={'class':"s-item__title"}):
            title = str(name.find(text=True, recursive=False))

        if title != 'None':
            price = lst.find('span', attrs={'class':"s-item__price"})
            price = str(price.find(text=True, recursive=True))

            lst_date = lst.find('span', attrs={'class':"s-item__dynamic s-item__listingDate"})
            lst_date = str(lst_date.find(text=True, recursive=True))

            try:
                cond = lst.find('span', attrs={'class':"SECONDARY_INFO"})
                cond = str(cond.find(text=True, recursive=True))
            except AttributeError: # no condition
                cond = None

            try:
                ship = lst.find('span', attrs={'class':"s-item__shipping s-item__logisticsCost"})
            except AttributeError:
                ship = lst.find('span', attrs={'class':"s-item__dynamic s-item__freeXDays"})
            finally:
                if ship is None:
                    ship = lst.find('span', attrs={'class':"s-item__dynamic s-item__freeXDays"})
                if ship is None: #sponsered
                    continue
                ship = str(ship.find(text=True, recursive=True))

            item_img = lst.find('div', attrs={'class':"s-item__image"})
            href, src = [x for x in str(item_img).split() if x.startswith('href') or x.startswith('src')]
            href = re.search(r'\"(.*?)\?', href).group(1)
            src = re.search(r'\"(.*?)\"', src).group(1)

            rows.append([title, price, lst_date, cond, ship, href, src])
    return pd.DataFrame(rows, columns=columns)
