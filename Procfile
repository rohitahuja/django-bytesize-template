web: gunicorn {{ project_name }}.wsgi
worker: celery -A {{ project_name }} worker -B -l info --purge
