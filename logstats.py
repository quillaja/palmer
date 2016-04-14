import argparse
import sys

LOGARCHIVE = '/home/quillaja/static.quillaja.net/palmer/img/archive/'
LOGPATHFMT = LOGARCHIVE + '{}.log'


def process_log():
    pass


def main():
    if not sys.argv[1]:
        print('no date provided')
        return

    date = sys.argv[1]
    success = 0
    failure = 0
    noscrape = 0
    try:
        with open(LOGPATHFMT.format(date), 'r') as logf:
            for line in logf:
                if 'Success' in line:
                    success += 1
                elif 'Failure' in line:
                    failure += 1
                elif 'No scraping' in line:
                    noscrape += 1

        runs = success + failure + noscrape
        scrapes = success + failure
        print(
            '\n{}\nRun: {} times\tNo scrape: {}\nSuccess: {} ({})\tFailure: {} ({})'.format(
                date, runs, noscrape, success, 100.0 * success / scrapes,
                failure, 100.0 * failure / scrapes))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
