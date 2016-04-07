#!/usr/bin/python
import sys
import time
from PIL import Image
import StringIO

import ephem
import requests

def log(msg):
    '''write to log file'''
    
    logfile = '/home/quillaja/static.quillaja.net/palmer/scrape.log'
    datefmt='%Y-%d-%m %H:%M:%S'
    fmt='{0}\t{1}\n'
    with open(logfile, 'a') as f:
        f.write(fmt.format(time.strftime(datefmt), msg))

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
    return (ephem.localtime(srise).hour, ephem.localtime(sset).hour)

def is_between_twilight(sun_rise_set):
    """Test if current hour is between sunrise and sunset."""
    srise, sset = sun_rise_set
    curhour = time.localtime().tm_hour
    return srise <= curhour <= sset

def is_img_size(bytestring, width, height):
    """
    Determines if the image, given as a string of bytes, is dimentions width x height.
    Uses PIL to read size from image.
    """
    strf = StringIO.StringIO(bytestring)
    img = Image.open(strf)
    return width == img.size[0] and height == img.size[1]
    
def scrape():
    """
    Does the scraping.
    """
    t = str(int(time.time()))
    url = 'http://www.timberlinelodge.com/wp-content/themes/Jupiter-child/cams/palmerbottom.jpg?nocache={}'.format(t)
    filename = '/home/quillaja/static.quillaja.net/palmer/img/palmer_{}.jpg'.format(t)
    
    # attempt to get url
    r = requests.get(url)
    
    #test image size, and write
    if (r is not None) and is_img_size(r.content, 640, 480):
        with open(filename, 'wb') as f:
            f.write(r.content)
        
        log('Success')
    else:
        log('Failure')
    
    
def main():
    # do actual scraping only bewteen nautical twilight sunrise and sunset, not at night
    sun_hours = sun('naut')
    if is_between_twilight(sun_hours):
        scrape()
    else:
        log('No scraping {0}:00 to {1}:00.'.format(sun_hours[1] + 1, sun_hours[0]))
        
if __name__ == '__main__':
    main()
    