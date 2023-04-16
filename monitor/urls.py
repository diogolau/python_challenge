from django.urls import path
from . import views


urlpatterns = [
    path("", views.new_stock),
    path("configurations/", views.configure_stock, name="configure_stock"),
    path("configurations/toggle/", views.disable_enable_tracking, name="disable_enable_tracking"),
    path("configurations/delete/", views.delete_stock, name="delete_stock"),
    path("configurations/changes/", views.change_stock_properties, name="change_stock_properties"),
    path("configurations/records/", views.show_stock_records, name="show_stock_records")
]