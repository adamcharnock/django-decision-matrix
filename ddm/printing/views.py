from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from ddm.core.models import Category


class CriteriaList(LoginRequiredMixin, generic.ListView):
    template_name = 'printing/list.html'
    model = Category
    context_object_name = 'categories'
