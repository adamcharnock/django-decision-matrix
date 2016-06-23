from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^delete/(?P<uuid>.*)/$', views.DeleteView.as_view(), name='delete'),
    url(r'^(?P<uuid>.*)/update/$', views.UpdateView.as_view(), name='update'),
    url(r'^(?P<uuid>.*)/$', views.DetailView.as_view(), name='detail'),
]
