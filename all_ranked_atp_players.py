import requests
from bs4 import BeautifulSoup
import numpy as np
from numpy import asarray
from numpy import savetxt

def all_atp_ranked_players():
    url = 'https://www.atptour.com/en/rankings/singles?RankRange=0-5000'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    names = []
    rank = 1
    htmltable = soup.find('table', { 'class' : 'mega-table desktop-table' })
    for tr in htmltable.findAll('tr'):
        for td in tr.findAll('td', {'class':'player bold heavy'}):
            ul = td.find('ul', {'class':'player-stats'})
            li = ul.find('li', {'class':'name center'})
            a = li.find('a')
            span = a.find('span')
            names.append({'name': span.text, 'rank': rank})
            rank += 1
            
    return names

def write_players_to_csv(players):
    for player in players:
        print(player)

players = all_atp_ranked_players()
write_players_to_csv(players)