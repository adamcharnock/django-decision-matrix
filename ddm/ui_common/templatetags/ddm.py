from django import template
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Q

from ddm import defaults

Criterion = apps.get_model('ddm_core', 'Criterion')
Score = apps.get_model('ddm_core', 'Score')

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
def get_group_fitness(context, option, group):
    if not group:
        # If no group, just get all users except the current one
        users = get_user_model().objects.filter(~Q(pk=context['request'].user.pk)).all()
    else:
        users = get_user_model().objects.filter(groups=group).all()
    return option.get_fitness(users)


@register.assignment_tag(takes_context=True)
def get_user_fitness(context, option):
    # Get the overall average fitness for the given open for the current user only
    return option.get_fitness_for_user(context['request'].user)


@register.assignment_tag()
def get_criteria_scores(option, criterion):
    return Score.objects.filter(option=option, criterion=criterion)

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


@register.filter()
def weight_in_words(weight):
    for cutoff, word in defaults.DDM_WEIGHT_WORDS:
        if weight >= cutoff:
            return word
    return '-'


@register.assignment_tag()
def get_criteria_score_variance(criterion, **kwargs):
    return criterion.get_score_variance(**kwargs)

@register.assignment_tag()
def percentage(value, total):
    if total:
        pc = value / float(total) * 100
    else:
        pc = 0
    return int(round(pc))


@register.filter()
def weight_as_index(weight):
    for i, (cutoff, word) in enumerate(defaults.DDM_WEIGHT_WORDS):
        if weight >= cutoff:
            return i
    return None


@register.simple_tag()
def score_min(): return defaults.DDM_SCORE_MIN


@register.simple_tag()
def score_max(): return defaults.DDM_SCORE_MAX


@register.simple_tag()
def weight_min():
    return defaults.DDM_WEIGHT_MIN


@register.simple_tag()
def weight_max(): return defaults.DDM_WEIGHT_MAX
