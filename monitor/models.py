from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    sell_value = models.FloatField()
    buy_value = models.FloatField()
    time_period = models.PositiveIntegerField()
    tracked = models.BooleanField(default=True)

    def change_tracked_status(self):
        self.tracked = not self.tracked


    def change_properties(self, new_sell_value, new_buy_value, new_time_period):
        self.sell_value = new_sell_value
        self.buy_value = new_buy_value
        self.time_period = new_time_period


class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    sell_value = models.FloatField()
    buy_value = models.FloatField()
    current_price = models.FloatField()
    action = models.CharField(max_length=5)

