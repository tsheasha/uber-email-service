import celery

from mail_server import MailServerException, get_mail_server

pipeline = celery.Celery(__name__, config_source='celeryconfig')

@pipeline.task(bind=True)
def enqueue(self, email):
    raised_exceptions = []
    active_server = get_mail_server() 
    try:
        active_server.send_mail(email)
    except MailServerException as mse:
        raised_exceptions.append(mse)        

    raise self.retry(exc=Exception(*raised_exceptions))
