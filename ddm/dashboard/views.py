from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from ddm import defaults

Option = apps.get_model('ddm_core', 'Option')
Criterion = apps.get_model('ddm_core', 'Criterion')


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/home.html'

    def get_best_options(self):
        options = sorted(Option.objects.all(), key=lambda c: c.get_fitness() or 0, reverse=True)
        return options

    def get_up_to_date_users(self):
        users = get_user_model().objects.annotate(num_scores=Count('scores')).order_by('-num_scores')
        return users

    def get_criteria_by_weight_variance(self):
        criteria = sorted(Criterion.objects.all(), key=lambda c: c.get_weight_variance(), reverse=True)

        high_variance = filter(lambda c: c.get_weight_variance() >= defaults.VARIANCE_CUTOFF, criteria)
        high_variance =  list(high_variance)

        criteria.reverse()
        low_variance = filter(lambda c: c.get_weight_variance() >= defaults.VARIANCE_CUTOFF, criteria)
        low_variance =  list(criteria)

        return high_variance, low_variance

    def get_criteria_by_score_variance(self):
        criteria = sorted(Criterion.objects.all(), key=lambda c: c.get_score_variance(), reverse=True)

        high_variance = filter(lambda c: c.get_score_variance() >= defaults.VARIANCE_CUTOFF, criteria)
        high_variance =  list(high_variance)

        criteria.reverse()
        low_variance = filter(lambda c: c.get_score_variance() >= defaults.VARIANCE_CUTOFF, criteria)
        low_variance =  list(criteria)

        return high_variance, low_variance

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['best_options'] = self.get_best_options()
        context['up_to_date_users'] = self.get_up_to_date_users()

        high, low = self.get_criteria_by_weight_variance()
        context['criteria_by_weight_variance_high'] = high
        context['criteria_by_weight_variance_low'] = low

        high, low = self.get_criteria_by_score_variance()
        context['criteria_by_score_variance_high'] = high
        context['criteria_by_score_variance_low'] = low

        return context
