from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import numpy as np
from django.utils.safestring import mark_safe
import certifi
import urllib3
from botocore.client import Config
import boto3
from django.conf import settings



def read_array(urlname, dim):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    r = http.request('GET', urlname)
    csvfile = r.data.decode('utf-8')

    if dim == 1:
        rel = csvfile.splitlines()
        if len(rel) == 1:
            rel = csvfile.split(',')
    elif dim == 2:
        lines = csvfile.splitlines()
        rel = []
        for line in lines:
            rel.append(line.split(','))

    rel = np.array(rel, dtype=np.float)

    #delete file
    try:
        s3 = boto3.client('s3', 'us-east-2',
                          config=Config(signature_version='s3v4'),
                          )
        S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME
        s3.delete_object(Bucket=S3_BUCKET, Key=urlname.split('/')[-1])
    except:
        print("Boto3 connection failing")

    return rel

class SlotProfileDataForm(forms.Form):
    L = forms.IntegerField(min_value=2, max_value=3, label='Number of slot types', initial=3 )
    nskus = forms.IntegerField(min_value=10, max_value=1000, label='Number of skus', initial=100)
    alpha = forms.DecimalField(min_value=50, max_value=99.99999, label='Desired Storage Service Level', initial=97.5)
    b = forms.DecimalField(min_value=0, label='Vertical clearance within slot', initial=10)
    M = forms.IntegerField(min_value=1, label= 'Pallet positions per slot', initial=2)
    hs = forms.FileField(label = mark_safe("Pallet height of each sku <i class='fa fa-question-circle' aria-hidden='true' title='Upload a csv file with one column and as many rows as skus.'></i>"),
                         widget=forms.FileInput(), required=False)
    hsurl = forms.CharField(widget=forms.HiddenInput())

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

    def clean_hsurl(self):
        urlname = self.cleaned_data.get("hsurl")
        hs = read_array(urlname, 1)
        return hs


