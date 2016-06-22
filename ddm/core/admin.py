from django.contrib import admin
from . import models

@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Criteron)
class CriteronAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Weight)
class WeightAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

