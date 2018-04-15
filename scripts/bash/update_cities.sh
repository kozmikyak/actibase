#!/bin/bash

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actibase/scripts/city/
pupa update Minneapolis events
pupa update StPaul events

deactivate
