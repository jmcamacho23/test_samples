"""
Author: Jose Camacho
Single-file weather scraper for 3 random cities
HEADERS are necessary in case the site tries to prevent scrapers without user agent strings
will create an xml file at the end once the prices for each are found

"""
from bs4 import BeautifulSoup
import requests, os, re
from datetime import datetime
import xml.etree.ElementTree as ET


time_now = datetime.now()
date_format = f'%d %b %I:%M %p %Z'
datetime_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36'
}
base_url = 'https://forecast.weather.gov/MapClick.php?'

urls_alias_dictionary = {'NYC': 'lat=40.714270000000056&lon=-74.00596999999993', 'LA': 'lat=34.052238&lon=-118.243344',
                         'Green Bay': 'lat=44.5133&lon=-88.0133'}


def test_weather_scraper_and_save():
    # set up main root element
    root = ET.Element("weather", time_zone="local_timezone", source="weather.gov")

    script_directory = os.path.dirname(os.path.abspath(__name__))
    file_name = f'{script_directory}/weather_temps_f.xml'

    for name, url in urls_alias_dictionary.items():
        station = requests.get(f'{base_url}{url}', headers=HEADERS)
        station.raise_for_status()

        location_main = ET.SubElement(root, "location")

        location_name = ET.SubElement(location_main, "name")
        location_name.text = name

        soup = BeautifulSoup(station.content, 'html.parser')
        # print(f'PAGE OUTPUT: \r{soup}') # un-comment for debugging
        print(f'Attempting to find info for {name}...')

        temp_value = soup.find('div', id='current_conditions-summary').find('p', class_='myforecast-current-lrg').text
        temp_value_cleaned = temp_value.replace("°F", "")
        humidity_value = soup.find('div', id='current_conditions_detail').find_all('tr')[0].text
        humidity_value_cleaned = humidity_value.replace('Humidity', '').strip()
        time_observed = soup.find('div', id='current_conditions_detail').find_all('tr')[6].text
        time_observed_cleaned = time_observed.replace("Last update", "").strip()

        time_cleaned = re.sub(r'\s[A-Za-z]{3}$', ' ', time_observed_cleaned).upper() + f" {time_now.year}"
        datetime_new = datetime.strptime(time_cleaned, "%d %b %I:%M %p %Y")

        print(f'{name}\n temp: {temp_value_cleaned} | Humidity: {humidity_value_cleaned} | Time Updated: {datetime_new}')

        temp_observed = ET.SubElement(location_main, "temp_value")
        temp_observed.text = temp_value_cleaned

        temp_observed_unit = ET.SubElement(location_main, 'temp_unit')
        temp_observed_unit.text = "F"

        humidity_observed = ET.SubElement(location_main, 'humidity')
        humidity_observed.text = humidity_value_cleaned

        temp_time_observed = ET.SubElement(location_main, "time_observed")
        temp_time_observed.text = str(datetime_new)

    tree = ET.ElementTree(root)

    # now write the entire loop to a xml file
    with open(f'{file_name}', 'wb') as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
