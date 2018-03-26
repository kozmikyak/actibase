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


class MNHouseScraper(Scraper):

    def scrape(self):
        for c in house_base:
            m = {}
            m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
            links = c.xpath('.//h3/a/@href')            
            if len(links) > 0:
                m['cmt'] = c.xpath('.//h3/a/text()')[0]
                m['link'] = c.xpath('.//h3/a/@href')[0]
                title = c.xpath('.//h3/text()')[0]
                if title == 'Agenda:':
                    m['title'] = c.xpath('.//h3/a/text()')[0]
                else:
                    m['title'] = c.xpath('.//h3/text()')[0]
                
            else:
                m['title'] = c.xpath('.//h3/text()')[0]
                m['link'] = None
            info_div = c.xpath('.//*[@class="calendar_p_indent"]')
            if len(info_div) == 0:
                pass
            else:
                info_div = info_div[0]
            print('Info Div: ', info_div)
            if len(info_div) > 0:
                info_list = info_div.xpath('.//text()')
                info_links = info_div.xpath('.//*/@href')
                print("info links: ", info_links)
                info_list = [x.replace('\n', '').strip() for x in info_list]
                info_list = [x for x in info_list if len(x) > 0]
                print('Info list: ', info_list)
                if info_list[0].startswith('Room:'):
                    m['room'] = info_list[1]
                else:
                    m['room'] = 'n/a'
                if len(info_list) > 2:
                    if info_list[2].startswith('Chair:'):
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
                else:
                    m['chair'] = None
            
            bill_rows = c.xpath(('.//*/table[@class="cal_bills"]/tbody/tr'))
            print('Bills: ', bill_rows)
            bills = []
            for brs in bill_rows:
                cells = brs.xpath('.//td')
                if len(cells) == 3:
                    b = {}
                    b['bill'] = cells[0].xpath('.//text()')[0]
                    b['author'] = cells[1].xpath('./text()')[0]
                    b['summary'] = cells[2].xpath('./text()')[0]
                    bills.append(b)
            if len(m['notice']) > 0:
                m['notice'] = m['notice'][0]
            else:
                m['notice'] = 'N/A'
            date = c.xpath('.//p/b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)

            if 'House Meets in Session' in m['title']:
                m['room'] = 'State leg'
                m['cmt'] = 'Minnesota House of Representatives'
                m['chair'] = None
                m['link'] = 'https://www.leg.state.mn.us/cal?type=all'
            event = Event(name=m['title'],
                          start_date=tz.localize(m['date']),
                          location_name=m['room'] 
            )
            if len(bills) > 0:
                for bill in bills:
                    nbill = event.add_agenda_item(description=bill['summary'])
                    nbill.add_bill(bill['bill'].replace('HF', 'HF '))
            if len(m['notice']) > 0:
                pass
            event.add_committee(m['cmt'])
            if m['link'] is not None:
                event.add_source(m['link'])
            if m['chair'] is not None:
                for chair in m['chair']:
                   event.add_person(name=chair, note="Chair")
            yield event
