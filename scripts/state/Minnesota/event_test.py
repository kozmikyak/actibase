import os
from pprint import pprint as ppr

from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb
import requests
from lxml import html
from lxml.etree import tostring

import datetime

start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()

print("Xvfb started")
br = wd.Chrome()
br.get('http://www.leg.state.mn.us/calendarday?jday=week')
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
    name = name.split(' ')
    if not any(sw in name for sw in stopwords) and len(name) == 3:
        name.pop(1)
        name = ' '.join(name)
    else:
        name = ' '.join(name)
    return name

for c in comm_base:
    m = {}
    date = c.xpath('.//p/b/text()')
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
#            ppr(m['chair'])
        if info_list[4] == 'Agenda: ':
            m['agenda'] = info_list[5]
    if len(m['notice']) > 0:
        m['notice'] = m['notice'][0]
    else:
        m['notice'] = 'N/A'
    ppr(m)

        
