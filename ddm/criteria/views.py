from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from ddm.core.models import Criterion, Category
from ddm.core.views import SortView as BaseSortView


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


class ReportView(LoginRequiredMixin, generic.ListView):
    template_name = 'criteria/report.html'
    model = Criterion
    context_object_name = 'criteria'

    def get_queryset(self):
        queryset = super(ReportView, self).get_queryset()
        queryset = list(queryset)
        queryset = sorted(queryset, key=lambda c: c.get_average_weight(), reverse=True)
        return queryset


class SortView(LoginRequiredMixin, BaseSortView):
    model = Criterion

    def get_success_url(self):
        return reverse('criteria:list')

    def get_all_objects(self):
        return self.model.objects.filter(category=self.object.category).order_by('order_num')
