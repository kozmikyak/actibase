from pupa.scrape import Scraper
from pupa.scrape import Bill

import sys
import os
import re
import random
import time

from io import BytesIO 
from PIL import Image
from time import sleep
import requests
from datetime import datetime
from pprint import pprint as ppr

from lxml import html
from selenium import webdriver as wd
import facebook, twitter

from xvfbwrapper import Xvfb

#sys.path.insert(0, '/websrv/actibase')
sys.path.insert(0, '/home/nkfx/ScreamFreely/MnActivist/server')

file_url = 'https://lims.minneapolismn.gov'
base_url = 'https://lims.minneapolismn.gov/Reports/LatestActions'

ROWS = []


def start_xvfb():
    start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
    xvfb = Xvfb()
    os.system(start_cmd)
    xvfb.start()
    print("Xvfb started")
    return xvfb
    
def init_page(url):
    br = wd.Chrome()
    br.get(url)
    sleep(3)
    return br

def get_new_page(url):
    br = wd.Chrome()
    br.get(url)
    sleep(3)
    base = html.fromstring(br.page_source)
    br.close()
    print("\nBase obtained\n")
    return base

def get_page(br):
    base = html.fromstring(br.page_source)
    print("\nBase obtained\n")
    return base, br

def next_page(base, br):
    if base.xpath('.//*/li[@class="paginate_button next"]'):
        br.find_elements_by_xpath('.//*/li[@class="paginate_button next"]/a')[0].click()
        return br
    else:
        br = 'nada'
        return br

def get_rows(base):
    global ROWS
    table = base.xpath('.//*/table[@id="latestAction"]/tbody/*')
    for t in table:
        ROWS.append(t)
    
def close_page(br):
    br.close()

def stop_xvfb(xvfb):
    xvfb.stop()
    os.system("pkill Xvfb")

xvfb = start_xvfb()    
br = init_page(base_url)

for x in range(2):
    print(x)
    base, br = get_page(br)
    get_rows (base)
    next_page(base, br)
    if br == 'nada':
        break
    sleep(3)

close_page(br)
#print('Rows: ', ROWS)

DATA = []








for row in ROWS:
    d = {}
    cells = row.xpath('.//td')
    x = 0
    for c in cells:
        link = c.xpath('.//a/@href')
        link_text = c.xpath('.//a/text()')
        text = c.xpath('.//text()')
        if len(link_text) > 0:
            d[x] = (link_text[0], file_url + link[0])
        else:
            d[x] = ('text', text[0].replace('\xa0', '').replace('\n', ''))
        x+=1
    DATA.append(d)

#ppr(DATA)

for d in DATA:
    link = d[0]
    pdf = d[1]
    text = d[2][1]
    base = get_new_page(link[1])
    print(base.xpath('.//*/div[@class="col-md-12"]'))
    


stop_xvfb(xvfb)


"""   
class MinneapolisBillScraper(Scraper):

    def scrape(self):
        # needs to be implemented
        pass
"""
