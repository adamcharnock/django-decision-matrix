from django.contrib.auth.models import User
from django.test import TestCase as BaseTestCase

from ddm.core.abstract_models import Category, Criterion, Weight, Option, Score


def get_name(klass):
    return '{} {}'.format(klass.__name__, klass.objects.count() + 1)


class TestDataManager(object):

    def user(self, username=None, email='a@a.com', **kwargs):
        username = username or get_name(User).replace(' ', '').lower()
        return User.objects.create(username=username, email=email, **kwargs)

    def option(self, name=None, **kwargs):
        name = name or get_name(Option)
        return Option.objects.create(name=name, **kwargs)

    def category(self, name=None, **kwargs):
        name = name or get_name(Category)
        return Category.objects.create(name=name, **kwargs)

    def any(self, klass):
        try:
            # Get one
            return klass.objects.all()[0]
        except IndexError:
            # None exist, so create one
            return getattr(self, klass.__name__.lower())()

    def criterion(self, name=None, category=None, **kwargs):
        category = category or self.any(Category)
        name = name or get_name(Criterion)
        return Criterion.objects.create(name=name, category=category, **kwargs)

    def weight(self, user=None, criterion=None, value=5):
        user = user or self.any(User)
        criterion = criterion or self.any(Criterion)
        return Weight.objects.create(user=user, criterion=criterion, value=value)

    def score(self, user=None, criterion=None, option=None, value=5):
        user = user or self.any(User)
        criterion = criterion or self.any(Criterion)
        option = option or self.any(Option)
        return Score.objects.create(user=user, criterion=criterion, option=option, value=value)


class TestCase(BaseTestCase):

    def setUp(self):
        self.data = TestDataManager()
