# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization, Person
from .events import StpaulEventScraper
from .people import StpaulPersonScraper
from .bills import StpaulBillScraper
from .vote_events import StpaulVoteEventScraper

import requests
from datetime import datetime
from datetime import date as dtdate

from pprint import pprint as ppr

from lxml import html

current_date = datetime.today()
current_month = current_date.month
current_year = current_date.year
date_range = []

for x in range(0,4):
    if not current_month == 12:
        cm = current_month
        if len(str(cm)) < 2:
            cm = '0{0}'.format(cm)
        timestamp = "{0}-{1}".format(current_year, cm)
        date_range.append(timestamp)
        current_month += 1

    elif current_month == 12:
        cm = '12'
        timestamp = "{0}-{1}".format(current_year, cm)        
        date_range.append(timestamp)
        current_month = 1
        current_year += 1


class Stpaul(Jurisdiction):
    global date_range

    division_id = "ocd-division/country:us/state:mn/place:st_paul"
    classification = "government"
    name = "Saint Paul"
    url = "https://www.stpaul.gov"
    scrapers = {
        "events": StpaulEventScraper,
#        "people": StpaulPersonScraper,
#        "bills": StpaulBillScraper,
#        "vote_events": StpaulVoteEventScraper,
    }

    def get_organizations(self):
        global date_range

        city = Organization('City of Saint Paul', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:st_paul')
        city.add_post('City Clerk', 'City Clerk', division_id='ocd-division/country:us/state:mn/place:st_paul')        
        yield city

        council = Organization(name="Saint Paul City Council", classification="legislature", parent_id=city)
        for x in range(1, 8):
            council.add_post(
                "Ward {}".format(x),
                "Councilmember",
                division_id='ocd-division/country:us/state:mn/place:st_paul/ward:{}'.format(x))

        yield council

        carter = Person(name="Melvin Carter")
        carter.add_term('Mayor',
                        'executive',
                        start_date=dtdate(2018, 1, 19),
                        appointment=True)
        
        carter.add_source('http://www.google.com')
        yield carter

        new_meetings = []
        temp_labels = []        
        for date in date_range:
            print('Checking date:', date)
            root = requests.get("https://www.stpaul.gov/calendar/" + date)
            base = html.fromstring(root.text)
            items = base.xpath('.//*/div[@class="view-content"]/div')
            meetings = []
            for i in items:
                if len(i.xpath('.//*/span[@class="date-display-single"]/text()')) > 0:
                    d = {}
                    d['date'] = i.xpath('.//*/span[@class="date-display-single"]/text()')[0]
                    d['info'] = i.xpath('.//*/span[@class="field-content"]/a/text()')[0]
                    d['link'] = i.xpath('.//*/span[@class="field-content"]/a/@href')[0]
                    meetings.append(d)

            for m in meetings:
                m['link'] = "https://www.stpaul.gov" + m['link']
            for m in meetings:
                r = requests.get(m['link'])
                b = html.fromstring(r.text)
                exists = b.xpath('.//div[@class="node-content clearfix"]')
                if len(exists)>0:
                    if not 'City Council' in m['info'] and not 'Legislative' in m['info'] and not 'Holiday' in m['info']:
                        m['name'] = m['info'].replace('Meeting', '').replace(' - Cancelled', '').replace('Events', '').strip()
                        if not m['name'] in temp_labels:
                            temp_labels.append(m['name'])
                            new_meetings.append(m)

        print('Creating organizations')
        for m in new_meetings:
            print(m)
            cmt = Organization(name=m['name'],
                               classification='committee',
                               parent_id=city
            )
            cmt.add_source(m['link'])
            yield cmt

