from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^delete/(?P<uuid>.*)/$', views.DeleteView.as_view(), name='delete'),
    url(r'^up/(?P<uuid>.*)/$', views.SortView.as_view(adjustment=-1), name='up'),
    url(r'^down/(?P<uuid>.*)/$', views.SortView.as_view(adjustment=+1), name='down'),
    url(r'^(?P<uuid>.*)/$', views.UpdateView.as_view(), name='update'),
]
