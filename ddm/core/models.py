from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count, Sum
from django_extensions.db.models import TimeStampedModel
from django_smalluuid.models import SmallUUIDField, uuid_default


def get_total_weight(*a, **kw):
    # Could be on the Weight manager
    return sum(criterion.get_average_weight() for criterion in Criterion.objects.all())


def get_total_complete_options(user):
    total_criteria = Criterion.objects.count()
    res = Score.objects.filter(user=user).\
        values('option').\
        annotate(total_scores=Count('option')).\
        order_by()

    complete_option_ids = [r['option'] for r in res if r['total_scores'] == total_criteria]
    return len(complete_option_ids)

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
            return sum(fitnesses) / get_total_weight(*a, **kw)
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

    class Meta:
        unique_together = (
            ('user', 'criterion'),
        )


class Score(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scores')
    criterion = models.ForeignKey('criterion', related_name='scores')
    option = models.ForeignKey('option', related_name='scores')
    value = models.IntegerField()

    class Meta:
        unique_together = (
            ('user', 'option', 'criterion'),
        )


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

    def get_total_weight(self, *a, **kw):
        res = Weight.objects.filter(criterion__category=self, **kw).aggregate(Sum('value'))
        return res['value__sum']

    def get_average_score(self, option, *a, **kw):
        res = Score.objects.filter(criterion__category=self, option=option, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_total_fitness(self, option, *a, **kw):
        total = None
        for criterion in self.criteria.all():
            weight = criterion.get_average_weight(*a, **kw)
            score = criterion.get_average_score(option, *a, **kw)

            if weight is not None and score is not None:
                if total is None:
                    total = 0
                total += weight * score
        return total

    def get_normalised_fitness(self, option, *a, **kw):
        total_fitness = self.get_total_fitness(option, *a, **kw)
        total_weight = self.get_total_weight(*a, **kw)
        if total_fitness is None or total_weight is None:
            return None
        else:
            return total_fitness / total_weight
