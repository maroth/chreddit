from dataAccess import DataAccess
from models import Submission
import requests
import traceback
import re
import os
from bs4 import BeautifulSoup


class WatsonScraper:
    dataAccess = DataAccess()
    watson_url = 'https://www.watson.ch'

    def scrape(self):
        page = requests.get(self.watson_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = ['https://www.watson.ch' + (a.get('href')) for a in soup.find_all("a", class_="teaserlink") if not "doubleclick" in a.get('href')]
        for link in links:
            if '/schweiz/' not in link:
                continue
            link_page = requests.get(link)
            link_soup = BeautifulSoup(link_page.content, 'html.parser')
            title = link_soup.find('h2', class_="maintitle").get_text()

            print ('saving new watson entry: ' + link)
            try:
                submission = Submission(
                    title = title,
                    description = '',
                    url = link,
                    feed_url = self.watson_url,
                    feed_name= 'Watson')
                self.dataAccess.save(submission)
                print(submission)
            except:
                traceback.print_exc()

