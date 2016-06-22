from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_smalluuid.models import SmallUUIDField, uuid_default


class Option(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)


class Criterion(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    category = models.ForeignKey('category')
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'criteria'

    def __str__(self):
        return self.name or 'Unnamed Criterion'


class Weight(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    criterion = models.ForeignKey('criterion')
    value = models.SmallIntegerField()


class Score(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    criterion = models.ForeignKey('criterion')
    option = models.ForeignKey('option')
    value = models.SmallIntegerField()


class Category(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name or 'Unnamed Category'
