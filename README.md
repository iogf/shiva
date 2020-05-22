Shiva is a platform whose goal is allowing flexible means to help people.
It is based on the concept of Tickets, when one needs help it creates a ticket,
when one wanna help it creates a ticket.

A ticket maps to some available or missing resource, it can be utilities, clothes, food
or even folks who are offering shelter.

When a new ticket is created then it performs a matching criteria among existing tickets.
Ticket owners will get notified according to their ticket's attributes like country, state,
city, ticket type, resource type etc.

When a ticket is created then an E-mail is sent to the ticket's author to validate the ticket it
comes with a deletion and avoid expiration link that is used to remove the ticket later. 

The rationale to not demand a login mechanism consists of the fact that people who are in 
need of basic resources to survive are unlikely to have access to a device with internet nor 
an E-mail account. 

The actual approach of having validation/deletion links for tickets it allows third parties 
to ask for help on one behalf with simplicity. 


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
# The site domain.
SITE_ADDRESS = 'http://0.0.0.0:8000'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

EMAIL_FROM = ''
~~~

Get Google Capitcha keys and fill the following attributes
in shiva/settings.py.

https://developers.google.com/recaptcha/intro

**Note:** You should add http://0.0.0.0:8000 in your Google Capitcha
domain to allow it working when in debug mode on port 8000. 

~~~
# For debugging on 0.0.0.0.
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
~~~

Set your site admins with:

~~~
ADMINS = [('Yourname', 'Youremail')]
~~~

That attribute defines who will get notified when tickets are reported.
It works only when DEBUG = False.

Migrate with.

~~~
python manage.py migrate
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

**Note:** You should have the attribute below in your settings.py
in order to run tests. It is to bypass google captcha.

Tickets usually will have an expiration date unless it is meant to be permanent. That feature
will be implemented yet. There is a ticket_app/management/commands/run_expiration 
command to check ticket expiration. You could run it with a cron job.

There is a mechanism of reporting tickets, when a ticket is reported then an E-mail
is sent to all django site admins.

~~~python

NOCAPTCHA = True

~~~

# Next Step

The next steps would be getting people interested to test, contribute with ideas
and mostly translation for other languages.

# Credits

I came accross the goal of this project when i met Cara Arellano (cara.arellano@berkeley.edu). 
She invited me to participate in a project to help India to recover from COVID-19 issues. 

I was told the project was the creation of a platform to simplify the process of finding 
available resources for donnation. I liked the project goal and i decided to work on Shiva's specification.