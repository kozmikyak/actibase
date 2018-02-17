from pupa.scrape import Scraper
from pupa.scrape import Event

import json
from datetime import datetime, timedelta
import requests

import pytz

def convert_date(date):
    new_date = datetime.strftime(date, DATE_FORMAT)
    return new_date.replace(' ', '%20')


def build_params(f,t,m,c,p):
    list_of_params = []
    params = {
        'fromDate': f,
        'toDate': t,
        'meetingType': m,
        'committeeID': c,
        'pageCount': p
    }
    
    for k,v in params.items():
        list_of_params.append('{0}={1}'.format(k,v))
    return list_of_params

CAL_URL = 'https://lims.minneapolismn.gov/Calendar/GetCalenderList?'

AGENDA_BASE_URL = 'https://lims.mineapolismn.gov/MarkedAgenda/'
CAL_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

DATE_FORMAT = '%b %m, %Y'
TODAY = datetime.now()
THE_FUTURE = TODAY + timedelta(days=60)


#from html2text import html2text

f,t,m,c,p = convert_date(TODAY), convert_date(THE_FUTURE), 0,'null', 1000
lp = '&'.join(build_params(f,t,m,c,p))
site = CAL_URL + lp
new_data = requests.get(site)
cal_list = new_data.json()


tz = pytz.timezone("US/Central")

class MinneapolisEventScraper(Scraper):

    def scrape(self):
        url = 'https://lims.minneapolismn.gov/Calendar/GetCalenderList?'
        council_events = cal_list
        for c in council_events:
            mtg_time = datetime.strptime(c['MeetingTime'], CAL_DATE_FORMAT)
            dt = tz.localize(mtg_time)
            e = Event(name=c['CommitteeName'],
                      start_date=dt,
                      location_name=c['Location'])
            e.add_committee(c['CommitteeName'])
            e.add_source(url)
            if c['MarkedAgendaPublished'] == True:
                event_url = "{0}{1}/{2}".format(AGENDA_BASE_URL, c['Abbreviation'], c['AgendaId'])
                e.add_media_link(note="Agenda",
                                 url=event_url,
                                 media_type="link")
            yield e
                      



    
