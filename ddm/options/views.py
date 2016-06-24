from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views import generic

from ddm.core.models import Option, Criterion, Category


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'options/list.html'
    model = Option
    context_object_name = 'options'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['total_criteria'] = Criterion.objects.count()
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    fields = ['name']
    template_name = 'options/create.html'
    model = Option

    def get_success_url(self):
        return reverse('options:list')


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ['name']
    template_name = 'options/update.html'
    model = Option
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_success_url(self):
        return reverse('options:list')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Option
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'options/confirm_delete.html'

    def get_success_url(self):
        return reverse('options:list')


class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), required=False, empty_label='All users')


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'options/detail.html'
    model = Option
    context_object_name = 'option'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # for_user = self.request.user
        user_form = UserForm(data=self.request.GET)

        if user_form.is_valid():
            for_user = user_form.cleaned_data['user']
        else:
            for_user = None

        context.update(
            categories=Category.objects.all(),
            for_user=for_user,
            user_form=user_form,
        )
        return context
