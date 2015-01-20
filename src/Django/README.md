
when the models.py are changed do this:
```
cd src/Django/mysite1
python manage.py makemigrations app1
python manage.py sqlmigrate app1 0001
python manage.py migrate
```
