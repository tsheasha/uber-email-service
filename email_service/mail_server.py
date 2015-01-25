import os
import json
import random
import requests
import traceback

from mail_server_conf import MAILGUN_API_KEY, MAILGUN_API_URL, MANDRILL_API_KEY, MANDRILL_API_URL

class MailServerException(Exception):
    pass

class BadHTTPRequest(MailServerException):
    pass

class UnauthorisedHTTPRequest(MailServerException):
    pass

class FailedHTTPRequest(MailServerException):
    pass

class InsufficientFundsError(MailServerException):
    pass

class UnidentifiedHTTPError(MailServerException):
    pass

HTTP_RESPONSE = {
        400 : BadHTTPRequest,
        401 : UnauthorisedHTTPRequest,
        402 : FailedHTTPRequest,
        'ValidationError' : BadHTTPRequest,
        'Invalid_Key'     : UnauthorisedHTTPRequest,
        'PaymentRequired' : InsufficientFundsError
}

class MailServer(object):
    def send_mail(self, email):
        """
        Send email after validations have passed in the
        dispatcher phase. This method is invoked for a mail
        server from the mail_queue. This does not guarantee
        that the email will be sent directly though since there
        are other validations to be don eon the mail server logic.
        In case an error appears the respectve error will be raised
        accordingly.
        """
        pass

    def _post_process(self, response):
        """
        Post processing phase after the email has been sent
        out. This phase is responsible for mail server response
        interpretation. Returning success messages and raising
        errors when necessary.
        """


class Mailgun(MailServer):

    def __init__(self):
        self.api_url = MAILGUN_API_URL
        self.api_key = MAILGUN_API_KEY
    
    def send_mail(self, email):
        payload = {
            'from'   : email.sender,
            'to'     : email.recipient,
            'subject': email.subject,
            'text'   : email.body
        }
        
        try:
            mailgun_response = requests.post(
                                  self.api_url,
                                  auth = ('api', self.api_key),
                                  data = payload
            )
        except requests.RequestException:
            traceback.print_exc()
        
        processed_response = self._post_process(mailgun_response)
        return processed_response

    def _post_process(self, response):
        if response.status_code == 200:
            return 'success'
        else:
            if response.status_code in HTTP_RESPONSE:
                raise HTTP_RESPONSE[response.status_code](response.json())
            else:
                raise UnidentifiedHTTPError(response.json())
 

class Mandrill(MailServer):

    def __init__(self):
        self.api_url = MANDRILL_API_URL
        self.api_key = MANDRILL_API_KEY
    
    def send_mail(self, email):
        email_message = {
            'from_email'   : email.sender,
            'to'     : [{'email' : email.recipient}],
            'subject': email.subject,
            'text'   : email.body
        }
        
        payload = {
            'key'     : self.api_key,
            'async'   : True,
            'message' : email_message
        }

        try:
            mandrill_response = requests.post(
                                  self.api_url,
                                  data = json.dumps(payload)
            )
        except requests.RequestException:
            traceback.print_exc()
        
        processed_response = self._post_process(mandrill_response)
        return processed_response

    def _post_process(self, response):
        if response.status_code == 200:
            return 'success'
        else:
            try:
                response_json = response.json()
                if response_json['status'] == 'error':
                    if response_json['name'] in HTTP_RESPONSE:
                        raise HTTP_RESPONSE[response_json['name']](response.json())
                    else:
                        raise UnidentifiedHTTPError(response.json())
                else:
                    raise UnidentifiedHTTPError(response.json())
            except ValueError:
                raise UnidentifiedHTTPError(response.json())
            except KeyError:
                raise UnidentifiedHTTPError(response.json())

_mail_servers = {
    'active': Mailgun(),
    'inactive': Mandrill()
}
def get_mail_server():
    """
    Distribute load between mail servers using a simple
    round robin algorithm.
    """
    active_server = _mail_servers['active']
    _mail_servers['active'], _mail_servers['inactive'] = _mail_servers['inactive'], _mail_servers['active']
    return active_server
