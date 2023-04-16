import requests  # Importing the requests library for making HTTP requests
import smtplib  # Importing the smtplib library for sending email notifications
import json  # Importing the json library for parsing JSON responses
import os  # Importing the os library for accessing environment variables
from dotenv import load_dotenv # Import the load_dotenv function to read .env
from .models import StockData  # Importing the StockData model for database operations
from celery import shared_task  # Importing the shared_task decorator from Celery for defining asynchronous tasks
from django_celery_beat.models import PeriodicTask, IntervalSchedule  # Importing models for defining periodic tasks

# Loading variables located at .env
load_dotenv()
API_KEY = os.getenv('API_KEY')  # Getting the API key from an environment variable
SENDER_MAIL = os.getenv('SENDER_MAIL')  # Email address for the sender
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')  # Password for the sender's email account
RCPT_MAIL = os.getenv('RCPT_MAIL')


# Shared task that will create a new Celery Beat scheduled task
@shared_task
def new_schedule_task(ticker, sell_value, buy_value, time_period):
    schedule, created = IntervalSchedule.objects.get_or_create(every=time_period, period=IntervalSchedule.MINUTES)
    PeriodicTask.objects.create(
        name=f"{ticker}_task",
        task="monitor.tasks.stock_api_verifications",
        interval=schedule,
        args=json.dumps([ticker, sell_value, buy_value])
    )
    return "Beat Task created"


# Shared task that will be attached to a Celery Beat scheduled task and will run the monitoring functions
@shared_task
def stock_api_verifications(ticker, sell_value, buy_value):
    email_monitor(api_stock_request(ticker, sell_value, buy_value))


# Function for making API request to get stock data and parsing the response
def api_stock_request(ticker, sell_value, buy_value):
    parameters = {
        "access_key": API_KEY,
        "symbol": ticker
    }

    response = requests.get(url="https://fcsapi.com/api-v3/stock/latest", params=parameters)
    json_response = response.json()

    if json_response['code'] == 200:
        # Loop through the response to find the stock with the desired exchange and currency
        for finded_stock in json_response['response']:
            if finded_stock['exch'] == "BM&FBovespa" and finded_stock['ccy'] == "BRL":
                # Return a dictionary with the stock information
                return {"ticker": ticker, "cotacao": float(finded_stock['c']), "sell_value": sell_value, "buy_value": buy_value}
    else:
        # If the response code is not 200, return False to indicate an error
        return False
    

# Function for sending an email if the conditions are met and recording stock data
def email_monitor(api_response):
    if api_response != False:
        if api_response['cotacao'] < api_response['buy_value']:
            message = "Buy"
        elif api_response['cotacao'] > api_response['sell_value']:
            message = "Sell"
        else:
            message = "Keep"

        # Create a new StockData instance and save it to the database
        new_stock_data = StockData(
            ticker=api_response["ticker"], 
            sell_value=api_response["sell_value"], 
            buy_value=api_response["buy_value"], 
            current_price=api_response["cotacao"], 
            action=message
        )
        new_stock_data.save()
        
        if message != "Keep":
            
            # Connect to Gmail's SMTP server, send an email with the stock information
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=SENDER_MAIL,password=SENDER_PASSWORD)
                connection.sendmail(from_addr=SENDER_MAIL, to_addrs=RCPT_MAIL, msg=f"Subject: Stock Market Monitor\n\n{message} {api_response['ticker']} stock")