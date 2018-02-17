

# Base Django Settings
secret_key='make a nice key'
allowed_hosts = [
    'mnactivist.org',
    'api.mnactivist.org',
    'localhost',
]

root_urlconf = 'Actibase.urls'
wsgi_application = 'Actibase.wsgi.application'

#Database Info
dbname='opencivicdata'
dbuser=''
dbpasswd=''

# Social Media Keys
tw_ckey = ''
tw_csecret = ''
tw_tkey = ''
tw_tsecret = ''
fb_token = ''
fb_id = ''
