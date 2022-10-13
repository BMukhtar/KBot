import requests  # library to send requests to web site(krisha.kz)
from bs4 import BeautifulSoup as bs  # library to copy all html-code
import csv  # library to write info to csv
import pandas as pd  # to convert csv to pandas DataFrame
import numpy as np  # to work np. arrays

"""
Initial setup:
1) create virtualenv project using pycharm

2) install the following libraries to virtualenv:
pip install numpy
pip install pandas
pip install requests
pip install beautifulsoup4
pip install lxml
"""

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
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
        # try:
        #     pagination = soup.find_all('a', attrs={'class': 'paginator__btn'})
        #     count = int(pagination[-2].text)
        #     for i in range(3, count - 1):
        #         url = 'https://krisha.kz/arenda/kvartiry/almaty/?das[rent.period]=2&page={i}'.format(i=i + 1)
        #         if url not in urls:
        #             urls.append(url)
        # except:
        #     pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'a-card a-storage-live ddl_product ddl_product_link not-colored is-visible'})
            for div in divs:
                title = div.find('a', attrs={'class': 'a-card__title'}).value
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
