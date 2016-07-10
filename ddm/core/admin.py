from django.apps import apps
from django.contrib import admin
from . import abstract_models


Option = apps.get_model('ddm_core', 'Option')
Criterion = apps.get_model('ddm_core', 'Criterion')
Weight = apps.get_model('ddm_core', 'Weight')
Score = apps.get_model('ddm_core', 'Score')
Category = apps.get_model('ddm_core', 'Category')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid', 'name']


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid', 'category', 'name', 'order_num']


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid', 'user', 'criterion', 'value']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid', 'user', 'criterion', 'option', 'value']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid', 'name', 'order_num']

