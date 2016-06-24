import json

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from ddm.core.models import Criterion, Weight, Category


def get_weight(criterion, user):
        try:
            weight = Weight.objects.get(
                user=user,
                criterion=criterion,
            )
        except Weight.DoesNotExist:
            weight = None
        return weight


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'weighting/list.html'
    model = Category
    context_object_name = 'category_weights'

    def get_queryset(self):
        queryset = []
        for category in super(ListView, self).get_queryset():
            subQueryset = []
            for criterion in category.criteria.all():
                subQueryset.append(
                    (criterion, get_weight(criterion, self.request.user))
                )
            queryset.append((category, subQueryset))
        return queryset


class WeightForm(forms.ModelForm):
    value = forms.IntegerField(required=False)

    class Meta:
        fields = ['value']
        model = Weight

    def save(self, commit=True):
        if self.cleaned_data.get('value'):
            super(WeightForm, self).save()
        else:
            if self.instance and self.instance.pk:
                self.instance.delete()


class SetView(LoginRequiredMixin, generic.CreateView):
    model = Weight
    form_class = WeightForm

    def get_form_kwargs(self):
        self.criterion = get_object_or_404(Criterion, uuid=self.kwargs.get('uuid'))
        weight = get_weight(self.criterion, self.request.user)
        # If the weight already exists for this user/criterion, then update the
        # instance of it rather than creating a new one
        if weight:
            self.object = weight
        return super(SetView, self).get_form_kwargs()

    def form_valid(self, form):
        if not form.instance.id:
            form.instance.criterion = self.criterion
            form.instance.user = self.request.user

        if self.request.is_ajax():
            form.save()
            return HttpResponse('OK')
        else:
            return super(SetView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors))
        else:
            return super(SetView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('weighting:home')
