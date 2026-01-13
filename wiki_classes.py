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

class WikiScraper:
    """
    Scraper for fetching wiki data. 
    Handles network requests, local file read mode, and error handling.
    """
    def __init__(self, base_url='https://minecraft.wiki/w', language='en', use_local_html_file_instead=False):
        self.url = base_url
        self.lang = language 
        self.local_file = use_local_html_file_instead
        
        #Ensuring that url doesn't end with a slash
        if self.url.endswith('/'):
            self.url = self.url[:-1]

    def get_article(self, phrase):
        """
        Fetches html and returns a WikiArticle object.
        Returns None if the article is not found.
        """
        html = self._get_html(phrase)

        if html:
            return WikiArticle(phrase, html)
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


