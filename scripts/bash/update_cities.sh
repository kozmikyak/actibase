#!/bin/bash

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actibase/scripts/city/
pupa Minneapolis events
pupa StPaul events

deactivate