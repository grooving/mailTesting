release: sh -c 'python3 manage.py sqlflush | python3 manage.py dbshell && python3 manage.py makemigrations emailTesting && python3 manage.py migrate'
web: sh -c 'gunicorn gmail.wsgi --log-file -'