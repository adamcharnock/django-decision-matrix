import statistics
from functools import lru_cache

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count, Sum
from django.utils.module_loading import import_string
from django_extensions.db.models import TimeStampedModel
from django_smalluuid.models import SmallUUIDField, uuid_default

from ddm import defaults


def get_total_complete_options(user):
    Criterion = apps.get_model('ddm_core', 'Criterion')
    Score = apps.get_model('ddm_core', 'Score')

    total_criteria = Criterion.objects.count()
    res = Score.objects.filter(user=user).\
        values('option').\
        annotate(total_scores=Count('option')).\
        order_by()

    complete_option_ids = [r['option'] for r in res if r['total_scores'] == total_criteria]
    return len(complete_option_ids)

class AbstractOption(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True
        ordering = ['name']
        app_label = 'ddm_core'

    def get_fitness_for_user(self, user):
        return self.get_fitness([user])

    def get_fitness(self, users=None):
        Criterion = apps.get_model('ddm_core', 'Criterion')

        if users is None:
            users = get_user_model().objects.all()

        fitnesses = [c.get_fitness(self, users) for c in Criterion.objects.all()]
        # Some criterion may not have been scored, in which case ignore them
        fitnesses = list(filter(lambda f: f is not None, fitnesses))
        if fitnesses:
            return sum(fitnesses)
        else:
            return None

    def get_completed_users(self):
        Criterion = apps.get_model('ddm_core', 'Criterion')
        Score = apps.get_model('ddm_core', 'Score')

        total_criteria = Criterion.objects.count()
        res = Score.objects.filter(option=self).\
            values('user').\
            annotate(total_scores=Count('user')).\
            order_by('total_scores')

        user_ids = [r['user'] for r in res if r['total_scores'] == total_criteria]
        return get_user_model().objects.filter(pk__in=user_ids)


class AbstractCriterion(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    category = models.ForeignKey('category', related_name='criteria')
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()
    weighting_notes = models.TextField(default='', blank=True)
    scoring_notes = models.TextField(default='', blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'criteria'
        ordering = ['category__name', 'order_num']
        app_label = 'ddm_core'
        db_table = 'core_criterion'
        app_label = 'ddm_core'

    def __str__(self):
        return self.name or 'Unnamed Criterion'

    def save(self, **kwargs):
        Criterion = apps.get_model('ddm_core', 'Criterion')

        if self.order_num is None:
            self.order_num = Criterion.objects.count()
        super(AbstractCriterion, self).save(**kwargs)

    @lru_cache()
    def get_average_weight(self, *a, **kw):
        res = self.weights.filter(*a, **kw).aggregate(Avg('value'))
        return res['value__avg']

    @lru_cache()
    def get_average_score(self, option, *a, **kw):
        res = self.scores.filter(option=option, *a, **kw).aggregate(Avg('value'))
        return res['value__avg']

    @lru_cache()
    def get_fitness_for_user(self, option, user):
        weight = self.get_average_weight(user=user)
        score = self.get_average_score(option, user=user)
        if weight is None or score is None:
            return None
        else:
            return weight * score

    def get_fitness(self, option, users=None):
        if users is not None:
            # Must be hashable for benefit of caching
            users = tuple(users)

        return self._get_fitness(option, users)

    @lru_cache()
    def get_score_variance(self, *args, **kwargs):
        Score = apps.get_model('ddm_core', 'Score')

        scores = Score.objects.filter(criterion=self, *args, **kwargs).values_list('value', flat=True)
        try:
            return statistics.variance(scores)
        except statistics.StatisticsError:
            return 0

    def get_weight_variance(self, *args, **kwargs):
        Weight = apps.get_model('ddm_core', 'Weight')

        weights = Weight.objects.filter(criterion=self, *args, **kwargs).values_list('value', flat=True)
        try:
            return statistics.variance(weights)
        except statistics.StatisticsError:
            return 0


    @lru_cache()
    def _get_fitness(self, option, users):
        fitnesses = []
        if users is None:
            users = get_user_model().objects.all()

        for user in users:
            fitnesses.append(self.get_fitness_for_user(option, user))

        fitnesses = [f for f in fitnesses if f is not None]

        if not fitnesses:
            return None
        else:
            return sum(fitnesses) / len(fitnesses)


class AbstractWeight(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='weights')
    criterion = models.ForeignKey('criterion', related_name='weights')
    value = models.IntegerField()

    class Meta:
        abstract = True
        app_label = 'ddm_core'
        unique_together = (
            ('user', 'criterion'),
        )


class AbstractScore(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scores')
    criterion = models.ForeignKey('criterion', related_name='scores')
    option = models.ForeignKey('option', related_name='scores')
    value = models.IntegerField()

    class Meta:
        abstract = True
        app_label = 'ddm_core'
        unique_together = (
            ('user', 'option', 'criterion'),
        )


class AbstractCategory(TimeStampedModel):
    uuid = SmallUUIDField(default=uuid_default())
    name = models.CharField(max_length=200)
    order_num = models.IntegerField()

    class Meta:
        abstract = True
        app_label = 'ddm_core'
        verbose_name_plural = 'categories'
        ordering = ['order_num']

    def __str__(self):
        return self.name or 'Unnamed Category'

    def save(self, **kwargs):
        Category = apps.get_model('ddm_core', 'Category')

        if self.order_num is None:
            self.order_num = Category.objects.count()
        super(AbstractCategory, self).save(**kwargs)

    def get_average_weight(self, *a, **kw):
        Weight = apps.get_model('ddm_core', 'Weight')
        res = Weight.objects.filter(criterion__category=self, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_total_weight(self, *a, **kw):
        Weight = apps.get_model('ddm_core', 'Weight')
        res = Weight.objects.filter(criterion__category=self, **kw).aggregate(Sum('value'))
        return res['value__sum']

    def get_average_score(self, option, *a, **kw):
        Score = apps.get_model('ddm_core', 'Score')
        res = Score.objects.filter(criterion__category=self, option=option, **kw).aggregate(Avg('value'))
        return res['value__avg']

    def get_total_fitness(self, option):
        total = None
        for criterion in self.criteria.all():
            fitness = criterion.get_fitness(option)
            if fitness is not None:
                if total is None:
                    total = 0
                total += fitness
        return total

    def get_total_fitness_for_user(self, option, user):
        total = None
        for criterion in self.criteria.all():
            fitness = criterion.get_fitness_for_user(option, user)
            if fitness is not None:
                if total is None:
                    total = 0
                total += fitness
        return total

    def get_normalised_fitness(self, option, *a, **kw):
        total_fitness = self.get_total_fitness(option, *a, **kw)
        total_weight = self.get_total_weight(*a, **kw)
        if total_fitness is None or total_weight is None:
            return None
        else:
            return total_fitness / total_weight
