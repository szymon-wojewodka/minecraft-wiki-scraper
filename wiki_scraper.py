import argparse
from wiki_classes import WikiDispatcher

def validate_arguments(args, parser):
    """
    Checks for logical errors within arguments.
    Throws a parser error if combination of arguments is not valid.
    """
    actions = [
        args.summary,
        args.table,
        args.count_words,
        args.auto_count_words
    ]

    if not any(actions):
        parser.error('No actions specified, check --help')

    if (args.table is None) != (args.number is None):
        parser.error('Arguments --table and --number depend on each other. '
                     'You must provide both or neither.')

    if args.first_row_is_header and (args.table is None):
        parser.error('Argument --first-row-is-number requires --table.')

    has_cw = args.count_words is not None
    has_analyze = args.analyze_relative_word_frequency
    has_mode = args.mode is not None
    has_count = args.count is not None
    has_chart = args.chart is not None

    if not (has_analyze == has_mode == has_count):
        parser.error('Arguments --analyze-relative-word-frequency, --mode and '
                     '--count form a set. Provide all of them or none.')

    if has_analyze and not has_cw:
        parser.error('Analyzing relative frequency requires --count-words.')

    if has_chart and not (has_cw and has_analyze):
        parser.error('Argument --chart requires --count-words, '
                     '--analyze-relative-word-frequency, --mode and --count.')

    has_acw = args.auto_count_words is not None
    has_depth = args.depth is not None
    has_wait = args.wait is not None

    if not (has_acw == has_depth == has_wait):
        parser.error('Arguments --auto-count-words, --depth and --wait form '
                     'a set. Provide all of them or none.')

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

    args = parser.parse_args()

    validate_arguments(args, parser)

    return args

def main():
    args = parse_arguments()

    dispatcher = WikiDispatcher(args)
    dispatcher.run()
    
if __name__ == '__main__':
    main()
