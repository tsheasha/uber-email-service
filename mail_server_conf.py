import os

if 'PRODUCTION_CHECK' in os.environ:
    MAILGUN_API_KEY  = os.environ['MAILGUN_API_KEY']
    MAILGUN_API_URL  = os.environ['MAILGUN_API_URL']
    MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
    MANDRILL_API_URL = os.environ['MANDRILL_API_URL']
else:
    MAILGUN_API_KEY  = 'key-dd679a3173037bff93374c2cc1e8004c'
    MAILGUN_API_URL  = 'https://api.mailgun.net/v2/app33464707.mailgun.org/messages'
    MANDRILL_API_KEY = 'YKnv7hRxBGpLfANN5y6jsg'
    MANDRILL_API_URL = 'https://mandrillapp.com/api/1.0/messages/send.json'
