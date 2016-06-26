from django.apps import apps
from django.contrib import admin
from . import abstract_models


Option = apps.get_model('core', 'Option')
Criterion = apps.get_model('core', 'Criterion')
Weight = apps.get_model('core', 'Weight')
Score = apps.get_model('core', 'Score')
Category = apps.get_model('core', 'Category')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    pass


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    pass


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

