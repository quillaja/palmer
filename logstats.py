import sys
import json

import settings

LOGPATHFMT = settings.ARCHIVE_PATH + '{}.log'


def process_date(date, fmt='text'):
    ''' Process a date given as a string in 'YYYY-MM-DD' format. Can return a
    printout of a summary or a json string of the data from the summary.'''

    success = 0
    failure = 0
    noscrape = 0
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

    if fmt == 'text':
        return '\n{}\nRun: {} times\tScrapes: {}\tNo scrape: {}\nSuccess: {} ({:.1f}%)\tFailure: {} ({:.1f}%)'.format(
            date, runs, scrapes, noscrape, success, 100.0 * success / scrapes,
            failure, 100.0 * failure / scrapes)
    elif fmt == 'json':
        rdict = {
            'date': date,
            'runs': runs,
            'scrapes': scrapes,
            'noscrapes': noscrape,
            'success': success,
            'failure': failure
        }
        return json.dumps(rdict)


def main():
    try:
        date = sys.argv[1]
        process_date(date)
    except IndexError:
        print('no date provided')
        return
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
