import unittest
import json

from tests import settings
from email_service.email import EmailMessage
from email_service.factory import create_app


class UberEmailTestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialise App
        """ 
        self.app = create_app(
            priority_settings=settings)
        self.client = self.app.test_client()
        
    def tearDown(self):
        pass

    def test_send(self):
        """
        Test if app send email or fails to send an email
        """

        email_message = EmailMessage()
        url = 'http://localhost:5000/email/'
        ctype = 'application/json'

        ####### 
        ######### Test Failure to send email
        #######

        payload = {
            "from_email"    : email_message.sender,
            "to_email"  : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )
        
        assert json.loads(response.data)["error"] == "Please include the recipient's email"
        
        email_message.recipient = 'tarek.sheasha@gmail.com'
        payload = {
            "from_email"    : email_message.sender,
            "to_email" : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )

        assert json.loads(response.data)["error"] == "Please include the sender's email"


        email_message.sender = 'tarek.sheasha@gmail.com'
        payload = {
            "from_email"    : email_message.sender,
            "to_email" : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )

        assert json.loads(response.data)["error"] == "Please include the subject of the email"

        email_message.subject = 'Test Subject'
        payload = {
            "from_email"    : email_message.sender,
            "to_email" : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )

        assert json.loads(response.data)["error"] == "Please include the email body"

        email_message.body = 'Test Body'
        email_message.sender = 'invalid_email'
        payload = {
            "from_email"    : email_message.sender,
            "to_email" : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )

        assert json.loads(response.data)["error"] == "Please enter valid email formats"

        #######
        ######### Test succesful sending of email
        ######
        email_message.sender = 'tarek.sheasha@gmail.com'
        payload = {
            "from_email"    : email_message.sender,
            "to_email" : email_message.recipient,
            "subject"     : email_message.subject,
            "email_body"  : email_message.body
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type = ctype
        )

        assert json.loads(response.data)["info"] == "EmailMessage has been sent"

        
if __name__ == '__main__':
    unittest.main()
