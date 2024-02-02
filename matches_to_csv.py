from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def pull_player_matches(url, name):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Use the appropriate webdriver for your browser

    # Navigate to the URL with dynamically loaded content
    url = f'{url}{name}'
    driver.get(url)

    # Wait for the dynamic content to load (adjust the timeout as needed)
    try:
        wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recent-results"]')))
    except TimeoutException:
        print('timeout exception')
    # Get the page source after JavaScript has executed
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    results_table = soup.find('table', {'id': 'recent-results'})
    if results_table == None: return ['None']
    player_matches = []
    for tr in results_table.find_all('tr'):
        mtch = []
        for td in tr.find_all('td'):
            mtch.append(td.text)
        player_matches.append(mtch)
    return player_matches

def main():
    # read csv file and create an array of all players names
    df = pd.read_csv('./data/AtpRankedPlayersNames.csv')
    names = df['name']
    
    # iterate through every player's name to grab their recent matches from tennisabtract.com
    url = 'https://www.tennisabstract.com/cgi-bin/player.cgi?p='
    data = []
    count = 1
    for name in names:
       data.append((name, pull_player_matches(url, name)))
       # number of players you want to pull starting at the rank 1 player
       if count >= 500: break
       count += 1
    newDf = pd.DataFrame(data)
    newDf.columns = ['name', 'matches']
    newDf.to_csv('./data/MatchHistory.csv')

if __name__ == '__main__':
    main()