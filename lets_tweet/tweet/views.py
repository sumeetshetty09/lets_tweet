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