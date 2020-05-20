Shiva is a platform whose goal is allowing flexible means to help people.
It is based on the concept of Tickets, when one needs help it creates a ticket,
when one wanna help it creates a ticket.

A ticket maps to some available or missing resource, it can be utilities, clothes, food
or even a folks who are offering shelter.

When a ticket mapping to an available resource is created then it performs a search for tickets
from people who are in need of help for that kind of resource then an E-mail is sent
to those people to inform them of new available resources. The ticket matching 
criteria takes also into accout country and city. 

When a ticket is created then an E-mail is sent to the ticket's author to validate the ticket it
comes with a deletion link that is used to remove the ticket later. 

The rationale to not have a login mechanism consists of the fact that people who are in 
need of basic resources to survive are unlikely to have access to a device with internet. 
The current approach allows one to use someone's else device to create a ticket and get 
contacted with no direct need of internet access.

# Debug

First set up a virtualenv.

~~~
cd ~/.virtualenvs/
virtualenv shiva -p python
~~~

Install Shiva requirements.

~~~

pip install -r requirements.txt
~~~

Fill E-mail backend attributes in shiva/settings.py.

~~~python
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
~~~

Get Google Capitcha keys and fill the following attributes
in shiva/settings.py.

https://developers.google.com/recaptcha/intro

~~~
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
~~~

Run the script below to create Django Admin Superusers.

~~~
./create-superusers
~~~

Run it like:

~~~
cd ~/projects/shiva-code
stdbuf -o 0 python manage.py runserver 0.0.0.0:8000
~~~

After that you should be able to access Shiva on.

http://0.0.0.0:8000

# Credits

I came accross the goal of this project when i met Cara Arellano (cara.arellano@berkeley.edu). 
She invited me to participate in a project to help India to recover from COVID-19 issues. 

I was told the project was the creation of a platform to simplify the process of finding 
available resources for donnation. I liked the project goal and i decided to work on Shiva's specification.