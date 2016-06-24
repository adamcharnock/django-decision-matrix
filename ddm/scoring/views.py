import json

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from ddm.core.models import Criterion, Option, Score, Category


def get_score(criterion, option, user):
        try:
            score = Score.objects.get(
                user=user,
                option=option,
                criterion=criterion,
            )
        except Score.DoesNotExist:
            score = None
        return score


class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'scoring/list.html'
    model = Category
    context_object_name = 'category_scores'

    def get(self, request, *args, **kwargs):
        self.option = get_object_or_404(Option, uuid=self.kwargs['option_uuid'])
        return super(ListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        # Querset will be a list of tuples in the form (Criterion, Score)
        queryset = []
        for category in super(ListView, self).get_queryset():
            subQueryset = []
            for criterion in category.criteria.all():
                subQueryset.append(
                    (criterion, get_score(criterion, self.option, self.request.user))
                )
            queryset.append((category, subQueryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update(
            option=self.option,
        )
        return context


class ScoreForm(forms.ModelForm):
    value = forms.IntegerField(required=False)

    class Meta:
        fields = ['value']
        model = Score

    def save(self, commit=True):
        if self.cleaned_data.get('value'):
            super(ScoreForm, self).save()
        else:
            if self.instance and self.instance.pk:
                self.instance.delete()


class SetView(LoginRequiredMixin, generic.CreateView):
    model = Score
    form_class = ScoreForm

    def get_form_kwargs(self):
        self.option = get_object_or_404(Option, uuid=self.kwargs.get('option_uuid'))
        self.criterion = get_object_or_404(Criterion, uuid=self.kwargs.get('criterion_uuid'))
        score = get_score(self.criterion, self.option, self.request.user)
        # If the score already exists for this user/criterion, then update the
        # instance of it rather than creating a new one
        if score:
            self.object = score
        return super(SetView, self).get_form_kwargs()

    def form_valid(self, form):
        if not form.instance.id:
            form.instance.option = self.option
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
        return reverse('scoring:list', args=(self.option.uuid,))
