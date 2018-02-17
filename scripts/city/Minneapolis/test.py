import requests
from lxml import html



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
    print(m)

"""
school = 'http://board.mpls.k12.mn.us/'
body = requests.get(school)
base = html.fromstring(body.text)
base.make_links_absolute(school)
members = base.xpath('.//*/div/a/@href')
members = list(set(members))
for member in members:
    member_base = requests.get(member)
    member_base = html.fromstring(member_base.text)
    member_base.make_links_absolute(school)
    text = member_base.xpath('.//*/span/p/text()')
    text = [mb.strip() for mb in text]
    text = [t for t in text if len(t)>0]
    print(text, '\n\n+++\n\n')
    role = text[0].split(',')[1]
    email = member_base.xpath('.//*/span/p/a/@href')[0]
    name = member_base.xpath('.//*/div/span/text()')[1]
    try:
        headshot = member_base.xpath('.//*/div/a/@href')[1]
    except:
        pass
    print(name, email, role, '\n\n+++\n\n\n\n')
"""
