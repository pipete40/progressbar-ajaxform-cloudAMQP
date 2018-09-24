web: gunicorn mycelery.wsgi

worker: python manage.py celery -A mycelery worker --without-gossip --without-mingle --without-heartbeat -l info
