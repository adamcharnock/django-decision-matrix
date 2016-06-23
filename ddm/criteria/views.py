from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from ddm.core.models import Criterion, Category


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'criteria/list.html'
    model = Category
    context_object_name = 'categories'


class CreateView(LoginRequiredMixin, generic.CreateView):
    fields = ['category', 'name']
    template_name = 'criteria/create.html'
    model = Criterion

    def get_success_url(self):
        return reverse('criteria:list')


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ['category', 'name']
    template_name = 'criteria/update.html'
    model = Criterion
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('criteria:list')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Criterion
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'criteria/confirm_delete.html'

    def get_success_url(self):
        return reverse('criteria:list')
