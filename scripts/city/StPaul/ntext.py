import requests
from lxml import html

from pprint import pprint as ppr

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
    if len(name) == 3:
        name.pop(1)
    name = (' ').join(name)
    if not name in names:
        person['name'] = name
        names.append(name)
        print(person)
