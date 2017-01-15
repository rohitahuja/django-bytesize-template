web: gunicorn {{ project_name }}.wsgi
worker: celery -A sample_bot worker -l info --without-gossip --without-mingle --without-heartbeat
