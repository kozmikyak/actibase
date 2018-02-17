# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization, Person
from .events import MinneapolisEventScraper
from .people import MinneapolisPersonScraper
from .bills import MinneapolisBillScraper
from .vote_events import MinneapolisVoteEventScraper

import datetime
import requests
import json


class Minneapolis(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:minneapolis"
    classification = "government"
    name = "Minneapolis"
    url = "http://minneapolismn.gov/"
    scrapers = {
        "events": MinneapolisEventScraper,
        "people": MinneapolisPersonScraper,
        #        "bills": MinneapolisBillScraper,
        #        "vote_events": MinneapolisVoteEventScraper,
    }

    def get_organizations(self):

        city = Organization('City of Minneapolis', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:minneapolis')
        city.add_post('City Clerk', 'City Clerk', division_id='ocd-division/country:us/state:mn/place:minneapolis')        
        yield city

        council = Organization(name="Minneapolis City Council", classification="legislature", parent_id=city)
        for x in range(1, 14):
            council.add_post(
                "Ward {}".format(x),
                "Councilmember",
                division_id='ocd-division/country:us/state:mn/place:minneapolis/ward:{}'.format(x))

        yield council


        frey = Person(name="Frey, Jacob")
        frey.add_term('Mayor',
                      'executive',
                      start_date=datetime.date(2018, 1, 19),
                      appointment=True)
        frey.add_source('http://www.google.com')
        yield frey

        parks = Organization('Minneapolis Parks and Recreation', classification='legislature')
        for x in range(1, 7):
            parks.add_post(
                "District {}".format(x),
                "Commissioner")

        parks.add_post("At Large", "Commissioner")

        yield parks

        school = Organization('Minneapolis School Board', classification='legislature')
        for x in range(1, 7):
            school.add_post(
                "District {}".format(x),
                "Director",)

        school.add_post("At Large", "Director")
        yield school
        


        cmt_link = 'https://lims.minneapolismn.gov/Calendar/GetCommittees'
        cmts_site = requests.get(cmt_link)
        cmts = cmts_site.json()
        for c in cmts:
            name = c['Name']
            abbv = c['Abbreviation']
            org_id = c['Id']
            active = c['Active']
            member_count = c['MembersCount']
            purpose = c['Purpose']
            start_date = c['StartDate']
            chair = c['ChairMan']
            members = c['Members']
            location = c['Location']
            address = c['Address']
            mtg_time = c['MeetingTime']
            quorum = c['QuorumCount']

            if name != 'City Council':
                org = Organization(name, classification='committee', parent_id=council)
                org.add_source(cmt_link)
                if start_date != None:
                    org.founding_date = start_date.split('T')[0]
                yield org
                
