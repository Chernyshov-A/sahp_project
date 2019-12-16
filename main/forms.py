from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import History


class SaveHistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('user', 'criterian', 'variants', 'selection_result')
