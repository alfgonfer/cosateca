release: sh -c 'cd cosateca && python manage.py migrate'
web: sh -c 'cd cosateca && gunicorn cosateca.wsgi --log-file -'