from django.contrib.auth.models import Group
from django.forms import forms
from django.forms.models import ModelChoiceField


class GroupForm(forms.Form):
    group = ModelChoiceField(Group.objects.all(), empty_label='Not me', required=False)
