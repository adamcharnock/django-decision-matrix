from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Option(TimeStampedModel):
    name = models.CharField(max_length=200)


class Criteron(TimeStampedModel):
    category = models.ForeignKey('category')

    class Meta:
        verbose_name_plural = 'criteria'


class Weight(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    criterion = models.ForeignKey('criteron')
    value = models.SmallIntegerField()


class Score(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    criterion = models.ForeignKey('criteron')
    option = models.ForeignKey('option')
    value = models.SmallIntegerField()


class Category(TimeStampedModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'
