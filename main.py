import requests  # library to send requests to web site(krisha.kz)
from bs4 import BeautifulSoup as bs  # library to copy all html-code
import csv  # library to write info to csv
import pandas as pd  # to convert csv to pandas DataFrame
import numpy as np  # to work np. arrays

"""
pip install numpy
pip install pandas
pip install requests
pip install beautifulsoup4
"""

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

base_url = 'https://krisha.kz/arenda/kvartiry/almaty/?das[rent.period]=2&page=2'


def krisha_parse(base_url, headers):
    flats = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'class': 'paginator__btn'})
            count = int(pagination[-2].text)
            # print(count)
            for i in range(count - 1):
                url = f'https://krisha.kz/arenda/kvartiry/almaty/?das[rent.period]=2&page={i + 1}'
                if url not in urls:
                    urls.append(url)
                # print(url)
        except:
            pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'a-card__body ddl_product_link'})
            for div in divs:
                title = div.find('a', attrs={'class': 'a-a-card__title link'}).text
                price = div.find('div', attrs={'class': 'a-card__price'}).text
                href = div.find('a', attrs={'class': 'a-card__title'})['href']
                address = div.find('div', attrs={'class': 'a-card__subtitle'}).text
                content = div.find('div', attrs={'class': 'a-card__text-preview'}).text
                owner = div.find('div', attrs={'class': 'a-card__owner user-title-not-pro'})
                if owner is None:
                    specialist = 1
                    owner = 0
                else:
                    specialist = 0
                    owner = 1
                flats.append({
                    'title': title,
                    'price': price,
                    'href': href,
                    'address': address,
                    'content': content,
                    'specialist': specialist,
                    'owner': owner
                })
        print(len(flats))
    else:
        print('ERROR')
    return flats


def files_writer(flats):
    # with open('HeadHunter.csv', 'a', encoding='utf-8') as file:
    with open(r"Krisha.csv", "w", encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('title', 'price', 'href', 'address', 'content', 'owner', 'specialist'))
        for flat in flats:
            a_pen.writerow((flat['title'], flat['price'], flat['href'], flat['address'], flat['content'], flat['owner'],
                            flat['specialist']))


flats = krisha_parse(base_url, headers)
files_writer(flats)
