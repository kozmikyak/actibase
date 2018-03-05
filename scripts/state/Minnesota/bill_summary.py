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

base_url = 'http://www.house.leg.state.mn.us/hrd/billsum.aspx'


def get_page(url):
    start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
    xvfb = Xvfb()
    os.system(start_cmd)
    xvfb.start()
    print("Xvfb started")
    br = wd.Chrome()
    br.get(url)
    base = html.fromstring(br.page_source)
    print("\n\n\nBase obtained\n\n\n")
    br.close()
    xvfb.stop()
    os.system("pkill Xvfb")
    return base

base = get_page(base_url)
next_link = base.xpath('.//*/a[@class="HRDNext"]/@href')
table = base.xpath('.//*/table[@id="HRDTable"]/tbody/tr')

for t in table:
    cells = t.xpath('.//td')
    data = []
    for c in cells:
        d = {}
        link = c.xpath('.//a/@href')
        text = c.xpath('.//text()')
        if not text[0] == '\xa0':
            d['t'] = text[0]
            if len(link) > 0:
                d['l'] = link[0]
            data.append(d)
        else:
            continue

    for d in data:
        blink = data[0]
        pdf_doc = data[1]
        summary = data[2]
        if len(d) > 3:
            all_versions = data[3]
        print('\n\n')
        bill = {}
        bill['number'] = blink["t"]
        bill['link'] = blink["l"]
        bill['text'] = pdf_doc["l"]
        bill['status'] = pdf_doc["t"]
        bill['summary'] = summary["t"]
        nbase = get_page(bill['link'])
        
        ppr(bill)
        print('\n\n')
