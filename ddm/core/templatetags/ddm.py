from django import template
from django.db.models import Q

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
def get_fitness(option):
    # Get the overall average fitness for the given open for all users
    return option.get_fitness()


@register.assignment_tag(takes_context=True)
def get_everyone_else_fitness(context, option):
    # Get the overall average fitness for the given open for all users except the current
    return option.get_fitness(~Q(user=context['request'].user))


@register.assignment_tag(takes_context=True)
def get_user_fitness(context, option):
    # Get the overall average fitness for the given open for the current user only
    return option.get_fitness(user=context['request'].user)


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
    kw = remove_none_values(user=user)
    return {
        c: c.get_fitness(option, **kw)
        for c
        in Criterion.objects.all()
    }

@register.assignment_tag()
def get_category_fitness(category, option, user=None):
    kw = remove_none_values(user=user)
    return category.get_normalised_fitness(option, **kw)
