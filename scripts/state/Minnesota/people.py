from pupa.scrape import Scraper
from pupa.scrape import Person

import requests
from pprint import pprint as ppr

import pyopenstates

state = 'MN'
apiKey = 'd2c0db7e-6a6e-4606-a9b0-83c18e647ff6'
pyopenstates.set_api_key(apiKey)

print('Starting')

bills_upper = pyopenstates.search_bills(state='MN', chamber="upper", updated_since="2017-01-01")
reps = pyopenstates.search_legislators(state=state)

rep_names = []

for r in reps:
    name = r['full_name']
    first_name = r['first_name']
    last_name = r['last_name']
    full_name = r['first_name'] +  ' ' + r['last_name']
    house = r['chamber']
    if house == 'lower':
        position = 'Representative'
        rep_names.append(full_name)
    elif house == 'upper':
        position = 'Senator'


class MinnesotaPersonScraper(Scraper):

    def scrape(self):
        url = 'http://alpha.openstates.org/graphql'
        scrapers = [
            { 'query': '{ people(memberOf:"ocd-organization/e91db6f8-2232-49cd-91af-fdb5adb4ac3b", first: 100) { edges { node { name party: currentMemberships(classification:"party") { organization { name }} links { url } sources { url } chamber: currentMemberships(classification:["upper", "lower"]) { post { label } organization { name classification parent { name }}}}}}}'},
#            { 'query': '{ people(memberOf:"ocd-organization/e91db6f8-2232-49cd-91af-fdb5adb4ac3b", last: 100) { edges { node { name party: currentMemberships(classification:"party") { organization { name }} links { url } sources { url } chamber: currentMemberships(classification:["upper", "lower"]) { post { label } organization { name classification parent { name }}}}}}}'},
            { 'query': '{ people(memberOf:"ocd-organization/6a026144-758d-4d57-b856-9c60dce3c4b5", first: 100) { edges { node { name party: currentMemberships(classification:"party") { organization { name }} links { url } sources { url } chamber: currentMemberships(classification:["upper", "lower"]) { post { label } organization { name classification parent { name }}}}}}}'},            
            ]


        base = requests.get(url=url, json=scrapers[0])
        base = base.json()
        ppl = base['data']['people']['edges']
        for p in ppl:
            p = p['node']
            if p['name'] in rep_names:
                rep_names.remove(p['name'])

        # Get names unretrieved from primary House API Query
        print('REP NAMES: ', rep_names)
        rep_names.remove('Gene Pelowski')

        for rep in rep_names:
            query = '{ people(memberOf:"ocd-organization/e91db6f8-2232-49cd-91af-fdb5adb4ac3b", first: 100, name: "' + rep + '") { edges { node { name party: currentMemberships(classification:"party") { organization { name }} links { url } sources { url } chamber: currentMemberships(classification:["upper", "lower"]) { post { label } organization { name classification parent { name }}}}}}}'
            query = { 'query' : query }
            scrapers.append(query)
        for s in scrapers:
            base = requests.get(url=url, json=s)
            base = base.json()
            print(base)
            ppl = base['data']['people']['edges']
            for p in ppl:
                p = p['node']
                orgs = p['chamber']
                rep = Person(name=p['name'], role='State Representative')
                for o in orgs:
                    ppr(o)
                    name = o['organization']['name']
                    classification = o['organization']['classification']
                    if o['organization']['parent']:
                        pname = o['organization']['parent']['name']
                        if pname == 'Minnesota Legislature':
                            label = o['post']['label']
                            if 'House' in name:
                                role = 'State Representative'
                            elif 'Senate' in name:
                                role = 'State Senator'
                            rep.add_term(role, classification, district=label, org_name=name)
                            rep.add_source(p['sources'][0]['url'])

                        else:
                            rep.add_membership(name)
                            rep.add_source(p['sources'][0]['url'])
                yield rep

                                
                        
 

                        
        
