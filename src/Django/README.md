
# MySite 1

This is the django tutorial

when the models.py are changed do this:
```
cd src/Django/mysite1
python manage.py makemigrations app1
python manage.py sqlmigrate app1 0001
python manage.py migrate
```

# MySite 2

My tests!

## To start the site:
```
cd $HOME/git/PythonCode/src/Django
django-admin startproject mysite2
#
cd $HOME/git/PythonCode/src/Django/mysite2
python manage.py migrate
```

## Start an app for a phone directory:

```
python manage.py startapp directory
```

Add the app into:
```
mysite2/settings.py
mysite2/urls.py
```

Add Logging info in: 
```
mysite2/settings.py
```

## Models:
One Person has multiple Phone numbers.

Edit: ```directory/models.py```

```
python manage.py makemigrations directory
python manage.py migrate
```

## Creating an admin user (admin/admin)

```
python manage.py createsuperuser
```

Test it: 

```
python manage.py runserver
```

Browse: [http://localhost:8000/admin/](http://localhost:8000/admin/)


## Create Views and URLs:

```
directory/urls.py
directory/views.py
```

## Create Templates:

```
directory/templates/phone_list.html
directory/templates/person_list.html
```

```
python manage.py runserver
```

Test:
http://localhost:8000/directory/person/
http://localhost:8000/directory/phone/