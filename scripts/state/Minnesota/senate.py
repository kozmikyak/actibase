from pupa.scrape import Scraper
from pupa.scrape import Event

import re, os
import datetime

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb

import requests
from lxml import html
from lxml.etree import tostring

import pytz

tz = pytz.timezone("US/Central")

#from html2text import html2text

start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()

br = wd.Chrome()
br.get('https://www.leg.state.mn.us/cal?type=all')
sleep(30)
base = html.fromstring(br.page_source)
xvfb.stop()
os.system("pkill Xvfb")

house_base = base.xpath('.//div[@class="cal_item house_item"]')
senate_base = base.xpath('.//div[@class="cal_item senate_item"]')
comm_base = base.xpath('.//div[@class="cal_item comm_item"]')

format1 = "%A, %B %d, %Y %I:%M %p"
format2 = "%A %B %d, %Y - "
format3 = "%m/%d/%y"

def pull_middle_name(name):
    stopwords = ['Jr.', 'Sr.', 'III']
    name = name.strip().split(' ')
    print('NAME: ', name)
    if not any(sw in name for sw in stopwords) and len(name) == 3:
        name.pop(1)
        name = ' '.join(name)
    else:
        name = ' '.join(name)
    print('NAME: ', name)
    return name


class MNSenateScraper(Scraper):

    def scrape(self):
        for c in senate_base:
            m = {}
            m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
            link = c.xpath('.//h3/a/@href')
            print('top link: ', c.xpath('.//h3/*'))
            if len(link) > 0:
                m['link'] = c.xpath('.//h3/a/@href')[0]
                m['title'] = c.xpath('.//h3/a/text()')[0]                
            else:
                m['link'] = 'https://www.leg.state.mn.us/cal?type=all'
                m['title'] = c.xpath('.//h3/text()')[0]
            print('top link 2: ', c.xpath('.//h3/text()'))
            info_div = c.xpath('.//div[@class="calendar_p_indent"]')
            if len(info_div) > 0:
                info_div = info_div[0]
                info_list = info_div.xpath('.//text()')
                nchairs = []
                agenda = False
                for il in info_list:
                    il = il.replace('\xa0', '')
                    if il.startswith(' and '):
                        il = il.replace(' and ', '')
                    if il.startswith('Room'):
                        m['room'] = il
                    if il.startswith('Rep.') or il.startswith('Sen.'):
                        cname = pull_middle_name(il[4:])
                        nchairs.append(cname.strip())
                    if agenda == True:
                        m['agenda'] = il
                    if il == 'Agenda: ':
                        agenda = True
                m['chair'] = nchairs
            if len(m['notice']) > 0:
                m['notice'] = m['notice'][0]
            else:
                m['notice'] = 'N/A'
            ppr(m)
            date = c.xpath('.//p/span/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                ppr(m)
                continue
            if 'or' in date[0]:
                date[0] = date[0].split('or')[0]
            m['date'] = datetime.datetime.strptime(date[0].replace('\xa0', ''), format1)
            ppr(m)
            if not 'room' in m.keys():
                print('oops')
                m['room'] = 'Senate in session'
            event = Event(name=m['title'],
                          start_date=tz.localize(m['date']),
                          location_name=m['room'] 
            )

            if len(m['notice']) > 0:
                pass
            event.add_committee(m['title'])
            event.add_source(m['link'])
            for chair in m['chair']:
                event.add_person(name=chair, note="Chair")
            yield event
        
