import os

SECRET_KEY = 'r\x91C`O\xdd\xc0\xf7\x14\xb4A\x04=Y\x90\x8fhk\xd8\xa5`\xd5m;'

if 'PRODUCTION_CHECK' in os.environ:
    DEBUG = True
else:
    DEBUG = True
