from django.urls import path

from .views import *

urlpatterns = [
    path('current_weather/', CurrentWeatherListView.as_view(),
         name='weather-list'),
    path('mailing_list/', MailingListView.as_view(),
         name='mailing-list'),
]
