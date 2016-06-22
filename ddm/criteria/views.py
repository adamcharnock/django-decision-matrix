from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from ddm.core.models import Criterion


class ListView(generic.ListView):
    template_name = 'criteria/list.html'
    model = Criterion
    context_object_name = 'criteria'


class CreateView(generic.CreateView):
    fields = ['category', 'name']
    template_name = 'criteria/create.html'
    model = Criterion

    def get_success_url(self):
        return reverse('criteria:list')


class UpdateView(generic.UpdateView):
    fields = ['category', 'name']
    template_name = 'criteria/update.html'
    model = Criterion
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('criteria:list')


class DeleteView(generic.DeleteView):
    model = Criterion
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'criteria/confirm_delete.html'

    def get_success_url(self):
        return reverse('criteria:list')
