k
import sys
import os
import re
import random
import time

from io import BytesIO 
from PIL import Image

import requests
from datetime import datetime
from pprint import pprint as ppr

from lxml import html
from selenium import webdriver as wd
import facebook, twitter

from xvfbwrapper import Xvfb

#sys.path.insert(0, '/websrv/actibase')
sys.path.insert(0, '/home/nkfx/ScreamFreely/MnActivist/server')
import mnauth as KF

LINKS = [
    'https://mnactivist.org/p/Minneapolis',
    'https://mnactivist.org/p/Saint-Paul',
    'https://mnactivist.org/p/Minnesota',
]

mnact = {'access_token': KF.fb_token, 'id': KF.fb_id}

start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()
print("Xvfb started")

br = wd.Chrome()
br.set_window_size(800, 1000)

graph = facebook.GraphAPI(mnact['access_token'], 2.7)
api = twitter.Api(consumer_key=KF.tw_ckey,
                  consumer_secret=KF.tw_csecret,
                  access_token_key=KF.tw_tkey,
                  access_token_secret=KF.tw_tsecret)


for link in LINKS:
    wait = random.randrange(174, 348, 16)
    br.get(link)
    timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.now())
    name = link.split('/')[-1:]
    name = ('-').join(name)
    picName = name + timestamp + '.png'
    time.sleep(5)
    br.get_screenshot_as_file('testShot.png') 
    screen = br.get_screenshot_as_png()
    box = (100, 100, 700, 850)
    im = Image.open(BytesIO(screen))
    region = im.crop(box)
    region.save(picName, 'PNG', optimize=True, quality=95)
    print('Picture save: {0}'.format(picName))
    msg = "More at MnActivist.org"
    image=open(picName, 'rb')
    graph.put_photo(image=image, album_path= mnact['id'] + "/photos", caption=msg)
    name = name.replace('-', ' ')
    api.PostUpdate('Upcoming events for {0}'.format(name), media=image)
    time.sleep(wait)


    
br.close() 
xvfb.stop()
os.system("pkill Xvfb")
#os.system("rm *.png")


