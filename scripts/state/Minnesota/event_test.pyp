
import os

from pprint import pprint as ppr

from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb
import requests
from lxml import html
from lxml.etree import tostring


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

MNSL, c = Organization.objects.get_or_create(name='MN State Legislature')
STP = dx_City.objects.get(city_name__name='Saint Paul')

format1 = "%A, %B %d, %Y %I:%M %p"
format2 = "%A %B %d, %Y - "
format3 = "%m/%d/%y"

for c in comm_base:
    m = {}
    date = c.xpath('.//p/b/text()')
    m['date'] = datetime.strptime(date[0], format1)
    m['notice'] = c.xpath('.//p/span[@class="cal_special"]/text()')
    m['title'] = c.xpath('.//h3/a/text()')[0]
    m['link'] = c.xpath('.//h3/a/@href')[0]
    info_div = c.xpath('.//div[@class="calendar_p_indent"]')    
    ppr(info_div)
    if info_div:
        m['info_text'] = tostring(info_div)[31:-6]
    if len(m['notice']) > 0:
        m['notice'] = m['notice'][0]
    else:
        m['notice'] = 'N/A'
    ppr(m)

        
