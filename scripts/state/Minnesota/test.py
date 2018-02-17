import requests
from pprint import pprint as ppr
import pyopenstates

state = 'MN'
apiKey = 'd2c0db7e-6a6e-4606-a9b0-83c18e647ff6'
pyopenstates.set_api_key(apiKey)

print('Starting')

bills_upper = pyopenstates.search_bills(state='MN', chamber="upper", updated_since="2017-01-01")
reps = pyopenstates.search_legislators(state=state)

for r in reps:
    name = r['full_name']
    first_name = r['first_name']
    last_name = r['last_name']
    full_name = r['first_name'] +  ' ' + r['last_name']
    house = r['chamber']
    if house == 'lower':
        position = 'Representative'
        print(full_name)
    elif house == 'upper':
        position = 'Senator'
    





"""

for bill in bills_upper:
#    ppr(bill)
    title = bill['title']
    number = bill['bill_id']
    status = bill['id']
    dbill = pyopenstates.get_bill(status)
    url = dbill['sources'][0]['url']
#    ppr(dbill)
    votes = dbill['votes']
    if len(votes) > 1:
        ppr(votes)
        break
    

    for vote in votes:
        if len(vote['other_votes']) > 0:
            ppr(vote['other_votes'])
            break



    sponsors = dbill['sponsors']
    for sponsor in sponsors:
        l = pyopenstates.get_legislator(sponsor['leg_id'])
        full_name = l['full_name']
        actions = dbill['actions']
        for act in actions:
            action = act['action']
            actor = act['actor']
            date = act['date']
            action_type = act['type']

        action_dates = dbill['action_dates']            
        for ad in action_dates:
            passed_house = ad['passed_house']
            passed_senate = ad['passed_senate']                
            signed = ad['signed']
            first = ad['first']
            last = ad['last']

    """
