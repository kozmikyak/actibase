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

comm_base = base.xpath('.//div[@class="cal_item comm_item"]')
for c in comm_base:
    print(c.xpath('.//h3/a/text()'))

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


class MNCommsScraper(Scraper):

    def scrape(self):
        for c in comm_base:
            print(c.xpath('.//h3/a/text()'))
        for c in comm_base:
            m = {}
            m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
            print(c.xpath('.//h3/*'))
            title = c.xpath('.//h3/a/text()')
            if len(title) == 0:
                continue
            else:
                m['title'] = title[0]
            m['link'] = c.xpath('.//h3/a/@href')[0]
            info_div = c.xpath('.//div[@class="calendar_p_indent"]')[0]
            print('one info div')
            if info_div is not None:
                info_list = info_div.xpath('.//text()')
                if info_list[0] == 'Room: ':
                    m['room'] = info_list[1]
                if info_list[1] == 'Chair: ':
                    chair = info_list[2]
                    if ',' in chair:
                        chairs = chair.replace('\xa0', '').split(',')
                        nchairs = []
                        for chair in chairs:
                            if chair.startswith('Rep.') or chair.startswith('Sen.'):
                                cname = pull_middle_name(chair[4:])
                                nchairs.append(cname.strip())
                        m['chair'] = nchairs
                    elif chair.startswith('Rep.') or chair.startswith('Sen.'):
                        cname = pull_middle_name(chair[4:].strip())
                        m['chair'] = [cname.strip()]
                if info_list[2] == 'Chair: ':
                    chair = info_list[3]
                    if ',' in chair:
                        chairs = chair.replace('\xa0', '').split(',')
                        nchairs = []
                        for chair in chairs:
                            if chair.startswith('Rep.') or chair.startswith('Sen.'):
                                cname = pull_middle_name(chair[4:])
                                nchairs.append(cname.strip())
                        m['chair'] = nchairs
                    elif chair.startswith('Rep.') or chair.startswith('Sen.'):
                        cname = pull_middle_name(chair[4:].strip())
                        m['chair'] = [cname.strip()]
                if info_list[4] == 'Agenda: ':
                    m['agenda'] = info_list[5]

            if len(m['notice']) > 0:
                m['notice'] = m['notice'][0]
            else:
                m['notice'] = 'N/A'
            ppr(m)
            date = c.xpath('.//p/b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                ppr(m)
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)

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

