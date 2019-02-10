from django.shortcuts import render, redirect

from apps.users.models import *

from .models import *

def index(request):
  user = User.objects.get(id=request.session['user_id'])
  context = {
    'user_id': user.id,
    'user_first_name': user.first_name,
    'user_last_name': user.last_name,
    'user_username': user.username,
    'books': Book.objects.all(),
    'reviews': Review.objects.all().order_by("-created_at")[0:3]
  }
  return render(request, 'books/index.html',context)

def add(request):

  context = {
    'authors': Author.objects.all(),
    'user_id': User.objects.get(id=request.session['user_id']).id
  }
  return render(request, 'books/newbook.html',context)

def new_author(request):
  import datetime
  author = Author.objects.create(
    first_name = request.POST['author_first_name'],
    last_name = request.POST['author_last_name'],
    created_at = datetime.datetime.now(),
    updated_at = datetime.datetime.now()
  )
  return redirect('/books/add')

def create_book_review(request):
  import datetime
  book = Book.objects.create_book(request.POST)
  review = Review.objects.create(
    review = request.POST['review'],
    rating = request.POST['rating'],
    user = User.objects.get(id=request.POST['user_id']),
    book = Book.objects.get(id=book.id),
    created_at = datetime.datetime.now(),
    updated_at = datetime.datetime.now()
  )
  return redirect('/books/display/' + str(book.id))

def display(request,id):
  book = Book.objects.get(id=id)
  context = {
    'book_id': book.id,
    'book_title': book.title,
    'reviews': book.book_reviews.all
  }
  return render(request,'books/bookdisplay.html',context)

def add_review(request):
  import datetime
  user = User.objects.get(id=request.session['user_id'])
  book = Book.objects.get(id=request.POST['book_id'])
  review = Review.objects.create(
    review = request.POST['review'],
    rating = request.POST['rating'],
    user = user,
    book = book,
    created_at = datetime.datetime.now(),
    updated_at = datetime.datetime.now()
  )
  return redirect('/books/display/' + str(book.id))

