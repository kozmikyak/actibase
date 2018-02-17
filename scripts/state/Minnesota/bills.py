from pupa.scrape import Scraper
from pupa.scrape import Bill

from pprint import pprint as ppr
import pyopenstates


import pytz
from datetime import datetime, timedelta

tz = pytz.timezone("US/Central")

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class MinnesotaBillScraper(Scraper):

    def scrape(self):
        state = 'MN'
        session = self.jurisdiction.legislative_sessions[0]
        apiKey = 'd2c0db7e-6a6e-4606-a9b0-83c18e647ff6'
        pyopenstates.set_api_key(apiKey)
        bills_upper = pyopenstates.search_bills(state=state, chamber="upper", updated_since="2017-01-01")
        bills_lower = pyopenstates.search_bills(state=state, chamber="lower", updated_since="2017-01-01")

        for b in bills_lower:
            number = b['bill_id']
            title = b['title']
            bill_id = b['id']
            dbill = pyopenstates.get_bill(bill_id)
            url = dbill['sources'][0]['url']

            bill = Bill(identifier=number,
                        legislative_session=session['identifier'],
                        title=title,
                        classification=b['type'][0],
                        chamber='upper')
            bill.add_source(url)
            bill.add_identifier(bill_id, scheme='openstatesv1')

            subjects = b['subjects']
            for s in subjects:
                bill.add_subject(s)
                
            sponsors = dbill['sponsors']
            for sponsor in sponsors:
                if not sponsor['leg_id'] == None:
                    l = pyopenstates.get_legislator(sponsor['leg_id'])
                    full_name = l['full_name'].split(' ')
                    if len(full_name) == 3:
                        full_name.pop(1)
                    full_name = (' ').join(full_name)
                    primary = False
                    if sponsor['type'] == 'primary':
                        primary = True
                    try:
                        bill.add_sponsorship(name=full_name, classification=sponsor['type'], entity_type='person', primary=primary)
                    except:
                        pass

            actions = dbill['actions']
            for act in actions:
                action = act['action']
                actor = act['actor']
                date = tz.localize(datetime.strptime(act['date'], DATE_FORMAT))
                Action_Type = act['type']
                bill.add_action(action, date, chamber=actor)

            action_dates = dbill['action_dates']
            for act in action_dates.items():
                k,v = act[0], act[1]
                if '_' in k:
                    chamber = k.split('_')[1]
                elif k == 'signed':
                    chamber = 'executive'
                else:
                    chamber = None
                k.replace('_', ' ')
                if not v == None and not k in ['first', 'last']:
                    bill.add_action(k,tz.localize(v), chamber=chamber)
            yield bill



        for b in bills_upper:
            number = b['bill_id']
            title = b['title']
            bill_id = b['id']
            dbill = pyopenstates.get_bill(bill_id)
            url = dbill['sources'][0]['url']

            bill = Bill(identifier=number,
                        legislative_session=session['identifier'],
                        title=title,
                        classification=b['type'][0],
                        chamber='upper')
            bill.add_source(url)
            bill.add_identifier(bill_id, scheme='openstatesv1')

            subjects = b['subjects']
            for s in subjects:
                bill.add_subject(s)
                
            sponsors = dbill['sponsors']
            for sponsor in sponsors:
                if not sponsor['leg_id'] == None:
                    l = pyopenstates.get_legislator(sponsor['leg_id'])
                    full_name = l['full_name'].split(' ')
                    if len(full_name) == 3:
                        full_name.pop(1)
                    full_name = (' ').join(full_name)
                    primary = False
                    if sponsor['type'] == 'primary':
                        primary = True
                    try:
                        bill.add_sponsorship(name=full_name, classification=sponsor['type'], entity_type='person', primary=primary)
                    except:
                        pass

            actions = dbill['actions']
            for act in actions:
                action = act['action']
                actor = act['actor']
                date = tz.localize(datetime.strptime(act['date'], DATE_FORMAT))
                Action_Type = act['type']
                bill.add_action(action, date, chamber=actor)

            action_dates = dbill['action_dates']
            for act in action_dates.items():
                k,v = act[0], act[1]
                if '_' in k:
                    chamber = k.split('_')[1]
                elif k == 'signed':
                    chamber = 'executive'
                else:
                    chamber = None
                k.replace('_', ' ')
                if not v == None and not k in ['first', 'last']:
                    bill.add_action(k,tz.localize(v), chamber=chamber)
            yield bill


            
"""

        for b in bills_lower:
            number = b['bill_id']
            title = b['title']
            bill_id = b['id']
            dbill = pyopenstates.get_bill(bill_id)
            url = dbill['sources'][0]['url']

            bill = Bill(identifier=number,
                        legislative_session=session['identifier'],
                        title=title,
                        classification=b['type'][0],
                        chamber='upper')
            bill.add_source(url)
            bill.add_identifier(bill_id, scheme='openstatesv1')

            subjects = b['subjects']
            for s in subjects:
                bill.add_subject(s)
                
            sponsors = dbill['sponsors']
            for sponsor in sponsors:
                if not sponsor['leg_id'] == None:
                    l = pyopenstates.get_legislator(sponsor['leg_id'])
                    full_name = l['full_name'].split(' ')
                    if len(full_name) == 3:
                        full_name.pop(1)
                    full_name = (' ').join(full_name)
                    primary = False
                    if sponsor['type'] == 'primary':
                        primary = True
                    try:
                        bill.add_sponsorship(name=full_name, classification=sponsor['type'], entity_type='person', primary=primary)
                    except:
                        pass

            actions = dbill['actions']
            for act in actions:
                action = act['action']
                actor = act['actor']
                date = tz.localize(datetime.strptime(act['date'], DATE_FORMAT))
                Action_Type = act['type']
                bill.add_action(action, date, chamber=actor)

            action_dates = dbill['action_dates']
            for act in action_dates.items():
                k,v = act[0], act[1]
                if '_' in k:
                    chamber = k.split('_')[1]
                elif k == 'signed':
                    chamber = 'executive'
                else:
                    chamber = None
                k.replace('_', ' ')
                if not v == None and not k in ['first', 'last']:
                    bill.add_action(k,tz.localize(v), chamber=chamber)
            yield bill
            


            votes = dbill['votes']
            for v in votes:
                chamber = v['chamber']
                vote_date = v['date']
                vote_event_id = v['id']
                motion = v['motion']
                no_count = v['no_count']
                yes_count = v['yes_count']
                url = v['sources'][0]['url']
                passed = 'not passed'
                if v['passed'] == True:
                    passed = 'passed'
                vote_obj = Vote(legislative_session=session['identifier'],
                                motion_text=motion,
                                start_date=vote_date,
                                result=passed )
                vote_obj.add_source(url)
                vote_obj.set_count(option="yes", value=yes_count)
                vote_obj.set_count(option="no", value=no_count)

                vote_results = [{'label': 'yes', 'votes': v['yes_votes']},{ 'label': 'no', 'votes': v['no_votes']}]
                for vr in vote_results:
                    label = vr['label']
                    for vote in vr['votes']:
                        try:
                            l = pyopenstates.get_legislator(vote['leg_id'])
                            full_name = l['full_name']
                            if label == 'yes':
                                vote_obj.yes(full_name)
                            elif label == 'no':
                                vote_obj.no(full_name)
                        except:
                            pass

                yield vote_obj        
            """
