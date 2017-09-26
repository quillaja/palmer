import time
from io import BytesIO #used StringIO in python2, BytesIO in python3
from PIL import Image

import ephem
import requests
import settings


def log(msg):
    '''write to log file'''

    fmt = '{0}\t{1}\n'
    with open(settings.ACTIVELOG_PATH, 'a') as f:
        f.write(fmt.format(time.strftime(settings.ACTIVELOG_DATEFMT), msg))


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

    for rval, i in ((func(), i) for i in range(1, times + 1)):
        if end(rval):
            return rval, i
        if i < times:
            time.sleep(pause)

    return None, i


def sun(twilight='nautical'):
    """Use PyEphem to calculate sunrise and sunset for the current day."""

    #pyephem requires horizon angle as a string
    horizons = {'civil': '-6', 'nautical': '-12', 'astronomical': '-18'}

    portland = ephem.Observer()
    portland.horizon = horizons[twilight]  #-6, -12, -18: civil, nautical, astronomical
    portland.elevation = settings.LOC_ELEV
    portland.lat, portland.lon = settings.LOC_LAT, settings.LOC_LON
    portland.date = time.strftime('%Y/%m/%d') + ' 19:00:00'  #today at noon PT, in UTC

    srise = portland.previous_rising(ephem.Sun(), use_center=True)  #returns UTC
    sset = portland.next_setting(ephem.Sun(), use_center=True)  #returns UTC
    return (ephem.localtime(srise).hour, ephem.localtime(sset).hour)


def is_between_twilight(sun_rise_set):
    """Test if current hour is between sunrise and sunset."""
    srise, sset = sun_rise_set
    curhour = time.localtime().tm_hour
    return srise <= curhour <= sset


def is_img_size(bytestring, width, height):
    """
    DEPRECATED
    Determines if the image, given as a string of bytes, is dimentions width x height.
    Uses PIL to read size from image.
    """
    strf = BytesIO(bytestring)
    img = Image.open(strf)
    return width == img.size[0] and height == img.size[1]

def isvalidimage(bytestring):
    """
    Determines if the image is valid or not, based on its dimensions and
    the content of the first row of the image. Valid image dimensions are in
    settings.VALID_IMG_DIMENSIONS and valid data is in settings.INVALID_IMG_DATA.
    """

    if len(bytestring) == 0:
        return False

    strf = BytesIO(bytestring)
    strf.seek(0)
    img = Image.open(strf)

    # test size
    if img.size != settings.VALID_IMG_DIMENSIONS:
        return False

    img_width = img.size[0]
    img_data = list(img.getdata())[0:img_width]
    bad_data = [settings.INVALID_IMG_DATA] * img_width

    # compare first row of data with generated bad data
    return img_data != bad_data


def scrape():
    """
    Does the scraping.
    """
    t = str(int(time.time()))
    url = settings.WEBCAM_URL.format(t)
    filename = settings.IMAGE_PATH.format(t)

    # set up headers
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':settings.USER_AGENT})

    # attempt to get url
    r = requests.get(url, headers=headers)

    #test image validity and write
    if (r is not None) and isvalidimage(r.content):
        with open(filename, 'wb') as f:
            f.write(r.content)

        log('Success')
    else:
        log('Failure (invalid image or no data)')


def main():
    try:
        # do actual scraping only bewteen nautical twilight sunrise and sunset, not at night
        sun_hours = sun(settings.TWILIGHT_TYPE)
        if is_between_twilight(sun_hours):
            scrape()
        else:
            log('No scraping {0}:00 to {1}:00.'.format(sun_hours[1] + 1,
                                                       sun_hours[0]))
    except Exception as e:
        log('Failure (other exception)')
        print(e)


if __name__ == '__main__':
    main()
