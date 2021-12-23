#!/bin/bash
python manage.py flush
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# touch /srv/logs/gunicorn.log 
# touch /srv/logs/access.log
# tail -n 0 -f /srv/logs/*.log &

#Start Gunicorn process
echo Starting Gunicorn
exec gunicorn config.wsgi:application \
    --name chaty \
    --bind 0.0.0.0:8000 \
    # --workers 3 \
    # --log-level=info \
    # --log-file=/srv/logs/gunicorn.log \
    # --access-logfile=/srv/logs/access.log \
    # "$@"