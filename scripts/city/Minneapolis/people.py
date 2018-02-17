from pupa.scrape import Scraper
from pupa.scrape import Person

#from opencivicdata.core.models import Organization


import requests
from lxml import html


class MinneapolisPersonScraper(Scraper):

    def scrape(self):

        # School Board
        school = 'http://board.mpls.k12.mn.us/'
        body = requests.get(school)
        base = html.fromstring(body.text)
        base.make_links_absolute(school)
        members = base.xpath('.//*/div[@class="summary"]')
        members = list(set(members))
        board = []
        for member in members:
            b = {}
            b['term'] = member.xpath('.//span/p/text()')[-1].replace('\r\n\t', '').replace('\xa0', '').replace('|', '').strip()
            b['district']= member.xpath('.//*/a/text()')[-1]
            link = member.xpath('.//*/@href')[0]
            member_base = requests.get(link)
            member_base = html.fromstring(member_base.text)
            member_base.make_links_absolute(school)
            text = member_base.xpath('.//*/span/p/text()')
            text = [mb.strip() for mb in text]
            text = [t for t in text if len(t)>0]
#            print(text, '\n\n+++\n\n')
            b['role'] = text[0].split(',')[1]
            b['email'] = member_base.xpath('.//*/span/p/a/@href')[0]
            b['name'] = member_base.xpath('.//*/div/span/text()')[1]
            try:
                b['headshot'] = member_base.xpath('.//*/div/a/@href')[1]
            except:
                pass
            member = Person(name=b['name'], role=b['role'])
            member.add_source(url=school)
            member.add_term('Director', 'legislature', org_name='Minneapolis School Board', district=b['district'])
            yield member


        # City Council

        council = 'http://www.minneapolismn.gov/council/'
        body = requests.get(council)
        base = html.fromstring(body.text)
        base.make_links_absolute(council)
        wards = base.xpath('.//*/ul[@id="cname"]/li')
        for w in wards:
            i = {}
            link =  w.xpath('.//a/@href')[0]
            text =  w.xpath('.//a/text()')[0]
            i['link'] = link
            i['ward'] = text.split('-')[0].strip()
            i['name'] = text.split('-')[1].strip()
            member = Person(name=i['name'], role='Council Member')
            member.add_source(link)
            member.add_term('Councilmember', 'legislature', org_name='Minneapolis City Council', district=i['ward'])
            yield member
        
        # Park and Rec Board
        parks = 'https://www.minneapolisparks.org/about_us/leadership_and_structure/commissioners/'
        body = requests.get(parks)
        base = html.fromstring(body.text)
        base.make_links_absolute(parks)
        member_base = base.xpath('.//*/div[@class="col-12"]/div/div/a')
        members = []
        for mb in member_base:
            m = {}
            m['name'] = mb.xpath('.//h3/text()')[0]
            m['link'] = mb.xpath('.//@href')[0]
            m['headshot'] = mb.xpath('.//img/@src')[0]
            post_base = mb.xpath('.//p/span/text()')[0]
            m['post'] = post_base.replace('Commissioner', '').strip()
            if ',' in m['post']:
                m['role'] = m['post'].split(',')[1]
                m['post'] = m['post'].split(',')[0]
            else:
                m['role'] = 'Commisioner'
            member = Person(name=m['name'], role=m['role'])
            member.add_source(url=parks)
            member.add_term('Commissioner', 'legislature', org_name='Minneapolis Parks and Recreation', district=m['post'])
            yield member

