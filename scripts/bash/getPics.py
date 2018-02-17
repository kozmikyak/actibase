import sys
import os
import django
import re
import random
import time

sys.path.append('/websrv/actibase/mnactivist/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MnActivist.settings'
django.setup()

import StringIO
from PIL import Image

import requests
from datetime import datetime
from pprint import pprint as ppr

from lxml import html
from selenium import webdriver as wd
import facebook

from xvfbwrapper import Xvfb

LINKS = [
    'https://mnactivist.org/#!/city/Minneapolis',
    'https://mnactivist.org/#!/city/Saint_Paul',
    'https://mnactivist.org/#!/state/Saint_Paul',
]

mnact = {'access_token': 'EAAShqFyQGf4BADay1SltU6Nrgnr4JDYUbkBz1PrKdAv742rZCOgcr1LkTYJgHGcUiMo3pHYKi1pAKjlOPd1DamgF5NmrO8TfdrJSOPTwttfdeZBv5gnplrZBWKSNTVplJ5NKWWI4sEVHZCqzJdjQpnxG8FEWtPSeWFENlN5WAwZDZD', 'id': '643301685878275'}

start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()

print("Xvfb started")

br = wd.Chrome()
graph = facebook.GraphAPI(mnact['access_token'], 2.7)
br.set_window_size(1250, 1080)



for link in LINKS:
    wait = random.randrange(174, 348, 16)
    br.get(link)
    timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.now())
    name = link.split('/')[-2:]
    if name[0] == 'city':
        msg = "The {0} of {1}'s Agenda Update. More info at MnActivist.org".format(name[0], name[1].replace('_', '').replace('Saint', 'St.'))
    elif name[0] == 'state':
        msg = "The {0} of Minnesota's Legislative Agenda Update. More info at MnActivist.org".format(name[0], name[1].replace('_', '').replace('Saint', 'St.'))
    else:
        msg = "More info at MnActivist.org"
    picName = ('-').join(name) + timestamp + '.png'
    time.sleep(5)
    br.get_screenshot_as_file('testShot.png') 
    screen = br.get_screenshot_as_png()
    box = (225, 180, 1000, 1000)
    im = Image.open(StringIO.StringIO(screen))
    region = im.crop(box)
    region.save(picName, 'PNG', optimize=True, quality=95)
    print('Picture save: {0}'.format(picName))
    graph.put_photo(image=open(picName, 'rb'), album_path= mnact['id'] + "/photos", caption=msg)    
    time.sleep(wait)


br.close()
xvfb.stop()
os.system("pkill Xvfb")
os.system("rm *.png")


