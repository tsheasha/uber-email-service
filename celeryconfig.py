import os

####### This file needs to be cretaed as per Celery docs to read configuration
if 'PRODUCTION_CHECK' in os.environ:
    ######## Celery Configuration as per Heroku 
    BROKER_URL = os.environ['CLOUDAMQP_URL']
    CELERY_RESULT_BACKEND = os.environ['REDISCLOUD_URL']
else:
    BROKER_URL = 'amqp://kisekwvy:k3CL1gRJzZcRYqi-InPbbt4TI_ssxIw5@bunny.cloudamqp.com/kisekwvy'
    CELERY_RESULT_BACKEND = 'redis://rediscloud:oMtOtyqkTIk5Pzmp@pub-redis-15065.eu-west-1-2.1.ec2.garantiadata.com:15065'

BROKER_POOL_LIMIT = 3
CELERY_REDIS_MAX_CONNECTIONS = 10

######## Default Celery serializer is pickle need to use my serialiser
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_EVENT_SERIALIZER = 'json'
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'

######## Default time for this is 1 day which is too long
######## for our use case
CELERY_TASK_RESULT_EXPIRES = 90
CELERY_MAX_CACHED_RESULTS = 5
