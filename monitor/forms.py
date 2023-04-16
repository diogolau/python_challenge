from django import forms
from .models import Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'sell_value', 'buy_value', 'time_period',]
        labels = {'ticker': 'Ticker', 'sell_value': 'Sell Value', 'buy_value': 'Buy Value', 'time_period': 'Time Period (in minutes)',}


class ChangeForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['sell_value', 'buy_value', 'time_period']
        labels = {'sell_value': 'New Sell Value', 'buy_value': 'New Buy Value', 'time_period': 'New Time Period'}