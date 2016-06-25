from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^score-sheet/$', views.CriteriaList.as_view(), name='score_sheet'),
]
