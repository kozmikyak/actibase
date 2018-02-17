from pupa.scrape import Scraper
from pupa.scrape import Person

import requests
from lxml import html


class StpaulPersonScraper(Scraper):

    def scrape(self):
        
        council = requests.get('https://www.stpaul.gov/departments/city-council')
        base = html.fromstring(council.text)
        base.make_links_absolute('https://www.stpaul.gov/departments/city-council')
        links = base.xpath('.//*[@class="field-item even"]/p/a/@href')
        links = list(set(links))
        links = [l for l in links if 'ward' in l]
        names = []
        for link in links:
            person = {}
            root = requests.get(link)
            base = html.fromstring(root.text)
            block = base.xpath('.//*[@class="well well--blue well--big-padding block-content"]')[0]
            ps = block.xpath('.//p')
            ps = [p for p in ps if len(p.xpath('.//*')) > 0]
            name = block.xpath('.//p/a/text()')[0].split(' ')
            title = base.xpath('.//*[@id="page-title"]/text()')[0]
            if len(name) == 3:
                name.pop(1)
            name = (' ').join(name)
            if not name in names:
                names.append(name)
                person['name'] = name
                person['ward'] = title.split('-')[0].strip()
                person['role'] = title.split('-')[1].split(' ')[0].strip()
                member = Person(name=person['name'], role=person['role'])
                member.add_source(link)
                member.add_term(person['role'], 'legislature', org_name='Saint Paul City Council', district=person['ward'])
                yield member
            

        
