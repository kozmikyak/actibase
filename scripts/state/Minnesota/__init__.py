# encoding=utf-8
import requests

from pupa.scrape import Jurisdiction, Organization
from .events import MinnesotaEventScraper
#from .people import MinnesotaPersonScraper
from .people_new import MNPersonScraper
from .bills import MinnesotaBillScraper
from .vote_events import MinnesotaVoteEventScraper


class Minnesota(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn"
    classification = "government"
    name = "Minnesota"
    url = "https://mn.gov"
    scrapers = {
#        "people": MinnesotaPersonScraper,
        "people": MNPersonScraper,        
#        "bills": MinnesotaBillScraper,
        "events": MinnesotaEventScraper,
#        "vote_events": MinnesotaVoteEventScraper,
    }

    legislative_sessions = [{"identifier":"2017s1",
                             "name":"2017 Regular Session",
                             "start_date": "2017-01-01",
                             "end_date": "2018-12-31"}]    

    def get_organizations(self):
        
        state = Organization(name="State of Minnesota", classification="executive")
        state.add_post('Governor', 'Governor', division_id='ocd-division/country:us/state:mn')
        state.add_post('Secretary of State', 'Secretary of State', division_id='ocd-division/country:us/state:mn')
        state.add_post('State Auditor', 'State Auditor', division_id='ocd-division/country:us/state:mn')
        state.add_post('Attorney General', 'Attorney General', division_id='ocd-division/country:us/state:mn')
        state.add_post('Lt Governor', 'Lt Governor', division_id='ocd-division/country:us/state:mn')
        state.add_post('Governor', 'Governor', division_id='ocd-division/country:us/state:mn')
        state.add_post('Governor', 'Governor', division_id='ocd-division/country:us/state:mn')        
        yield state

        url = 'http://alpha.openstates.org/graphql'
        
        leg_base_json = { 'query' : '{ jurisdiction(name: "Minnesota") { name url organizations(classification: "legislature", first: 1) { edges { node { id name classification children(first: 2) { edges { node { id name classification children(first: 100) { edges { node { id name classification parent { id }}}}}}}}}}}}'}
        
        legis_data_base = requests.get(url=url, json=leg_base_json)
        base_data = legis_data_base.json()
        base_data = base_data['data']
        legislature = Organization(name=base_data['jurisdiction']['organizations']['edges'][0]['node']['name'],
                                   classification=base_data['jurisdiction']['organizations']['edges'][0]['node']['classification'])
        
        yield legislature
        
        house = Organization(name=base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][1]['node']['name'],
                      classification=base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][1]['node']['classification'],)
        for x in range(1, 68):
            x = str(x)
            z = x + 'A'
            house.add_post(
                "{}".format(z),
                "State Representative",
                division_id='ocd-division/country:us/state:mn/sldl:{}'.format(z.lower()))
            z = x + 'B'
            house.add_post(
                "{}".format(z),
                "State Representative",
                division_id='ocd-division/country:us/state:mn/sldl:{}'.format(z.lower()))
        yield house


        senate = Organization(name=base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][0]['node']['name'], 
                              classification=base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][0]['node']['classification'],)
        print(senate)
        for x in range(1, 68):
            senate.add_post(
                "{}".format(x),
                "State Senator",
                division_id='ocd-division/country:us/state:mn/sldu:{}'.format(x))
        yield senate

        house_cmts = base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][1]['node']['children']['edges']
        senate_cmts = base_data['jurisdiction']['organizations']['edges'][0]['node']['children']['edges'][0]['node']['children']['edges']

        names = []
        for s in senate_cmts:
            print(s['node'])
            s = s['node']
            c = Organization(name=s['name'], classification=s['classification'], parent_id=senate)
            c.add_source(url)
            names.append(s['name'])
            yield c

        for h in house_cmts:
            h = h['node']            
            c = Organization(name=h['name'], classification=h['classification'], parent_id=house)
            c.add_source(url)
            names.append(h['name'])            
            yield c

"""
        print('\n\n\n+++++ \n\n\n\n INFO \n\n\n\n ++++\n\n\n')
        print(len(names))
        print(len(set(names)))
"""
