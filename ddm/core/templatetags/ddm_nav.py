from django import template
from django.apps import apps

from ddm.core.abstract_models import get_total_complete_options

Score = apps.get_model('core', 'Score')
Criterion = apps.get_model('core', 'Criterion')
Option = apps.get_model('core', 'Option')
Weight = apps.get_model('core', 'Weight')

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_total_incomplete_options(context):
    return Option.objects.count() - get_total_complete_options(context['request'].user)


@register.assignment_tag()
def get_total_criteria():
    return Criterion.objects.count()


@register.assignment_tag(takes_context=True)
def get_total_weightings_missing(context):
    return Criterion.objects.count() - Weight.objects.filter(user=context['request'].user).count()
