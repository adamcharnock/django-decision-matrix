from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from ddm.core.models import Category


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'categories/list.html'
    model = Category
    context_object_name = 'categories'


class CreateView(LoginRequiredMixin, generic.CreateView):
    fields = ['name']
    template_name = 'categories/create.html'
    model = Category

    def get_success_url(self):
        return reverse('categories:list')


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ['name']
    template_name = 'categories/update.html'
    model = Category
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('categories:list')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'categories/confirm_delete.html'

    def get_success_url(self):
        return reverse('categories:list')


class SortView(LoginRequiredMixin, generic.DetailView):
    model = Category
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_class = Form
    adjustment = 1

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        categories = list(Category.objects.all().order_by('order_num'))
        current_index = categories.index(self.object)
        destination_index = current_index + self.adjustment

        if destination_index < 0:
            destination_index = len(categories) - 1
        if destination_index > len(categories) - 1:
            destination_index = 0

        categories[current_index], categories[destination_index] = \
            categories[destination_index], categories[current_index]

        for i, category in enumerate(categories):
            print(category, i)
            category.order_num = i
            category.save()

        return HttpResponseRedirect(reverse('categories:list'))

