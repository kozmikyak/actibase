# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import HennepinEventScraper
from .people import HennepinPersonScraper
from .bills import HennepinBillScraper
from .vote_events import HennepinVoteEventScraper


class Hennepin(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/county:hennepin"
    classification = "government"
    name = "Hennepin County"
    url = "https://www.hennepin.us"
    scrapers = {
        "events": HennepinEventScraper,
        "people": HennepinPersonScraper,
        "bills": HennepinBillScraper,
        "vote_events": HennepinVoteEventScraper,
    }

    def get_organizations(self):

        hnp = Organization(name="Hennepin County", classification="legislature")
        hpn.add_post("County Attorney", "County Attorney")
        hpn.add_post("Sheriff", "Sheriff")

        for x in range(1, 8):
            hnp.add_post(
                "District {}".format(x),
                "Councilmember",
n                division_id='ocd-division/country:us/state:mn/county:hennepin/council_district:{}'.format(x))
        
        org = Organization(name="Housing and Redevelopment Authority", classification="committee")
        org = Organization(name="Regional Railroad Authority", classification="committee")        

        yield hpn

        broot = request.get('https://www.hennepin.us/your-government#leadership')
        base = html.fromstring(broot.text)
        grids = base.xpath('.//*[@class="module-grid"]/article')
        for g in grids:
            c = {}
            c['link'] = g.xpath('.//*/@href')[0]
            name = g.xpath('.//h1/text()')[0]
            cr = requests.get(c['link'])
            cb = html.fromstring(cr.text)
            cbase = cb.xpath('.//*[@class="street-address"]')
            blocks = cbase.xpath('.//*[@class="contactBlock"]')
            for bl in blocks:
                bname = bl.xpath('.//h3/text()')[0]
                email = bl.xpath('.//*/@href')
                text = bl.xpath('.//p/text()')
                if ',' in bname:
                    bname = bname.split(',')
                    aname = bname[0]
                    position = bname[1]
                else:
                    bname = bname.replace('Commissioner' '').strip()
