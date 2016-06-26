from ddm.core.base_test import TestCase


class CriteriaModelTestCase(TestCase):

    def test_get_average_weight(self):
        criterion = self.data.criterion()
        self.data.weight(user=self.data.user(), criterion=criterion, value=0)
        self.data.weight(user=self.data.user(), criterion=criterion, value=1)
        self.data.weight(user=self.data.user(), criterion=self.data.criterion(), value=5)  # should be ignored
        self.assertEqual(criterion.get_average_weight(), 0.5)

    def test_get_average_score(self):
        criterion = self.data.criterion()
        option = self.data.option()
        self.data.score(user=self.data.user(), criterion=criterion, option=option, value=0)
        self.data.score(user=self.data.user(), criterion=criterion, option=option, value=1)

        self.assertEqual(criterion.get_average_score(option), 0.5)

    def test_get_fitness(self):
        criterion = self.data.criterion()
        option = self.data.option()

        user1 = self.data.user()
        self.data.weight(user=user1, criterion=criterion, value=5)
        self.data.score(user=user1, criterion=criterion, option=option, value=5)

        user2 = self.data.user()
        self.data.weight(user=user2, criterion=criterion, value=0)
        self.data.score(user=user2, criterion=criterion, option=option, value=0)

        self.assertEqual(criterion.get_fitness(option), 12.5)
        self.assertEqual(criterion.get_fitness_for_user(option, user1), 25)
        self.assertEqual(criterion.get_fitness_for_user(option, user2), 0)

    def test_score_variance(self):
        criterion = self.data.criterion()
        option = self.data.option()
        self.data.score(user=self.data.user(), criterion=criterion, option=option, value=5)
        self.data.score(user=self.data.user(), criterion=criterion, option=option, value=1)

        self.assertEqual(criterion.get_score_variance(), 8.0)

    def test_weight_variance(self):
        criterion = self.data.criterion()
        self.data.weight(user=self.data.user(), criterion=criterion, value=1)
        self.data.weight(user=self.data.user(), criterion=criterion, value=5)

        self.assertEqual(criterion.get_weight_variance(), 8.0)
