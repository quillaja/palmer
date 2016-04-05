#!/usr/bin/python
import sys
import time

import ephem
import requests

def log(msg):
    '''write to log file'''
    
    logfile = '/home/quillaja/static.quillaja.net/palmer/scrape.log'
    datefmt='%Y-%d-%m %H:%M:%S'
    fmt='%s\t%s\n'
    with open(logfile, 'a') as f:
        f.write(fmt % (time.strftime(datefmt), msg))

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

def sun(twilight='naut'):
    """Use PyEphem to calculate sunrise and sunset for the current day."""
    
    #pyephem requires horizon angle as a string
    horizons = {
        'civil': '-6',
        'naut': '-12',
        'astro': '-18'
    }
    
    portland = ephem.Observer()
    portland.horizon = horizons[twilight] #-6, -12, -18: civil, nautical, astronomical
    portland.elevation = 3500 #3500 meters (ie Hood summit)
    portland.lat, portland.lon = '45.37', '-121.70' #Hood summit 45.373505,-121.6962728
    portland.date = time.strftime('%Y/%m/%d') + ' 19:00:00' #today at noon PT, in UTC

    srise = portland.previous_rising(ephem.Sun(), use_center=True) #returns UTC
    sset = portland.next_setting(ephem.Sun(), use_center=True) #returns UTC
    return (ephem.localtime(srise).hour, ephem.localtime(sset).hour + 1)

def is_between_twilight(sun_rise_set):
    """Test if current hour is between sunrise and sunset."""
    srise, sset = sun_rise_set
    curhour = time.localtime().tm_hour
    return srise <= curhour <= sset
    
def scrape():
    """
    Does the scraping.
    """
    t = str(int(time.time()))
    url = 'http://www.timberlinelodge.com/wp-content/themes/Jupiter-child/cams/palmerbottom.jpg?nocache=' + t
    filename = '/home/quillaja/static.quillaja.net/palmer/img/palmer_%s.jpg' % t
    
    # attempt to get url up to 2 times, with 60 seconds between each attempt
    r, tries = do(lambda: requests.get(url), 2, lambda r: len(r.content) > 30000, 60)
    
    if r:
        with open(filename, 'wb') as f:
            f.write(r.content)
        
        log('Success (%s)' % tries)
    else:
        log('Failure (%s)' % tries)
    
    
def main():
    # do actual scraping only bewteen astronomical twilight sunrise and sunset, not at night
    sun_hours = sun('astro')
    if True:#is_between_twilight(sun_hours):
        log(sun_hours)
        scrape()
    else:
        log('No scrape: %s' % sun_hours)
        
if __name__ == '__main__':
    main()