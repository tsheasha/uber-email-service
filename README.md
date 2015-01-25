Uber E-mail Service
==============

## Uber E-mail Service [Deployed Version](https://uber-email-service.herokuapp.com/)

I have chosen to proceed with the challenge regarding the email service, in the back-end track.

## Running locally?

To run this locally:-

    1) ~$ pip install -r requirements.txt
    2) ~$ python runserver.py

To run the tests:-

    1) ~$ pip install nose
    2) ~$ nosetests

## About me

I have previously worked a lot with Python, on several projects.
Some of which were coding challenges and others out of my passion
for the language. These include:-

* [PyDroid](https://github.com/tsheasha/pydroid):- I created a PyQT port for Python on Android in an effort to createa complete Python GUI Framework for Android also ported to [android-python27](https://code.google.com/p/android-python27/).
* [Todo List](https://github.com/tsheasha/tictail):- A flask and Backbone.js Todo List
* [BlackJack](https://github.com/tsheasha/BlackJack):- An implementation of the BlackJack card game in Java

[Tarek Sheasha on LinkedIn](https://www.linkedin.com/pub/tarek-sheasha/38/646/297)

## Solution

In order to tackle the issue where a mail server might fail, I am balancing the load between two Mail Servers:

    1) Mailgun
    2) Mandrill

The choice of which of them to use is determined by a round-robin algorithm which can accomodate easily more mail servers.

#### Queuing?
A more elegant solution exists as well within the code which is my prefrred solution.
A queue that holds the emails and dispatches them regularly retrying if a certain sending fails by re-enqueueing the emails. The files containing this queuing system can be viewed at [mail_queue](https://github.com/tsheasha/uber-email-service/blob/master/email_service/mail_queue.py), [mail_dispatcher](https://github.com/tsheasha/uber-email-service/blob/master/email_service/mail_dispatcher.py#L58)

This solution however was not fasible since it will cost money to run on Heroku, so I
sufficed with the more naive approach mentioned above. However is running locally
it can be tested to see the queuing system work:

      ~$ celery worker -A email_service.mail_queue.pipeline


## Architecture:

I have a personal passion for modular software and hence I tried my best
to make this applicaiton as modular as possible.

To do so I utilised tools in Flask such as Blueprints and an application factory.
Each python module is responsible for very granular tasks making the functionalities
more generic and eventually scalable.

URLs were maintained as RESTful as possible as can be seen in the API documentation below.
Responses are gzipped and the HTTP response Content-Encoding Header specifies this, increasing page load speed.
The code is also documented so that the person who reads it does not suffer

I have created tests and automation tests for this application using unittests and selenium. These can be run as specified in the Running Locally? section of this README.

Points on improvement given more time:

* I would have used a subdomain for an api “api.uber-email-service.herokuapp.com”, to maintain a scalable system that can accommodate several versions. This api would server mobile clients using native apps (being hypothetical here). The reason why I would prefer this over being in the same url with a trailing "api" at the end is to balance the loads on the servers and dedicate server(s) for the web service and server(s) for the api service.

* Specifying the response type and API version to be part of the HTTP Header instead of
being part of the url, I found the HTTP header option to be more elegant and RESTful.

     I have worked my hardest into making the API as RESTful as possible, maintaining RESTful URLs along the way.

### API Documentation
Send an email
     
     POST /email/
     
Parameters
     
| Name        | Type           | Description  |
| ------------- |:-------------:|:-----|
| from_email | string      |  The sender of the email. |
| to_email | string      |  The recipient of the email. |
| subject | string      |  The subject of the email. |
| email_body | string      |  The body of the email. |
          
Response

          HTTP/1.1 200
          

#### To be implemented

List all emails
     
     GET /email/
     

Get a single email
     
     GET /email/<id>
     
Delete an email
      
      DELETE /email/<id>
      
Update an email
      
      PUT /email/<id>
      
Looking forward to your feedback!
