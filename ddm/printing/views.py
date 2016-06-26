from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

Category = apps.get_model('core', 'Category')


class CriteriaList(LoginRequiredMixin, generic.ListView):
    template_name = 'printing/list.html'
    model = Category
    context_object_name = 'categories'
