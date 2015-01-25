web: gunicorn runserver:application
worker: celery worker -A email_service.mail_queue.pipeline
