import celery
import json
import mail_queue
import os

from email import EmailMessage
from flask import Blueprint, request
from mail_server import MailServerException, get_mail_server

# Creating a Mail Dispatcher  Blueprint in an effort to make the applicaiton Modular
mail_dispatcher_blueprint = Blueprint('mail_dispatcher', __name__, url_prefix='/email')

# Send an email
@mail_dispatcher_blueprint.route('/', methods=['POST'])
def send():
    """
    Send the email to the recipient via the form. The idea is
    not to send the email direclty by performing an API call,
    the idea is to enqueue each email into a queue in which in
    my case is Celery running on the AMQP broker with a Redis backend

    Creating a quue for this will not only help us keep track if any
    bottlenecks exist, indicated by a long queue, however it will also
    add a factor of guarantee that the message will not be lost if failed
    to send it will keep being dequeued and enqueued until the mail servers
    respone positively
    """
    
    if request.form:
        form_data = request.form
    else:
        form_data = request.get_json()
    email_message = EmailMessage()
    
    if form_data['to_email']:
        email_message.recipient = form_data['to_email']
    else:
        return json.dumps({"error": "Please include the recipient's email"})

    if form_data['from_email']:
        email_message.sender = form_data['from_email']
    else:
        return json.dumps({"error": "Please include the sender's email"})

    if form_data['subject']:
        email_message.subject = form_data['subject']
    else:
        return json.dumps({"error": "Please include the subject of the email"})

    if form_data['email_body']:
        email_message.body = form_data['email_body']
    else:
        return json.dumps({"error": "Please include the email body"})

    if not email_message.validate_emails():
        return json.dumps({"error": "Please enter valid email formats"})
    
    if 'PAYMENT_CHECK' in os.environ:
        # This is how I would do it in reality by using a queue,
        # however this will cost money to run on Heroku, so I
        # sufficed with the more naive approach in the 'else'
        # I tested the queuing system works:
        # celery worker -A email_service.mail_queue.pipeline
        delivery = mail_queue.enqueue.delay(email_message)
        try:
            server = delivery.get(timeout=3)
            return json.dumps({"status": 200,
                               "info": 'EmailMessage has been sent using {}.'.format(server)})
        except celery.exceptions.TimeoutError:
            return json.dumps({"status": 201,
                               "info":'EmailMessage has been queued.'})
    else:
        active_server = get_mail_server() 
        try:
            active_server.send_mail(email_message)
        except MailServerException as mse:
            active_server = get_mail_server() 
            try:
                active_server.send_mail(email_message)
            except MailServerException as mse_1:
                raise mse_1
        return json.dumps({"status": 200,
                           "info": 'EmailMessage has been sent'})
