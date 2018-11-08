# -*- coding: utf-8 -*-

from chise import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from chise.execution.models import *


class ExecutionForm1(forms.ModelForm):
    class Meta:
        model = Execution
        fields = ('site', 'keywords', 'description',)

class ExecutionForm2(forms.ModelForm):
    class Meta:
        model = Execution
        fields = ('modules',)

class ExecutionForm3(forms.ModelForm):
    class Meta:
        model = Execution
        fields = ('variables',)
