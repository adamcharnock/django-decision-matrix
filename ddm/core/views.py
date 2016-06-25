from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic


class SortView(generic.DetailView):
    # Base view for sorting things
    model = None
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    adjustment = 1

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    def get_all_objects(self):
        return self.model.objects.all().order_by('order_num')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        all_objects = list(self.get_all_objects())
        current_index = all_objects.index(self.object)
        destination_index = current_index + self.adjustment

        if destination_index < 0:
            destination_index = len(all_objects) - 1
        if destination_index > len(all_objects) - 1:
            destination_index = 0

        all_objects[current_index], all_objects[destination_index] = \
            all_objects[destination_index], all_objects[current_index]

        for i, category in enumerate(all_objects):
            print(category, i)
            category.order_num = i
            category.save()

        return HttpResponseRedirect(self.get_success_url())
