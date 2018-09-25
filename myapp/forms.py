from django import forms
from django.core.validators import MinValueValidator
from django.utils.safestring import mark_safe


class GenerateRandomUserForm(forms.Form):
    total_user = forms.IntegerField(
        label='Number of users',
        required=True,
        validators=[
            MinValueValidator(10)
        ]
    )


class SlotProfileDataForm(forms.Form):
    L = forms.IntegerField(min_value=2, max_value=3, label='Number of slot types', initial=3 )
    nskus = forms.IntegerField(min_value=10, max_value=1000, label='Number of skus', initial=100)
    alpha = forms.DecimalField(min_value=50, max_value=99.99999, label='Desired Storage Service Level', initial=97.5)
    b = forms.DecimalField(min_value=0, label='Vertical clearance within slot', initial=10)
    M = forms.IntegerField(min_value=1, label= 'Pallet positions per slot', initial=2)
    """hs = forms.FileField(label = mark_safe("Pallet height of each sku <i class='fa fa-question-circle' aria-hidden='true' title='Upload a csv file with one column and as many rows as skus.'></i>"),
                         help_text = mark_safe("Download an <a href='/static/files/hs.csv'> example </a> with 100 skus"),
                         widget=forms.FileInput(attrs={'accept': ".csv"})) #validators = [validators.validate_hs])
    invs = forms.FileField(label= mark_safe("Inventory level of each sku <i class='fa fa-question-circle' aria-hidden='true' title='Upload a csv file with as many rows as skus and as many columns as time-periods. Include at least 100 time-periods for a good analysis.'></i>"),
                           help_text= mark_safe("Download an <a href='/static/files/invs.csv'> example </a> with 100 skus"),
                           widget=forms.FileInput(attrs={'accept': ".csv"}))
    """
