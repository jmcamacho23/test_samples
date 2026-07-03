"""
Author: Jose Camacho
Single-file Amazon price scraper for 3 random items
HEADERS are necessary because Amazon tries to prevent scrapers without user agent strings
will create an xml file at the end once the prices for each are found

"""

from bs4 import BeautifulSoup
import requests, os
from xml.dom import minidom
from datetime import datetime as dt

def test_amazon_scraper():
    time_now = dt.now()
    datetime_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip',
        'DNT': '1',
        'Connection': 'close'
    }
    base_url = 'https://amazon.com/'
    sls_fert_url = 'Advanced-16-4-8-Balanced-NPK-Concentrated/dp/B06XWFL84R'
    aabatteries_url = 'EBL-Rechargeable-Batteries-2800mAh-Ready2Charge/dp/B00DNPT1AO'
    air_filters_url = 'FilterBuy-20x25x1-Pleated-Furnace-Filters/dp/B00CJZ8PGU'

    urls = {'SLS Fert': sls_fert_url, 'AA Batteries': aabatteries_url, 'Air Filters': air_filters_url}

    root = minidom.Document()
    xml = root.createElement('amazon_prices')
    xml.setAttribute('date', datetime_now)
    root.appendChild(xml)

    script_directory = os.path.dirname(os.path.abspath(__name__))
    file_name = f'{script_directory}/amazon_prices.xml'


    for name, url in urls.items():
        station = requests.get(f'{base_url}{url}', headers=headers)
        station.raise_for_status()

        soup = BeautifulSoup(station.text, 'html.parser')

        subscribe_price = soup.find('span', id='sns-tiered-price').text
        subscribe_price_formatted = subscribe_price.split('(')[0].replace('$', '').split()[0]
        price_single = soup.find('div', id='corePrice_feature_div').find('span', class_='a-offscreen').text
        price_single_formatted = price_single.replace('$', '').split()[0]

        print(f'{name}\n Subscribe: ${subscribe_price_formatted} | Buy Now: ${price_single_formatted}')

        device = root.createElement('product')
        device.setAttribute('name', name)
        device.setAttribute('subscribe_price', subscribe_price_formatted)
        device.setAttribute('buy_now_price', price_single_formatted)

        xml.appendChild(device)
        xml_str = root.toprettyxml()

    # now write to file
    with open(f'{file_name}', 'a') as f:
        f.write(xml_str)
