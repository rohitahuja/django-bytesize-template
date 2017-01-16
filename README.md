# Bytesize Django Starter Template

A project starter template for Django 1.10 that is production ready for creating a Facebook Messenger bot deployed to Heroku.

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Base application for developing a Facebook Messenger bot with all the necessary utilities such as message handling, message logging, and chat preparation.
- Comes configured with Celery as the task scheduler.
- Uses Python 2.7.

## The High Level

When interactions occur with the connected bot, a set of message events will be sent to this application's web process through the ``/webhook`` route, which is handled in ``bot/views.py``. The function will verify the request, create an asynchronous task to handle the message events (see ``handle_payload`` in ``bot/tasks.py``), and respond to Facebook with a 200 OK response. We create an asynchronous task to respond to Facebook as soon as possible to continue receiving message events. Once the task is created, it will be handled by the celery worker process. Note that the web process is the main process that runs our Django application code and responds to different requests to our routes. The celery worker process runs the tasks that are in queue asynchronously of the web process.

The way message events are handled is contained in ``bot/utils/handle.py`` (see ``MessageHandler``) and ``bot/utils/base/handle.py`` (see ``BaseMessageHandler``). It is extremely important that you understand how these two classes work before writing your own custom handlers (the comments in the classes should walk you through how they work). The idea is that ``MessageHandler`` inherits from ``BaseMessageHandler``. You should not have to change ``BaseMessageHandler``; you should override the handle methods in ``MessageHandler``. Note that the most important method to understand is ``handle`` in ``BaseMessageHandler``.

Once a message is handled and responded to, you have the option to log the message. The logging code is in ``bot/utils/log.py`` (see ``MessageLogger``), but it's more than likely that you won't need to change it. It'd be good to understand how the logging works though.

You can also prepare the chat with entities like a persistent menu, a get started page, etc. To do this, you'll need to customize the prepare methods in ``bot/utils/prepare.py``. See *Hacking on the Project* for more instructions on how to do this.

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

Enter your project folder:

    $ cd helloworld

Create your virtual environment and activate it:

    $ virtualenv venv
    $ source ./venv/bin/activate

Install the necessary dependencies:

    $ pip install -r requirements.txt

Make adjustments if necessary to the models in ``bot/models.py``, and then create the migration files and migrate:

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

Create your messenger bot on https://developers.facebook.com/ 

Add the App Secret on the Dashboard as an environment variable on Heroku:
    
    $ heroku config:set APP_SECRET=<APP_SECRET>

Add the products Messenger and Webhooks. On the Webhooks tab, create a New Subscription with the Callback URL as `http://<your-heroku-subdomain>.herokuapp.com/webhook/` and the Verify Token as one that you can set on Heroku as the environment variable ``VERIFY_TOKEN`` on Heroku, or ``yeezyyeezywhatsgood`` by default. For Fields, check all the ones that begin with ``message``.

On the Messenger tab, under "Webhooks", subscribe the webhook we just created to the page you want to connect your bot with. Also, under "Token Generation", generate a token for the page we're connecting the bot to and add it as an environment variable on Heroku:

    $ heroku config:set PAGE_ACCESS_TOKEN=<PAGE_ACCESS_TOKEN>

### Hacking on the Project

Hack away on the project. To handle messages, write message handlers in ``bot/utils/handle.py``.

To prepare a chat with entities like a persistent menu, a get started page, etc., customize the prepare methods in ``bot/utils/prepare.py``. Then, run the following:
    
    $ heroku run python manage.py shell
    $ >>> from bot.utils.prepare import *
    $ >>> p = BotThreadPreparer()
    $ >>> p.prepare()

Work on the rest of what's necessary for your application. If at any point you want to create an asynchronous task (periodic or not), see ``bot/tasks.py`` for examples. Regular tasks will need to get called in code (see the call for ``handle_payload`` in ``bot/views.py``), and periodic tasks will get picked up by the celery worker to run at their scheduled time. Add your tasks to a ``tasks.py`` file in the relevant app's folder.

### Testing the Project

For now, to test the project, you'll need to do it on production. So make some changes, push to Heroku, and test your messenger bot.

In the future when we get remote servers, to test the project, you'll need to open two terminal windows.

In the first one, run the server:

    $ python manage.py runserver

In the second one, run the celery worker:

    $ celery -A {{ project_name }} worker -B -l info --without-gossip --without-mingle --without-heartbeat

Now, with your messenger bot that is connected to the public URL of your remote server, you'll be able to test your code without having to push to Heroku. Only when you feel confident in your changes should you push to Heroku. 
