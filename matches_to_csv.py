import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    # read csv file and create an array of all players names
    df = pd.read_csv('./data/AtpRankedPlayersNames.csv')
    names = df['name']
   

if __name__ == '__main__':
    main()