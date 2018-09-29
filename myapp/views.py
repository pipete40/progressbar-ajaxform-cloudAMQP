import json
from django.shortcuts import render
from celery.result import AsyncResult
from django.http import HttpResponse, HttpResponseServerError
from myapp.forms import SlotProfileDataForm
from myapp.tasks import create_random_user_accounts
import numpy as np
import time
import os
import boto3
from botocore.client import Config
from django.conf import settings

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


def sign_s3(request):

    file_name = request.GET.get('filename', None)
    file_type = request.GET.get('filetype', None)

    if (file_name is not None) and (file_type is not None):


        # Load necessary information into the application
        S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME


        # Initialise the S3 client
        s3 = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
        )

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )

        url = 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
        data ={'presigned': presigned_post, 'url': url}

        # Return the data to the client
        return HttpResponse(json.dumps(data), content_type='application/json')

    else:
        return HttpResponse('No job id given.')


