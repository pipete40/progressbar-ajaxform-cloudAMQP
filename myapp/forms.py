from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import numpy as np
from django.utils.safestring import mark_safe

class SlotProfileDataForm(forms.Form):
    L = forms.IntegerField(min_value=2, max_value=3, label='Number of slot types', initial=3 )
    nskus = forms.IntegerField(min_value=10, max_value=1000, label='Number of skus', initial=100)
    alpha = forms.DecimalField(min_value=50, max_value=99.99999, label='Desired Storage Service Level', initial=97.5)
    b = forms.DecimalField(min_value=0, label='Vertical clearance within slot', initial=10)
    M = forms.IntegerField(min_value=1, label= 'Pallet positions per slot', initial=2)
    hs = forms.FileField(label = mark_safe("Pallet height of each sku <i class='fa fa-question-circle' aria-hidden='true' title='Upload a csv file with one column and as many rows as skus.'></i>"),
                         help_text = mark_safe("Download an <a href='/static/files/hs.csv'> example </a> with 100 skus"),
                         widget=forms.FileInput(attrs={'accept': ".csv"})) #validators = [validators.validate_hs])


    def clean_L(self):
        return int(self.cleaned_data.get("L"))

    def clean_nskus(self):
        return int(self.cleaned_data.get("nskus"))

    def clean_alpha(self):
        return float(self.cleaned_data.get("alpha")) / 100

    def clean_b(self):
        return float(self.cleaned_data.get("b"))

    def clean_M(self):
        return int(self.cleaned_data.get("M"))

    def clean_hs(self):
        csvfile = self.cleaned_data.get("hs")
        hs = np.genfromtxt(csvfile, delimiter=',')
        return hs


