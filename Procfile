web: gunicorn mycelery.wsgi
worker: python manage.py celery  worker -B --without-gossip --without-mingle --without-heartbeat -l info


