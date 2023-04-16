import json
from .tasks import new_schedule_task  # Importing a task from a module
from .models import Stock, StockData  # Importing models from a module
from .forms import StockForm, ChangeForm  # Importing forms from a module
from django.shortcuts import render, redirect  # Importing shortcuts from Django
from django_celery_beat.models import PeriodicTask, IntervalSchedule  # Importing a model from a module
from django.db import IntegrityError


# View function for creating a new stock
def new_stock(request):
    if request.method == "POST" and "start_monitoring" in request.POST:
        form = StockForm(request.POST)  # Creating a form instance with POST data
        if form.is_valid() and form.save(commit=False).sell_value > form.save(commit=False).buy_value > 0:  # Checking if form data is valid
            try:
                stock = form.save(commit=False)  # Saving form data to a model instance
                stock.ticker = stock.ticker.upper()  # Setting ticker to uppercase
                stock.save()  # Saving the stock instance to the database
                # Scheduling a new task with Celery to monitor the stock
                new_schedule_task.delay(stock.ticker, stock.sell_value, stock.buy_value, stock.time_period)
            except IntegrityError:
                pass
    form = StockForm()  # Creating a new form instance
    return render(request, "home_page.html", {'form': form})  # Rendering the form in a template


# View function for configuring stocks
def configure_stock(request):
    stocks = Stock.objects.all()  # Retrieving all stock instances from the database
    context = {
        'stocks': stocks  # Passing the stocks to the template context
    }
    return render(request, 'configure_stocks.html', context)  # Rendering the stocks in a template


# View function for changing stock properties
def change_stock_properties(request):
    if request.method == "POST" and "change_button" in request.POST:
        stock_ticker = request.POST["change_button"]  # Getting the stock ticker from POST data
    if request.method == "POST" and "change_stock_properties" in request.POST:
        form = ChangeForm(request.POST)  # Creating a form instance with POST data
        stock_ticker = request.POST["change_stock_properties"] # Getting the stock ticker from POST data
        # Checking if form data is valid
        if form.is_valid() and form.save(commit=False).sell_value > form.save(commit=False).buy_value > 0:  
            new_properties = form.save(commit=False)  # Saving form data to a model instance
            stock = Stock.objects.get(ticker=stock_ticker)  # Retrieving the stock instance from the database
            # Changing the properties of the stock instance
            stock.change_properties(new_properties.sell_value, new_properties.buy_value, new_properties.time_period)
            stock.save()  # Saving the updated stock instance to the database
            task = PeriodicTask.objects.get(name=f"{stock_ticker}_task")  # Retrieving the corresponding Celery task
            # Updating the task arguments and interval
            task.args = json.dumps([stock_ticker, new_properties.sell_value, new_properties.buy_value])
            new_schedule, created = IntervalSchedule.objects.get_or_create(every=new_properties.time_period, period=IntervalSchedule.MINUTES)
            task.interval = new_schedule
            task.save()
    form = ChangeForm()  # Creating a new form instance
    return render(request, "change_properties.html", {'form': form, 'stock_ticker': stock_ticker})  # Rendering the form and stock ticker in a template


# View function for enabling/disabling tracking of a stock
def disable_enable_tracking(request):
    if request.method == "POST":
        stock_ticker = request.POST["track_button"]  # Getting the stock ticker from POST data
        stock = Stock.objects.get(ticker=stock_ticker)  # Retrieving the stock instance from the database
        stock.tracked = not stock.tracked  # Toggling the tracking_enabled field
        stock.save()  # Saving the updated stock instance to the database
        task = PeriodicTask.objects.get(name=f"{stock_ticker}_task")  # Retrieving the corresponding Celery task
        task.enabled = not task.enabled  # Setting the enabled field of the task
        task.save()  # Saving the updated task instance to the database
    return redirect(to=configure_stock)  # Redirecting to the configure_stocks view


# View function for deleting a stock, along with its tasks and records data
def delete_stock(request):
    if request.method == "POST":
        stock_ticker = request.POST["delete_button"]  # Getting the stock ticker from the delete button in the form
        Stock.objects.get(ticker=stock_ticker).delete()  # Deleting the stock instance from the database
        PeriodicTask.objects.get(name=f"{stock_ticker}_task").delete()  # Deleting the corresponding Celery task
        StockData.objects.filter(ticker=stock_ticker).delete()  # Deleting related stock data records from the database
    return redirect(to=configure_stock)  # Redirecting to the configure_stocks view


# View function for showing the records data of a stock
def show_stock_records(request):
    if request.method == "POST" and "records_button" in request.POST:
        stock_ticker = request.POST["records_button"]  # Getting the stock ticker from the records button in the form
        records = StockData.objects.filter(ticker=stock_ticker).values()  # Querying stock data records from the database
        context = {
            'records': records
        }
    return render(request, "stock_records.html", context=context)  # Rendering the stock_records.html template with the retrieved stock data records
