import json
from django.shortcuts import render
from celery.result import AsyncResult
from django.http import HttpResponse, HttpResponseServerError
from myapp.forms import SlotProfileDataForm
from myapp.tasks import create_random_user_accounts
import numpy as np
import time


def read_params(request, form):
    alpha = form.cleaned_data['alpha']
    L = form.cleaned_data['L']
    b = form.cleaned_data['b']
    hs = form.cleaned_data['hs']
    M = form.cleaned_data['M']
    return hs, alpha, L, M

def generate_random_user(request):
    if request.method == 'POST':
        form = SlotProfileDataForm(request.POST, request.FILES)
        if form.is_valid():
            hs, alpha, L, M = read_params(request, form)
            task = create_random_user_accounts(11)
            a = np.mean(hs) + np.random.rand()
            return render(request, 'myapp/index.html', {'form': form, 'sub': True, 'txt': a})
    else:
        form = SlotProfileDataForm
    return render(request, 'myapp/index.html', {'form': form})

