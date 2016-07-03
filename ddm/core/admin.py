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

