import requests
from bs4 import BeautifulSoup
import pandas as pd

# 'https://live-tennis.eu/en/atp-live-ranking'
url = 'https://www.atptour.com/en/rankings/singles'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

htmltable = soup.find('table', { 'class' : 'mega-table desktop-table' })
names = []
for tr in htmltable.findAll('tr'):
    for td in tr.findAll('td', {'class':'player bold heavy'}):
        ul = td.find('ul', {'class':'player-stats'})
        li = ul.find('li', {'class':'name center'})
        a = li.find('a')
        span = a.find('span')
        names.append(a.text)

print(names)