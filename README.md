# Bytesize Django Starter Template

A project starter template for Django 1.10 that is production ready for creating a Facebook Messenger bot deployed to Heroku.

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Base application for developing a Facebook Messenger bot with all the necessary utilities such as message handling, message logging, and chat preparation.
- Comes configured with Celery as the task scheduler.
- Uses Python 2.7.

## High Level Understanding of Workflow
handler breakdown
logging
celery
1. Be sure to read through the code in bot/utils/ to understand how message events are handled and logged.

## How to Use

To use this project, follow these steps:

### Seting up your Environment

Install Django:

    $ pip install django

Install RabbitMQ:
    
    $ brew install rabbitmq

### Creating your Project

Using this template to create a new Django app is easy:

    $ django-admin.py startproject --template=https://github.com/rohitahuja/django-bytesize-template/archive/master.zip --name=Procfile helloworld

You can replace ``helloworld`` with your desired project name.

### Setting up the Project

Create your virtual environment and activate it:

    $ virtualenv venv
    $ source ./venv/bin/activate

Install the necessary dependencies:

    $ pip install -r requirements.txt

Make adjustments if necessary to the models in bot/models.py, and then create the migration files and migrate:

    $ python manage.py makemigrations
    $ python manage.py migrate

### Deployment to Heroku

Initialize version control for the project:

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

Create a Heroku project:

    $ heroku create
    $ git push heroku master

Migrate the models on Heroku:

    $ heroku run python manage.py migrate

Set up a messaging queue (CloudAMQP) for celery:

    $ heroku addons:create cloudamqp

Turn on the worker dyno:

    $ heroku ps:scale worker=1

### Connecting to a Messenger Bot

Follow these steps:
Create your messenger bot on https://developers.facebook.com/ 

Add the App Secret on the Dashboard as an environment variable on Heroku:
    
    $ heroku config:set APP_SECRET=<APP_SECRET>

Add the products Messenger and Webhooks. On the Webhooks tab, create a New Subscription with the Callback URL as `http://<your-heroku-subdomain>.herokuapp.com/webhook/` and the Verify Token as one that you can configure on Heroku as the environment variable "VERIFY_TOKEN" on Heroku, or "yeezyyeezywhatsgood" by default. For Fields, check all the ones that begin with "message".

On the Messenger tab, under "Webhooks", subscribe the webhook we just created to the page you want to connect your bot with. Also, under "Token Generation", generate a token for the page we're connecting the bot to and add it as an environment variable on Heroku:

    $ heroku config:set PAGE_ACCESS_TOKEN=<PAGE_ACCESS_TOKEN>

### Hacking on the Project

Hack away on the project. Follow roughly these steps:
    1. To handle messages:
        - Write message handlers in bot/utils/handle.py
    2. To prepare a chat with entities like a persistent menu, a get started page, etc.
        - Customize the prepare methods in bot/utils/prepare.py
        - Run the following:
            $ heroku run python manage.py shell
            $ >>> from bot.utils.prepare import *
            $ >>> p = BotThreadPreparer()
            $ >>> p.prepare()
    3. Work on the rest of what's necessary for your application.

### Testing the Project

To test the project, you'll need to open two terminal windows.

In the first one, run the server:

    $ python manage.py runserver

In the second one, run the celery worker:

    $ celery -A sample_bot worker -B -l info --without-gossip --without-mingle --without-heartbeat

