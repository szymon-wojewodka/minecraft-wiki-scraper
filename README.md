# Minecraft Wiki Scraper & Analyzer

## Overview
A command-line tool designed to extract, aggregate, and analyze data from the Minecraft Wiki. Developed as an academic project to demonstrate Object-Oriented Programming principles, web scraping, and data analysis. The application features a modular architecture that separates network requests, HTML parsing, and command dispatching.

Alongside basic web scraping functionalities, the project includes an automated web crawler and a linguistic analysis module that compares domain-specific terminology frequencies with general English language patterns.

## Features
* **Summary Extraction:** Retrieves and sanitizes the introductory paragraph of any specified wiki article.
* **Table Export:** Locates a specific HTML table by its index, parses the tabular data using Pandas, and exports it directly to a CSV file.
* **Word Counting:** Processes article text to extract alphanumeric words and maintains a persistent count across multiple runs in a local JSON database.
* **Automated Crawler:** Utilizes a breadth-first search (BFS) algorithm to autonomously navigate through internal wiki links up to a specified depth, with built-in rate limiting to prevent server overload.
* **Linguistic Analysis & Visualization:** Normalizes and compares word frequencies from the scraped dataset against standard English language distributions, generating visual bar charts.

## Tech Stack
* **Language:** Python 3
* **Web Scraping:** BeautifulSoup4, Requests
* **Data Manipulation:** Pandas
* **Data Visualization:** Matplotlib
* **Linguistics:** wordfreq
* **Standard Libraries:** argparse, collections, json, re

## Installation

1. Clone the repository to your local machine.
2. It is recommended to use a virtual environment:

    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install the required dependencies:

    pip install -r requirements.txt

## Usage Examples

The tool is operated via the command line. Below are examples of how to use its core functionalities.

**Fetch an article summary:**

    python wiki_scraper.py --summary "Creeper"

**Extract a table to CSV:**
Extracts the second table from the "Block" article, treating the first row as a header.

    python wiki_scraper.py --table "Block" --number 2 --first-row-is-header

**Count words in an article:**

    python wiki_scraper.py --count-words "Diamond"

**Run the automated web crawler:**
Starts at "Redstone", crawls up to 2 links deep, and waits 1 second between requests.

    python wiki_scraper.py --auto-count-words "Redstone" --depth 2 --wait 1

**Analyze word frequencies and generate a chart:**
Analyzes the top 10 words, sorted by wiki frequency, and saves a chart.

    python wiki_scraper.py --analyze-relative-word-frequency --mode article --count 10 --chart output.png

## Testing
The project includes unit and integration testing setups. Scraper classes are designed to accept local HTML files (via the `use_local_html_file_instead` flag) to facilitate offline testing without making real HTTP requests.
