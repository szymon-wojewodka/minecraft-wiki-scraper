import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from collections import Counter
import wordfreq
import matplotlib.pyplot as plt

class WikiArticle:
    """
    Represents a single wiki article fetched with scraper.
    Parses HTML content using BeautifulSoup to extract required data.
    """
    def __init__(self, title, html):
        self.title = title
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def _get_div_content(self):
        #Some articles have an empty mw-parser-output
        #before the one with actual content
        div_content = self.soup.select_one(
            'div.mw-content-ltr.mw-parser-output'
        )

        #If div with 2 classes required is not found, we use find just in case
        if not div_content:
            div_content = self.soup.find('div', class_='mw-parser-output')

        if not div_content:
            return None

        return div_content

    def get_summary(self):
        div_content = self._get_div_content()

        if div_content is None:
            return 'Content not found'

        p = div_content.find('p', recursive=False)

        if p:
            return p.get_text().strip()

        return 'Summary not found'

    def get_table(self, number, row_header):
        div_content = self._get_div_content()

        if div_content is None:
            return 'Content not found'

        tables = div_content.find_all('table', limit=number)

        if len(tables) < number:
            raise IndexError(f'Table index {number} out of range (found {len(tables)} tables).')

        target = tables[number - 1]

        data = []
        rows = target.find_all('tr')

        for row in rows:
            row_data = []
            cells = row.find_all(['th','td'])

            for cell in cells:
                row_data.append(cell.get_text(strip=True))

            if row_data:
                data.append(row_data)

        if not data:
            raise ValueError('Table is empty.')

        df = pd.DataFrame(data)

        if row_header:
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header

        if not df.empty:
            df = df.set_index(df.columns[0])

        return df

    def get_word_count(self):
        div_content = self._get_div_content()

        if div_content is None:
            raise ValueError('Article content not found.')

        text = div_content.get_text(' ', strip=True)
        candidates = re.findall(r'\w+', text.lower())
        words = [word for word in candidates if word.isalpha()]

        return Counter(words)

    def get_links(self):
        div_content = self._get_div_content()

        if div_content is None:
            return [] 

        links = []
        for a in div_content.find_all('a', href=True):
            href = a['href']
            if href.startswith('/w/') and 

class WikiScraper:
    """
    Scraper for fetching wiki data. 
    Handles network requests, local file read mode, and error handling.
    """
    def __init__(self, base_url='https://minecraft.wiki/w', use_local_html_file_instead=False):
        self.url = base_url
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

        if self.args.table is not None:
            self.handle_table()

        if self.args.count_words is not None:
            self.handle_count_words()

        if self.args.analyze_relative_word_frequency:
            self.handle_analyze()

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

    def handle_table(self):
        phrase = self.args.table

        if not phrase.strip():
            print("The phrase used for table is empty.")
            return

        article = self.scraper.get_article(phrase)

        if article:
            try:
                df = article.get_table(
                    self.args.number, self.args.first_row_is_header
                )
                print(df)
                filename = f'{phrase}.csv'
                df.to_csv(filename, encoding='utf-8')

                occurence_table = df.stack().value_counts().to_frame('Count')
                print(occurence_table)
            except IndexError as e:
                print(f'Error: {e}')
            except ValueError as e:
                print(f'Data Error: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')
        else:
            print(f'Table error: Article "{phrase}" not found.')

    def handle_count_words(self):
        phrase = self.args.count_words

        if not phrase.strip():
            print('The phrase used for count_words is empty.')
            return

        article = self.scraper.get_article(phrase)

        if article:
            try:
                article_counts = article.get_word_count()
                self._update_json(article_counts)
            except ValueError as e:
                print(f'Error: {e}')
            except Exception as e:
                print(f'Unexpected error: {e}')
        else:
            print(f'Count words error: Article "{phrase}" not found.')

    def _update_json(self, new_counts):
        json_file = 'word-counts.json'
        global_counts = Counter()

        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding = 'utf-8') as f:
                    data = json.load(f)
                    global_counts = Counter(data)
            except json.JSONDecodeError:
                print('JSON file corrupted, creating new one')

        updated_counts = global_counts + new_counts

        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(updated_counts, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving JSON file: {e}")

    def handle_analyze(self):
        json_file = 'word-counts.json'
        if not os.path.exists(json_file):
            print("No data found, run --count-words first.")
            return

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                wiki_data = json.load(f)
        except json.JSONDecodeError:
            print("JSON file with word count is corrupted.")
            return

        if not wiki_data:
            print("Database is empty.")
            return

        n = self.args.count
        mode = self.args.mode
        language = 'en'

        final_data = []


        if mode == 'article':
            sorted_wiki = sorted(wiki_data.items(), key=lambda item: item[1], reverse=True)[:n]
 
            for word, wiki_count in sorted_wiki:
                lang_freq = wordfreq.word_frequency(word, language)

                lang_val = lang_freq if lang_freq > 0 else None

                final_data.append({
                    "word": word,
                    "wiki_raw": wiki_count,
                    "lang_raw": lang_val
                })
        elif mode == 'language':
            top_lang_words = wordfreq.top_n_list(language, n)

            for word in top_lang_words:
                wiki_count = wiki_data.get(word, None)
                lang_freq = wordfreq.word_frequency(word, language)
 
                final_data.append({
                    "word": word,
                    "wiki_raw": wiki_count,
                    "lang_raw": lang_freq
                })
        df = pd.DataFrame(final_data)

        max_wiki = df['wiki_raw'].max()
        max_lang = df['lang_raw'].max()

        df['frequency in the article'] = df['wiki_raw'] / max_wiki
        df['frequency in wiki language'] = df['lang_raw'] / max_lang

        output_df = df[['word', 'frequency in the article', 'frequency in wiki language']]
        print(output_df.to_string(index=False))

        if self.args.chart:
            self._plot_chart(df, self.args.chart)

    def _plot_chart(self, df, filename):
        plot_data = df.fillna(0)
        words = plot_data['word']
        wiki_vals = pd.to_numeric(plot_data['frequency in the article'])
        lang_vals = pd.to_numeric(plot_data['frequency in wiki language'])
        x = range(len(words))
        width = 0.35
        plt.figure(figsize=(10, 6))

        plt.bar([i - width/2 for i in x], wiki_vals, width, label='Wiki Article', color='blue')
        plt.bar([i + width/2 for i in x], lang_vals, width, label='English Language', color='red')

        plt.xlabel('Words')
        plt.ylabel('Relative Frequency (Normalized)')
        plt.title('Frequency of words: Wiki vs English Language')
        plt.xticks(x, words, rotation=45) 
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(filename)

    def handle_auto_count(self):
        
