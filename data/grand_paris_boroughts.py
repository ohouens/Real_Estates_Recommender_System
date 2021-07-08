import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'http://comersis.fr/communes.php?epci=200054781'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

cities = soup.find('tbody').find_all('tr')
# print(cities[0].prettify())

names = [city.find('a').get_text() for city in cities]
departments = [city.find(class_="label").get_text() for city in cities]

boroughts = pd.DataFrame({
    "name": names,
    "departments": departments
})

# print(boroughts.head())
boroughts.to_csv('grand_paris_boroughts.csv')
