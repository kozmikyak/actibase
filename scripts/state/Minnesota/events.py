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

print("Xvfb started")
br = wd.Chrome()
#br.get('http://www.leg.state.mn.us/calendarday?jday=week')
br.get('https://www.leg.state.mn.us/cal?type=all')
sleep(5)
base = html.fromstring(br.page_source)
print("\n\n\nBase obtained\n\n\n")
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


class MinnesotaEventScraper(Scraper):

    def scrape(self):
        for c in senate_base:
            m = {}
            m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
            link = c.xpath('.//h3/a/@href')
            if len(link) > 0:
                m['link'] = c.xpath('.//h3/a/@href')[0]
                m['title'] = c.xpath('.//h3/a/text()')[0]                
            else:
                m['link'] = 'none available'
                m['title'] = c.xpath('.//h3/text()')[0]
            info_div = c.xpath('.//div[@class="calendar_p_indent"]')
            if len(info_div) > 0:
                info_div = info_div[0]
                info_list = info_div.xpath('.//text()')
#                ppr(info_list)
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
            date = c.xpath('.//p/b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                ppr(m)
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)
            ppr(m)

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
        
        for c in house_base:
            m = {}
            date = c.xpath('.//p/b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                ppr(m)
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)
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
            info_div = c.xpath('.//div[@class="calendar_p_indent"]')[0]
            print('one info div')
            if len(info_div) > 0:
                info_list = info_div.xpath('.//text()')
                info_links = info_div.xpath('.//*/@href')
                print(info_links)
                info_list = [x.replace('\n', '').strip() for x in info_list]
                info_list = [x for x in info_list if len(x) > 0]
                ppr(info_list)
                if info_list[0].startswith('Room:'):
                    m['room'] = info_list[1]
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
            
            bill_rows = c.xpath(('.//*/table[@class="cal_bills"]/tbody/tr'))
            print(bill_rows)
            print('\n\n')
            bills = []
            for brs in bill_rows:
                cells = brs.xpath('.//td')
                if len(cells) == 3:
                    b = {}
                    b['bill'] = cells[0].xpath('.//text()')[0]
                    b['author'] = cells[1].xpath('./text()')[0]
                    b['summary'] = cells[2].xpath('./text()')[0]
                    bills.append(b)
                print('next')
            if len(m['notice']) > 0:
                m['notice'] = m['notice'][0]
            else:
                m['notice'] = 'N/A'
            ppr(m)
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

            
        for c in comm_base:
            m = {}
            date = c.xpath('.//p/b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                ppr(m)
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)
            m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
            m['title'] = c.xpath('.//h3/a/text()')[0]
            m['link'] = c.xpath('.//h3/a/@href')[0]
            info_div = c.xpath('.//div[@class="calendar_p_indent"]')[0]
            print('one info div')
            if info_div is not None:
                info_list = info_div.xpath('.//text()')
                if info_list[0] == 'Room: ':
                    m['room'] = info_list[1]
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

