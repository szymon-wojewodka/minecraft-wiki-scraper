import sys
import os
from wiki_classes import WikiScraper

def run_integration_test():
    phrase = "Creeper"
    expected_snippet = "A creeper is a common hostile mob"
    file_path = os.path.join('test_files', f'{phrase}.html')
    if not os.path.exists(file_path):
        sys.stderr.write(f"Test file not found at {file_path}\n")
        sys.exit(1)

    try:
        scraper = WikiScraper(use_local_html_file_instead=True)
        article = scraper.get_article(phrase)

        if article is None:
            sys.stderr.write(f"Scraper returned None for phrase '{phrase}'.\n")
            sys.exit(1)

        summary = article.get_summary()

        if expected_snippet not in summary:
            sys.stderr.write("Summary content mismatch.\n")
            sys.stderr.write(f"Expected to find: '{expected_snippet}'\n")
            sys.stderr.write(f"Actual summary: '{summary}'\n")
            sys.exit(1)

    except Exception as e:
        sys.stderr.write(f"An unexpected exception occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    run_integration_test()
