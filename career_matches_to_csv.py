from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def pull_all_matches(url1, url2, name):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Use the appropriate webdriver for your browser

    # Navigate to the URL with dynamically loaded content
    url = f'{url1}{name}{url2}'
    driver.get(url)

    # Wait for the dynamic content to load (adjust the timeout as needed)
    try:
        wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="matches"]')))
    except TimeoutException:
        print('timeout exception')
    # Get the page source after JavaScript has executed
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    results_table = soup.find('table', {'id': 'matches'})
    if results_table == None: return ['None']
    tbody = results_table.find('tbody')
    player_matches = []
    for tr in tbody.find_all('tr'):
        mtch = []
        for td in tr.find_all('td'):
            mtch.append(td.text)
        player_matches.append(mtch)
    return player_matches

def main():
    # read csv file and create an array of all players names
    df = pd.read_csv('./data/AtpRankedPlayersNames.csv')
    names = df['name']
    
    # iterate through every player's name to grab their career matches from tennisabtract.com
    url1 = 'https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p='
    url2 = '&f=ACareerqq'
    data = []
    #count represents the number of players that we end up pulling
    count = 1
    number_of_players = 500
    for name in names:
       data.append((name, pull_all_matches(url1, url2, name)))
       # number of players you want to pull starting at the rank 1 player
       if count >= number_of_players: break
       count += 1
    #putting data into a dataframe and saving it to a csv file
    newDf = pd.DataFrame(data)
    newDf.columns = ['name', 'matches']
    csv_name = f'./data/AllMatchHistoryTop{count}.csv'
    newDf.to_csv(csv_name)

if __name__ == '__main__':
    main()