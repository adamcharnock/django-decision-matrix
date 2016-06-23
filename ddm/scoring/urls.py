from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<option_uuid>.*)/(?P<criterion_uuid>.*)/update$', views.SetView.as_view(), name='update'),
    url(r'^(?P<option_uuid>.*)$', views.ListView.as_view(), name='list'),
]
