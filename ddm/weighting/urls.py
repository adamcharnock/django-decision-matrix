from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='home'),
    url(r'^update/(?P<uuid>.*)$', views.SetView.as_view(), name='update'),
]
