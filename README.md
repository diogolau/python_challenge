![💻Stock_Monitor📈 (1)](https://user-images.githubusercontent.com/80986568/232264382-50ebe616-af1e-44bd-aaaf-6a7714e7d7ca.png)

# Stock Monitor

Stock Monitor is a web application that will help you to track your investments.

## Features
- Track Brazillian stocks continuously.
- Can select what stocks to monitor.
- Can edit each stock variables without needing to delete them.
- Can toggle between track and don't track a stock, without deleting them.
- Can see the records of each stock.
- Can delete a stock, including it's call to the API schedule and it's records at the web interface.
- Easy to use.

## Installation

&nbsp;&nbsp;&nbsp;&nbsp;First of all, you will need 3 things to run this application: Django, Redis and Celery.

&nbsp;&nbsp;&nbsp;&nbsp;For installing Redis on Windows, you should see this: https://github.com/tporadowski/redis/releases

&nbsp;&nbsp;&nbsp;&nbsp;After installing Redis, make sure that the port of Redis is equal to the port at CELERY_BROKER_URL, inside settings.py file.

&nbsp;&nbsp;&nbsp;&nbsp;For using the Django Application, you will have to make sure that API_KEY, SENDER_MAIL, SENDER_PASSWORD and RCPT_MAIL, all variables inside monitor/tasks.py, are configured. For that, create a .env file in the
same directory as your manage.py file. Inside it, write this: 

```.env
API_KEY = #your API key here#
RCPT_MAIL = #the email that will receive the notifications here#
SENDER_MAIL = #the email that will send notifications#
SENDER_PASSWORD = #the password#
```

**_NOTE_**: The API should be [FCSApi](https://fcsapi.com/). To use another API, you will need to adapt the "api_stock_request" function inside tasks.py file, at your monitor directory.

&nbsp;&nbsp;&nbsp;&nbsp;For installing the dependencies that are in the Pipfile file, first install [pipenv](https://pypi.org/project/pipenv/) by running: 

```bash
pip install pipenv
```
&nbsp;&nbsp;&nbsp;&nbsp;Now, install all the dependecies running: 

```bash
pipenv install
```

&nbsp;&nbsp;&nbsp;&nbsp;That should install all of the packages inside Pipfile.

&nbsp;&nbsp;&nbsp;&nbsp;At this point, you should have all of the required packages installed, just needing to start the Django application. But first, we will activate Celery and Celery Beat. To do that, open 3 Git Bashes (I'm running it at Visual Studio Code), I don't recommend using Powershell due to security configurations that Windows may have and can cause some errors. 

&nbsp;&nbsp;&nbsp;&nbsp;Using Git Bash you will execute the necessary commands without needing to change any security configurations on your computer. With all of the Git Bashes opened, you will execute the following commands:

1. First Bash -> Celery:

```bash
celery -A stockmonitor.celery worker --pool=solo -l info
```
&nbsp;&nbsp;&nbsp;&nbsp;For more information, visit the official documentation: https://docs.celeryq.dev/en/stable/

2. Second Bash -> Celery Beat:

```bash
celery -A stockmonitor.celery beat -l info
```

&nbsp;&nbsp;&nbsp;&nbsp;For more information, visit the official documentation: https://django-celery-beat.readthedocs.io/en/latest/.

 **_NOTE:_** As you may notice, Celery Beat documentation is not inside the same website as Celery. That's because we use a package called 'django_celery_beat', but it will be installed automatically when you run 'pipenv install'.

3. Third Bash -> Django:

&nbsp;&nbsp;&nbsp;&nbsp;Here, you may have to execute several commands, depending on your requirements. You can use this command to see what you can do:

```bash
python manage.py
```

&nbsp;&nbsp;&nbsp;&nbsp;However, you may only need to run these three commands, in the respective order:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
&nbsp;&nbsp;&nbsp;&nbsp;That's it, you should have the web application working with all of its features.
