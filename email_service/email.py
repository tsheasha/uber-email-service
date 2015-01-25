import re


class EmailMessage(object):
    """
    A class representing an email message with its four
    constituents:
        1) Sender
        2) Recipient
        3) Subject
        4) Body

    The reason an object is created for each email is firstly
    to make the code look more elegant and secondly this opens
    up a whole new spectrum of functionalities we might require
    in the future
    """
    def __init__(self, sender='', recipient='', subject='', body=''):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def validate_emails(self):
        """
        Although email validation is done as well on Email Server level
        it is very useful to do the validaiton in its more naive form before
        performing the API call to the server, hence saving up on email
        quota and replying back quicker to user regarding invalid format
        of the email address they entered
        """
        valid_sender_email = re.search('(\w+[.|\w])*@(\w+[.])*\w+', self.sender) is not None
        valid_recipient_email = re.search('(\w+[.|\w])*@(\w+[.])*\w+', self.recipient) is not None
        
        return valid_sender_email and valid_recipient_email
