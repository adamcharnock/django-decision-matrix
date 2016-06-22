from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_smalluuid.models import SmallUUIDField, uuid_default


class Option(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)


class Criterion(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    category = models.ForeignKey('category', related_name='criteria')
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'criteria'

    def __str__(self):
        return self.name or 'Unnamed Criterion'


class Weight(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='weights')
    criterion = models.ForeignKey('criterion', related_name='weights')
    value = models.IntegerField()


class Score(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scores')
    criterion = models.ForeignKey('criterion', related_name='scores')
    option = models.ForeignKey('option', related_name='scores')
    value = models.IntegerField()


class Category(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name or 'Unnamed Category'
