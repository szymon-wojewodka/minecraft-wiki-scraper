import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

class WikiArticle:
    """
    Represents a single wiki article fetched with scraper.
    Parses HTML content using BeautifulSoup to extract required data.
    """
    def __init__(self, title, html):
        self.title = title
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_summary(self):
        #Some articles have an empty mw-parser-output
        #before the one with actual content
        div_content = self.soup.select_one(
            'div.mw-content-ltr.mw-parser-output'
        )

        #If div with 2 classes required is not found, we use find just in case
        if not div_content:
            div_content = self.soup.find('div', class_='mw-parser-output')

        if not div_content:
            return 'Content not found' 

        p = div_content.find('p', recursive=False)

        if p:
            return p.get_text().strip()

        return 'Summary not found'

class WikiScraper:
    """
    Scraper for fetching wiki data. 
    Handles network requests, local file read mode, and error handling.
    """
    def __init__(self, base_url='https://minecraft.wiki/w', language='en', use_local_html_file_instead=False):
        self.url = base_url
        self.lang = language 
        self.local_file = use_local_html_file_instead
        self.cache = {}
        #Ensuring that url doesn't end with a slash
        if self.url.endswith('/'):
            self.url = self.url[:-1]

    def get_article(self, phrase):
        """
        Fetches html and returns a WikiArticle object.
        Returns None if the article is not found.
        """
        if phrase in self.cache:
            return self.cache[phrase]

        html = self._get_html(phrase)

        if html:
            article = WikiArticle(phrase, html)
            self.cache[phrase] = article
            return article

        return None

    def _get_html(self, phrase):
        """
        Private method to fetch raw HTML content.
        Based on attribute local_file decides whether to fetch from local file or web.
        """
        formatted_phrase = phrase.replace(' ', '_')

        if self.local_file:
            path = os.path.join('test_files', f'{formatted_phrase}.html')
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    html_page = file.read()
                    return html_page
            return None

        url = f'{self.url}/{formatted_phrase}'

        try:
            r = requests.get(url)
            r.raise_for_status() # Raises HTTPError for bad responses
            # Handling "Soft 404" (placeholder page)
            if 'There is currently no text in this page' in r.text: 
                return None
            return r.text

        except requests.exceptions.RequestException as e:
            print(f'Error fetching {url}: {e}')
            return None

class WikiDispatcher:
    """
    Central controller for interpreting parsed arguments and dispatches
    execution to appropiate handler methods.
    """
    def __init__(self, args):
        self.args = args
        self.scraper = WikiScraper()

    def run(self):
        """
        Execution logic, checks active flags and routes the flow to
        specific handling methods.
        """
        if self.args.summary is not None:
            self.handle_summary()

    def handle_summary(self):
        phrase = self.args.summary

        if not phrase.strip():
            print("The phrase used for summary is empty.")
            return
        
        article = self.scraper.get_article(phrase)

        if article:
            print(article.get_summary())
        else:
            print(f'Summary error: Article "{phrase}" not found.')
