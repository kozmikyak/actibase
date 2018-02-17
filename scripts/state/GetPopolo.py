import sys
import os
import django

<<<<<<< HEAD:scripts/State/GetPopolo.py
sys.path.append('/websrv/actibase/mnactivist/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MnActivist.settings'
django.setup()

=======
>>>>>>> 016422fcf872ee843d9e943d015c57411ff04974:scripts/state/GetPopolo.py

from pprint import pprint as ppr

import requests
from lxml import html
import re, os
import datetime

from dex.models import *

import pyopenstates

from MnHouseMemAdditionalInfo import process_text, parse_info, get_member

apiKey = 'd2c0db7e-6a6e-4606-a9b0-83c18e647ff6'
state = raw_input("Which state? ")
# state = sys.argv[1]
pyopenstates.set_api_key(apiKey)


DIGISTATE = dx_State.objects.get(state_name__code=state)
HOUSE, c1 = Org.objects.get_or_create(name="MN House of Representative",
                                      digistate=DIGISTATE)
SENATE, c2 = Org.objects.get_or_create(name="MN State Senate",
                                       digistate=DIGISTATE)

cmts = pyopenstates.search_committees(state=state)
reps = pyopenstates.search_legislators(state=state)
districts_lower = pyopoenstates.search_districts(state=state, chamber="lower")
#districts_upper = pyopenstates.search_districts(state=state, chamber="upper")
bills_upper = pyopenstates.search_bills(state=state, chamber="upper", updated_since="2017-01-01")
bills_lower = pyopenstates.search_bills(state=state, chamber="lower", updated_since="2017-01-01")



for bill in bills_upper:
    number = bill['bill_id']
    intro = bill['title']
    status = bill['id']
#    try:
    nbill, create = PolicyRecord.objects.get_or_create(number=number,
                                                       intro_text=intro[:512],
                                                       digistate=DIGISTATE,
                                                       primary_org=SENATE,
                                                       status=status)
    dbill = pyopenstates.get_bill(nbill.status)
    url = dbill['sources'][0]['url']
    nbill.link = url
    nbill.save()
    sponsors = dbill['sponsors']
    for sponsor in sponsors:
        try:
            rep = PublicOfficial.objects.get(city_str=sponsor['leg_id'])
            nbill.authors.add(rep.id)
            nbill.save()
        except:
            print("Senate oops sponsor: {0}".format(sponsor))


#    except:
#        ppr(bill)
#        print("Error 1")
#        quit()


for bill in bills_lower:
    number = bill['bill_id']
    intro = bill['title']
    status = bill['id']
    try:
        nbill, create = PolicyRecord.objects.get_or_create(number=number,
                                                           intro_text=intro[:512],
                                                           digistate=DIGISTATE,
                                                           primary_org=HOUSE,
                                                           status=status)
        dbill = pyopenstates.get_bill(nbill.status)
        url = dbill['sources'][0]['url']
        nbill.link = url
        nbill.save()
        sponsors = dbill['sponsors']
        for sponsor in sponsors:
            try:
                rep = PublicOfficial.objects.get(city_str=sponsor['leg_id'])
                nbill.authors.add(rep.id)
                nbill.save()
            except:
                print("House oops sponsor: {0}".format(sponsor))

    except:
        ppr(bill)
        print("Error 2")
        quit()
