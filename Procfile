web: gunicorn mycelery.wsgi --timeout 5
worker: celery -A mycelery worker --without-gossip --without-mingle --without-heartbeat -l info


