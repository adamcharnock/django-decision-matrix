from django.shortcuts import render
from django.views import generic

from ddm.core.models import Criterion, Weight


class ListView(generic.ListView):
    template_name = 'weighting/list.html'
    model = Criterion
    context_object_name = 'criterion_weights'

    def get_queryset(self):
        queryset = []
        criteria = super(ListView, self).get_queryset()
        for criterion in criteria:
            queryset.append(
                (criterion, self.get_weight(criterion))
            )
        return queryset

    def get_weight(self, criterion):
        try:
            weight = Weight.objects.get(
                user=self.request.user,
                criterion=criterion,
            )
        except Weight.DoesNotExist:
            weight = None
        return weight
