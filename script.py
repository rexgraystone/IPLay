from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import datetime

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
today = datetime.datetime.now()
current_year = today.year
seasons = range(2008, current_year)

class IPL:
    winners = {2008: 'RR', 2009: 'DEC', 2010: 'CSK', 2011: 'CSK', 2012: 'KKR', 2013: 'MI', 2014: 'KKR', 2015: 'MI', 2016: 'SRH', 2017: 'MI', 2018: 'CSK', 2019: 'MI', 2020: 'MI', 2021: 'CSK', 2022: 'GT'}
    """
    All the seasons and their corresponding winners
    """
    columns = ['Season', 'Position', 'Team', 'Played', 'Won', 'Lost', 'Tied', 'No Result', 'Net Run Rate', 'Score For', 'Overs For', 'Score Against', 'Overs Against', 'Points', 'Qualified?', 'Winner?']
    """
    All the columns that are required to store the table
    """

    def __init__(self, season: int) -> object:
        self.season = season
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get_values(self, values) -> list:
        """
        Split up all the elements in a particular iterable object into different elements in a list
        ### Parameters
        values: the iterable object
        """
        row = []
        for value in values:
            row.append(value.text)
        return row

    def get_qualifiers(self, index: int) -> int:
        """
        Checks whether a given team has qualified for the playoffs, if they finished in the Top 4
        ### Parameters
        index: the position of the team
        """
        if index < 4:
            return 1
        else:
            return 0

    def get_winner(self, team: str, season: int) -> int:
        """
        Checks whether a given team is the winner of a particular season
        ### Parameters
        team: the given team
        season: the year
        """
        if team == self.winners[season]:
            return 1
        else:
            return 0

    def extract(self, index: int, row: list) -> list:
        """
        Extract only the text and remove all unnecessary whitespaces from an element in a list
        ### Parameters 
        index: the position of the element to be updated
        row: the corresponding list of said element
        """
        score_for, overs_for = tuple(row[index].split('/'))
        score_against, overs_against = tuple(row[index+1].split('/'))
        del row[index:index+2]
        row.insert(index, score_for)
        row.insert(index+1, overs_for)
        row.insert(index+2, score_against)
        row.insert(index+3, overs_against)
        return row

    def get_dataframe(self) -> pd.DataFrame:
        """
        Extracts the table standings in the IPL of a given year
        ### Parameters
        season: the year
        """
        url = f'https://www.iplt20.com/points-table/men/{self.season}'
        self.driver.get(url)
        time.sleep(5)
        response = self.driver.page_source.encode('utf-8').strip()
        df = pd.DataFrame(columns=self.columns)
        soup = BeautifulSoup(response, 'html.parser')
        positions = soup.find_all('tr', class_='team0 ng-scope')
        for index, position in enumerate(positions):
            team = position.find('h2', class_='ih-pt-cont mb-0 ng-binding').text
            values = position.find_all('td', class_='ng-binding')
            row = self.get_values(values)
            row = self.extract(7, row)
            row[0] = re.sub(r"\s+", '', row[0])
            row.insert(0, self.season)
            row.insert(2, team)
            qualified = self.get_qualifiers(index)
            row.append(qualified)
            winner = self.get_winner(team, self.season)
            row.append(winner)
            df.loc[index] = row
        return df

    def save_csv(self, df: pd.DataFrame, season: int) -> None:
        df.to_csv(f"Datasets/IPL_Table_{season}.csv", header=True, index=False)
        print(f"The .csv file for the {season} season has successfully been created.")

for season in seasons:
    table = IPL(season=season)
    df = table.get_dataframe()
    table.save_csv(df=df, season=season)