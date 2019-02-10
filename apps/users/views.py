from django.shortcuts import render, redirect

from django.contrib import messages

from .models import *

def index(request):
  return render(request, 'users/index.html')

def create(request):
  if request.method != 'POST':
    return redirect('users:index')
  errors = User.objects.validate(request.POST)
  if errors:
    for error in errors:
      messages.error(request, error)
    return redirect('users:index')
  else:
    user = User.objects.create_user(request.POST)
    request.session['user_id'] = user.id
    return redirect('books:index')

def login(request):
  if request.method != 'POST':
    return redirect('users:home')
  valid,response = User.objects.login(request.POST)
  if valid:
    user_id = response
    request.session['user_id'] = response
    return redirect('books:index')
  else:
    errors = response
    if errors:
      for error in errors:
        messages.error(request,error)
    return redirect('users:index')

def logout(request):
  request.session.clear()
  return redirect('users:index')

def show(request,id):
  user = User.objects.get(id=id)
  context = {
    'user_first_name': user.first_name,
    'user_last_name': user.last_name,
    'user_username': user.username,
    'user_email': user.email,
    'books_reviewed': user.books_reviewed.all
  }
  return render(request,'users/showuser.html',context)