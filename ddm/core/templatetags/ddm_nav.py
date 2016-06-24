from django import template

from ddm.core.models import Score, Criterion, Option, Weight, get_total_complete_options

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
