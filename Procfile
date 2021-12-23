release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: guincorn config.wsgi --log-file -