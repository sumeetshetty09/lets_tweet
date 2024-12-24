# lets_tweet
install virtual environment,
pip install virtualenv

python -m venv env

env\scripts\activate

pip install django

pip freeze > requirements.txt

django-admin startproject lets_tweet

cd lets_tweet

ls (to check for manage.py file presence)

--------------------------------------------------------------------
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
--------------------------------------------------------------------
python manage.py createsuperuser

Username (leave blank to use 'sumeet'): 
Email address: sumeeetsht@gmail.com
Password: 12345
Password (again): 12345
------------------------------------------------------------------
some basic settings we will add in settings.py file:
import os

TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        }

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

-----------------------------------------------------------
Edit projects urls.py file to include static and media files.
------------------------------------------------------------

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
----------------------------------------------------------------------

now we will create an app:

python manage.py startapp tweet

add 'tweet' app to installed apps in settings.py file:
------------------------------------------------
in views.py;
------------------------------------------------
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')
----------------------------------------------------
create file urls.py
----------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
------------------------------------------------------------
now create a template file index.html in templates directory
------------------------------------------------------------
-----------------------------------------------------------
Edit projects urls.py file to include apps urls.py
------------------------------------------------------------

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/', include('tweet.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
-----------------------------------------------------------------------
now we will work on layout.html:
so create a new file in templates directory(project folder) named layout.html