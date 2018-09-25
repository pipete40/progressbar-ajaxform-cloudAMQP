
from django.shortcuts import render
import json
from celery.result import AsyncResult
from django.http import HttpResponse
from myapp.forms import SlotProfileDataForm
from myapp.tasks import create_random_user_accounts
import numpy as np

def generate_random_user(request):
    if request.method == 'POST':
        form = SlotProfileDataForm(request.POST)
        if form.is_valid():
            alpha = form.cleaned_data.get('alpha')
            L = form.cleaned_data.get('L')
            b = form.cleaned_data.get('b')
            hs = form.cleaned_data.get('hs')
            invs = form.cleaned_data.get('invs')
            M = form.cleaned_data.get('M')
            total_user = int(np.mean(hs))
            task = create_random_user_accounts.delay(total_user)
            return HttpResponse(json.dumps({'task_id': task.id}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'task_id': None}), content_type='application/json')
    else:
        form = SlotProfileDataForm
    return render(request, 'myapp/index.html', {'form': form})


def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')