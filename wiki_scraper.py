import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Minecraft Wiki scraper tool')

    # Summary arguments
    parser.add_argument(
        '--summary',
        type=str,
        metavar='PHRASE',
        help='Fetch summary for the specified phrase'
    )

    # Table arguments
    parser.add_argument(
        '--table',
        type=str,
        metavar='PHRASE',
        help='Fetch a table from the article (requires --number)'
    )

    parser.add_argument(
        '--number',
        type=int,
        metavar='NUMBER',
        help='Index of the table to extract (indexing starts from 1)'
    )

    parser.add_argument(
        '--first-row-is-header',
        action='store_true',
        help='Treat first row of the table as a header'
    )

    # Word counting and analysis arguments
    parser.add_argument(
        '--count-words',
        type=str,
        metavar='PHRASE',
        help='Count words in the specified article'
    )

    parser.add_argument(
        '--analyze-relative-word-frequency',
        action='store_true',
        help='Analyze frequency relative to Wiki language average '
        '(requires --count-words, --mode, --count)'
    )

    parser.add_argument(
        '--mode',
        type=str,
        choices=['article','language'],
        help='Analyze words sorted by most frequent language or article words'
    )

    parser.add_argument(
        '--count',
        type=int,
        metavar='NUMBER',
        help='Number of top words to display for analyzing'
    )

    parser.add_argument(
        '--chart',
        type=str,
        metavar='PATH',
        help='Generate a chart in a specified file path'
    )

    # Crawler arguments
    parser.add_argument(
        '--auto-count-words',
        type=str,
        metavar='PHRASE',
        help='Start crawler from the specified phrase (requires --depth, --wait)'
    )

    parser.add_argument(
        '--depth',
        type=int,
        metavar='NUMBER',
        help='Crawler recursion depth'
    )

    parser.add_argument(
        '--wait',
        type=int,
        metavar='SECONDS',
        help='Wait time between requests in seconds'
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    
if __name__ == '__main__':
    main()
