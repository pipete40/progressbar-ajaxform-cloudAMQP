from __future__ import absolute_import, unicode_literals
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task, current_task
import time

@shared_task
def create_random_user_accounts(total_user):
    for i in range(total_user):

        """
        username = 'user_%s' % get_random_string(20, string.ascii_letters)
        email = '%s@example.com' % username
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
        """
        time.sleep(0.5)
        current_task.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': total_user,
                                        'percent': int((float(i) / total_user) * 100)})
    return 'done'
