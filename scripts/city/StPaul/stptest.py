import requests
import datetime
from pprint import pprint as ppr

from lxml import html

current_date = datetime.today()
current_month = current_date.month
current_year = current_date.year

def stp_cycle(date):
    root = requests.get("https://www.stpaul.gov/calendar/" + date)
    base = html.fromstring(root.text)
    items = base.xpath('.//*/div[@class="view-content"]/div')
    meetings = build_mtgs(items)
    print('building meetings')
    complete_link_and_update(meetings)

def build_mtgs(items):
    meetings = []
    for i in items:
        if len(i.xpath('.//*/span[@class="date-display-single"]/text()')) > 0:
            d = {}
            d['date'] = i.xpath('.//*/span[@class="date-display-single"]/text()')[0]
            d['info'] = i.xpath('.//*/span[@class="field-content"]/a/text()')[0]
            d['link'] = i.xpath('.//*/span[@class="field-content"]/a/@href')[0]
            meetings.append(d)
    return meetings

def complete_link_and_update(meetings):
    format1 = "%A %B %d, %Y - %I:%M %p"
    format2 = "%A %B %d, %Y - "
    format3 = "%m/%d/%y"

    for m in meetings:
        m['link'] = "https://www.stpaul.gov" + m['link']

    for m in meetings:
        ppr(m['info'])
        r = requests.get(m['link'])
        b = html.fromstring(r.text)
        exists = b.xpath('.//div[@class="node-content clearfix"]')
        if len(exists)>0:
            date = exists[0].xpath('.//*/span[@class="date-display-single"]/text()')
            loc1 = exists[0].xpath('.//*/div[@class="thoroughfare"]/text()')
            loc2 = exists[0].xpath('.//*/div[@class="premise"]/text()')
            if len(loc1) > 0:
                m['location'] = loc1[0] 
            if len(loc2) > 0:
                m['location'] = m['location'] + " " + loc2[0]
            else:
                m['location'] = 'N/A'
            if ":" in date[0]:
                m['date'] = datetime.strptime(date[0], format1)
            elif "/" in date[0]:
                new_date = date[0].split('/')
                for n in new_date:
                    if len(n) == 1:
                        n = '0'+ n
                new_date = '/'.join(new_date)
                m['date'] = datetime.strptime(new_date, format3)
            else:
                date = datetime.strptime(date[0], format2)
                m['date'] = date
            if not 'City Counil' in m['info'] and not 'Legislative Hearings' in m['info']:
                event = Event(name=m['info'],
                              url=m['link'], 
                              start_time=m['date'], 
                              location_name=m['location']
                )
                event.add_committee(m['info'])
            else:
                event = Event(name=m['info'],
                              url=m['link'], 
                              start_time=m['date'], 
                              location_name=m['location']
                )
                event.add_committee('Saint Paul City Council')                
            yield event


date_range = []
print(current_month)
for x in range(0,3):
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

for date in date_range:
    stp_cycle(date)

print('date range', date_range)
print('START NEXT PULL')


'''

r = requests.get("https://stpaul.legistar.com/Calendar.aspx")
b = html.fromstring(r.text)
eas = b.xpath('.//*/table[@class="rgMasterTable"]/*/tr')

for e in eas:
    print('GET EVENTS')
    date_format = '%m/%d/%Y %I:%M %p'
    name = e.xpath('.//td[1]/*/a/*/text()')
    date = e.xpath('.//td[2]/*/text()')
    time = e.xpath('.//td[4]/*/span/*/text()')
    loc = e.xpath('.//td[5]/*/text()')
    details = e.xpath('.//td[6]/*/a/@href')
    agenda = e.xpath('.//td[7]/*/*/a/@href')
    if len(date) > 0:
        print('CHECK DATE')
        name = name[0]
        if len(details) > 0:
            deets_link = 'https://stpaul.legistar.com/' + details[0]
        if len(agenda) > 0:
            agenda_link = 'https://stpaul.legistar.com/' + agenda[0]
        dt = date[0] + ' ' + time[0]
        rdt = datetime.strptime(dt, date_format)
        try:
            ev = Events.objects.get(calendar="St Paul", time=rdt, title__startswith=name)
            if len(details) > 0 and len(agenda) > 0:
                note = '{0}\n <a href="{1}" target="_blank"><h3>Meeting Details</h3></a> <a href="{2}" target="_blank"><h3>PDF Agenda</h3></a>'.format(loc[0], deets_link, agenda_link)
                
                ev.notes = note
                ev.save()
            elif len(details) > 0 and not len(agenda) >0:
                note = '{0}\n<a href="{1}" target="_blank"><h3>Meeting Details</h3></a>'.format(loc[0], deets_link)
                ev.notes = note
                ev.save()
            else:
                note = '{0}'.format(loc[0])
                ev.notes = note
                ev.save()
        except:
            pass
'''
