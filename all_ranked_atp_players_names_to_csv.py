import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def all_atp_ranked_players():
    url = 'https://www.atptour.com/en/rankings/singles?RankRange=0-5000'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    names = []
    rank = 1
    # iterate through and go down hierarchy of html to grab all players names and put it into an array
    htmltable = soup.find('table', { 'class' : 'mega-table desktop-table' })
    for tr in htmltable.findAll('tr'):
        for td in tr.findAll('td', {'class':'player bold heavy'}):
            ul = td.find('ul', {'class':'player-stats'})
            li = ul.find('li', {'class':'name center'})
            a = li.find('a')
            span = a.find('span')
            span = span.text
            span = span.replace(' ', '')
            span = span.replace('-', '')
            span = span.replace('.','')
            names.append((rank, span))
            rank += 1
        # change the condition to select how many players you want
        if rank >= 5000:
            break
            
    return names

def main():
    players = np.array(all_atp_ranked_players())
    df = pd.DataFrame(players)
    df.columns = ['rank', 'name']
    df.to_csv("./data/AtpRankedPlayersNames.csv", index=False)


if __name__ == "__main__":
    print('main ran')
    main()