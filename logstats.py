import sys

import settings

LOGPATHFMT = settings.ARCHIVE_PATH + '{}.log'


def main():
    try:
        date = sys.argv[1]
    except IndexError:
        print('no date provided')
        return

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
            '\n{}\nRun: {} times\tScrapes: {}\tNo scrape: {}\nSuccess: {} ({:.1f}%)\tFailure: {} ({:.1f}%)'.format(
                date, runs, scrapes, noscrape, success, 100.0 * success /
                scrapes, failure, 100.0 * failure / scrapes))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
