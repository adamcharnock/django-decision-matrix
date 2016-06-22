from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from ddm.core.models import Category


class ListView(generic.ListView):
    template_name = 'categories/list.html'
    model = Category
    context_object_name = 'categories'


class CreateView(generic.CreateView):
    fields = ['name']
    template_name = 'categories/create.html'
    model = Category

    def get_success_url(self):
        return reverse('categories:list')


class UpdateView(generic.UpdateView):
    fields = ['name']
    template_name = 'categories/update.html'
    model = Category
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('categories:list')


class DeleteView(generic.DeleteView):
    model = Category
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'categories/confirm_delete.html'

    def get_success_url(self):
        return reverse('categories:list')
