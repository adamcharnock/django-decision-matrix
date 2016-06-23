from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count
from django_extensions.db.models import TimeStampedModel
from django_smalluuid.models import SmallUUIDField, uuid_default


class Option(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def get_fitness(self, *a, **kw):
        """ Get the fitness (weight * score) for this option

        Filtering arguments can be passed in as *a and **kw to narrow down the
        wieghts and scores selected (i.e. by user)
        """
        fitnesses = [c.get_fitness(self, *a, **kw) for c in Criterion.objects.all()]
        # Some criterion may not have been scored, in which case ignore them
        fitnesses = list(filter(lambda f: f is not None, fitnesses))

        if fitnesses:
            return sum(fitnesses) / len(fitnesses)
        else:
            return None

    def get_completed_users(self):
        total_criteria = Criterion.objects.count()
        res = Score.objects.filter(option=self).\
            values('user').\
            annotate(total_scores=Count('user')).\
            order_by('total_scores')

        user_ids = [r['user'] for r in res if r['total_scores'] == total_criteria]
        return get_user_model().objects.filter(pk__in=user_ids)


class Criterion(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    category = models.ForeignKey('category', related_name='criteria')
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'criteria'
        ordering = ['category__name', 'name']

    def __str__(self):
        return self.name or 'Unnamed Criterion'

    def get_average_weight(self, *a, **kw):
        res = self.weights.filter(*a, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_average_score(self, option, *a, **kw):
        res = self.scores.filter(option=option, *a, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_fitness(self, option, *a, **kw):
        weight = self.get_average_weight(*a, **kw)
        score = self.get_average_score(option, *a, **kw)
        if weight is None or score is None:
            return None
        else:
            return weight * score


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
        ordering = ['name']

    def __str__(self):
        return self.name or 'Unnamed Category'

    def get_average_weight(self, *a, **kw):
        res = Weight.objects.filter(criterion__category=self, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_average_score(self, option, *a, **kw):
        res = Score.objects.filter(criterion__category=self, option=option, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_average_fitness(self, option, *a, **kw):
        weight = self.get_average_weight(*a, **kw)
        score = self.get_average_score(option, *a, **kw)
        if weight is None or score is None:
            return None
        else:
            return weight * score
