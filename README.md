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
add {% load static %} at the top of the file
add {% block content %} and {% endblock %} to the file
copy and paste css link from bootstrap cdn in the layout.html file
inject the layout.html file in the index.html file {% extends "layout.html" %}
copy paste navbar code from bootstrap documentation in the layout.html file
add <html lang="en" data-bs-theme="dark"> for dark mode
----------------------------------------------------------------------------------------
now we will work on models.py file
import User from django.contrib.auth.models
#this User is the default user model in django which is AbstractBaseUser coming from admin panel.it is configurable.

create a class Tweet:
class Tweet(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   text = models.TextField(max_length=255)
   photo = models.ImageField(upload_to='photos/', blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self): #it is useful for whenever we integrate this in Admin, it will give us the demo/url from this class which can be used to see fields of the model/class which can be modified.
     return f'{self.user.username} - {self.text[:10]}'
------------------------------------------------------------------------------------------------
#python -m pip install Pillow (for imagefield)

make migrations and migrate
----------------------------------------------------------------------------
register the model in admin.py file

from .models import Tweet
admin.site.register(Tweet)
---------------------------------------------------------------------------
now we will work on forms:
create a new file named forms.py in the apps directory

from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
  class Meta:
    model = Tweet
    fields = ['text', 'photo']
-----------------------------------------------------------------------------
now we will work on views.py file in order perform CRUD operations.
create a new file named views.py in the apps directory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from .models import Tweet
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

def tweet_list(request):
  tweets = Tweet.objects.all().order_by('-created_at')
  return render(request, 'tweet_list.html', {'tweets': tweets})

def tweet_create(request):
  if request.method == 'POST':
    form = TweetForm(request.POST, request.FILES)
    if form.is_valid():
      tweet=form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')
  else:
    form = TweetForm()
  return render(request, 'tweet_form.html', {'form': form})


def tweet_edit(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk=tweet_id,user = request.user)
  if request.method == 'POST':
    form = TweetForm(request.POST, request.FILES, instance=tweet)
    if form.is_valid():
      tweet=form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')
  else:
    form = TweetForm(instance=tweet)
  return render(request, 'tweet_form.html', {'form': form})

def tweet_delete(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk=tweet_id,user = request.user)
  if request.method == 'POST':
    tweet.delete()
    return redirect('tweet_list')
  return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})
------------------------------------------------------------------------------------------

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
]
------------------------------------------------------------------------------------------
now we will work on required templates:
create these templates in templates folder in your app directory
1. tweet_list.html
2. tweet_form.html
3. tweet_confirm_delete.html
4. login.html
5. logout.html
6. register.html
7. base.html
### 1. tweet_list.html
{% extends "layout.html" %}

{% block title %}
lets tweet
{% endblock %}

{% block content %}

<h1 class="text-center mt-4">Welcome to Lets Tweet Django Project</h1>

<a href="{% url 'tweet_create' %}" class="btn btn-primary mb-4">Create New Tweet</a>
<div class="container row gap-3">
  {% for tweet in tweets %}
  <div class="card" style="width: 18rem;">
    <img src="{{tweet.photo.url}}" class="card-img-top" alt="...">
    <div class="card-body">
      <h5 class="card-title">{{tweet.user.username}}</h5>
      <p class="card-text">{{tweet.text}}</p>
      <a href="{% url 'tweet_edit' tweet.id %}" class="btn btn-primary">Edit</a>
      <a href="{% url 'tweet_delete' tweet.id %}" class="btn btn-danger">Delete</a>
    </div>
  </div>
  {% endfor %}
</div>

{% endblock %}
-------------------------------------------------------------------------------------------
### 2. tweet_form.html
{% extends "layout.html" %}

{% block title %}Lets Tweet{% endblock %}
{% block content %}

<h1 class="text-center mt-4">Welcome to Tweet App</h1> 

<h2> 
  {%if form.instance.pk %} 
  Edit Tweet 
  {% else %} 
  Create New Tweet 
  {% endif %}
  <form method="post" enctype="multipart/form-data" class ="form">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-warning" type="submit">Submit</button> 
  </form>
  <a href="{% url 'tweet_list' %}">Back to Home</a>
</h2>

{% endblock %}
---------------------------------------------------------------------------------
### 3. tweet_confirm_delete.html
{% extends "layout.html" %}
{% block title %}Lets Tweet{% endblock %}
{% block content %}
<h1 class="text-center mt-4">Welcome to Tweet App</h1>
<h2>Are you sure you want to delete this tweet?</h2>
<form method="post">
{% csrf_token %}
\begin{itemize}
\item <button type="submit" class="btn btn-danger">Yes, delete it</button
\item <a href="{% url 'tweet_list' %}" class="btn btn-primary">
No, go back
</a>
\end{itemize}
\end{form}
---------------------------------------------------------------------------------
lets work on user registration and login and logout
---------------------------------------------------------------------------------
-----------------------add to forms.py-------------------------------------

from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

-----------------------add to views.py-------------------------------------
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth import login, authenticate, logout

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      return redirect('login') #for automatic login "login(request,user)" or u can redirect to any page like 'tweet_list'
  else:
    form = UserRegistrationForm()
  return render(request, 'registration/register.html', {'form': form})
----------------------------------------------
-----------------------add to urls.py-------------------------------------
urlpatterns = [
    path('register/', views.register, name='register'),
]

but this wont work untill we add the following to settings.py
-----------------------add to settings.py-------------------------------------
LOGIN_URL = '/accounts/login'

LOGIN_REDIRECT_URL = '/tweet/'
LOGOUT_REDIRECT_URL = '/tweet/'

modification also required in main urls.py
-----------------------add to main urls.py-------------------------------------

from django.contrib.auth.urls import views as auth_views

urlpatterns = [
  path('accounts/', include('django.contrib.auth.urls')),
]
-------------------------------------------------------------------------------
now lets work on html files required for registration and login;

registration related html files should be stored in outer directory of project "lets_tweet\templates\registration" because authentication is not a part of app it's handled by the django.
so keep them created:
-----------------------register.html----------------------------------
{% extends 'layout.html' %}
{% block content %} 
<h2>Register Form</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button class="btn btn-primary" type="submit">Register</button>
</form>

{% endblock %}
-----------------------login.html-------------------------------------
{% extends 'layout.html' %}

{% block content %} 
<h2>Login Form</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button class="btn btn-primary" type="submit">Login</button>
</form>

<p>Dont have an account? <a href="{% url 'register' %}">Register here</a></p

{% endblock %}

-----------------------logged_out.html.html---------------------------
{% extends 'layout.html' %}
{% block content %} 
<h2>Logged out</h2>


<p>You have been Logged out! <a href="{% url 'login' %}">Login again</a></p

{% endblock %}
-------------------------------------------------------------------------------
now lets modify layout.html to include home and logout buttons
<form class="d-flex" role="search">
            </form>
            <a class="btn btn-primary mx-2" href="{% url 'tweet_list' %}">Tweet Home</a>
            {% if user.is_authenticated %}
            <form method="post" action="{% url 'logout' %}">
              {% csrf_token %}
              <button class="btn btn-danger" type="submit">Logout</button>

            </form>
            {% else %}
            <a class="btn btn-primary mx-2" href="{% url 'register' %}">Register</a>
            <a class="btn btn-success mx-2" href="{% url 'login' %}">Login</a>
            {% endif %}
          </div>


-------------------------------------------------------------------------------
user- sumeet
password- 12345

user- virat
password- v@123456

user- amit
password- amit@123
-------------------------------------------------------------------------------