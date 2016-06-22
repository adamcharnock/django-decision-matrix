from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from ddm.core.models import Option


class ListView(generic.ListView):
    template_name = 'options/list.html'
    model = Option
    context_object_name = 'options'


class CreateView(generic.CreateView):
    fields = ['name']
    template_name = 'options/create.html'
    model = Option

    def get_success_url(self):
        return reverse('options:list')


class UpdateView(generic.UpdateView):
    fields = ['name']
    template_name = 'options/update.html'
    model = Option
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('options:list')


class DeleteView(generic.DeleteView):
    model = Option
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'options/confirm_delete.html'

    def get_success_url(self):
        return reverse('options:list')
