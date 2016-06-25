from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q

from ddm import defaults
from ddm.core.models import Score, Criterion

register = template.Library()

@register.filter
def or_none(value, none='-'):
    if value is None:
        return none
    else:
        return value


@register.filter
def show_value(value, none='-'):
    if value is None:
        return none
    else:
        try:
            return int(value)
        except (ValueError, TypeError):
            return none


@register.filter
def show_average(value, none='-'):
    # Like show_value, but also shows a decimal point
    if value is None:
        return none
    else:
        try:
            return "{:.1f}".format(value)
        except (ValueError, TypeError):
            return none



def remove_none_values(**kw):
    return {
        k: v
        for k, v
        in kw.items()
        if v is not None
    }


@register.filter
def get(dictionary, key):
    return dictionary.get(key)

@register.assignment_tag(takes_context=True)
def get_user_scores(context, option):
    # Get at the scores the current user has specified for the given option
    return Score.objects.filter(option=option, user=context['request'].user)


@register.assignment_tag()
def get_fitness(option, user=None):
    # Get the overall average fitness for the given open for all users
    return option.get_fitness_for_user(user) if user else option.get_fitness()


@register.assignment_tag(takes_context=True)
def get_everyone_else_fitness(context, option):
    # Get the overall average fitness for the given open for all users except the current
    users = get_user_model().objects.filter(~Q(pk=context['request'].user.pk)).all()
    return option.get_fitness(users)


@register.assignment_tag(takes_context=True)
def get_user_fitness(context, option):
    # Get the overall average fitness for the given open for the current user only
    return option.get_fitness_for_user(context['request'].user)


@register.assignment_tag()
def get_weight_lookup(user=None):
    # Get a dictionary of criterion to weight values
    kw = remove_none_values(user=user)
    return {
        c: c.get_average_weight(**kw)
        for c
        in Criterion.objects.all()
    }


@register.assignment_tag()
def get_score_lookup(option, user=None):
    # Get a dictionary of criterion to score values
    kw = remove_none_values(user=user)
    return {
        c: c.get_average_score(option, **kw)
        for c
        in Criterion.objects.all()
    }

@register.assignment_tag()
def get_fitness_lookup(option, user=None):
    # Get a dictionary of criterion to score values
    return {
        c: c.get_fitness_for_user(option, user) if user else c.get_fitness(option)
        for c
        in Criterion.objects.all()
    }

@register.assignment_tag()
def get_category_fitness(category, option, user=None):
    return category.get_total_fitness_for_user(option, user) if user else category.get_total_fitness(option)


@register.simple_tag()
def score_min(): return defaults.DDM_SCORE_MIN


@register.simple_tag()
def score_max(): return defaults.DDM_SCORE_MAX


@register.simple_tag()
def weight_min(): return defaults.DDM_WEIGHT_MIN


@register.simple_tag()
def weight_max(): return defaults.DDM_WEIGHT_MAX
