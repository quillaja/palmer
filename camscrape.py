#!/usr/bin/python
import sys
import time

import requests

def do(func, times, end=None, pause=0):
    """
    Does a task a specificed number of times, or until the end
    condition is met, pausing between each attempt.
     func: a function that returns a value.
     times: the max number of times to run the function.
     end: a function that takes 1 parameter, the return value of func(), and returns true or false.
     pause: number of seconds to pause between attempts.
    """
    if end is None:
        end = lambda x: False

    for rval, i in ((func(), i) for i in xrange(1, times + 1)):
        if end(rval):
            return rval, i
        if i < times:
            time.sleep(pause)

    return None, i

def scrape():
    t = str(int(time.time()))
    tformat = time.strftime('%Y-%m-%d_%H:%M:%S')
    url = 'http://www.timberlinelodge.com/wp-content/themes/Jupiter-child/cams/palmerbottom.jpg?nocache=' + t
    filename = '/home/quillaja/static.quillaja.net/palmer/img/palmer_%s.jpg' % t
    
    # attempt to get url up to 2 times, with 60 seconds between each attempt
    r, tries = do(lambda: requests.get(url), 2, lambda r: len(r.content) > 30000, 60)
    
    # r = requests.get(url)
    # r.raise_for_status()
    # if len(r.content) < 50000:
    #     raise IOError('Data recieved too short')
    if r:
        with open(filename, 'wb') as f:
            f.write(r.content)
        print('%s: Completed successfully in %s tries.' % (tformat, tries))
    else:
        sys.stderr.write('%s: %s attempts to scrape failed.' % (tformat, tries))
        #raise IOError('Attempts to scrape t = %s failed.' % t)

# do actual scraping only bewteen 5am and 10pm, not at night
if 5 <= time.localtime().tm_hour <= 22:
    scrape()