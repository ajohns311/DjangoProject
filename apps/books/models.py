from django.db import models

from apps.users.models import *

class BookManager(models.Manager):
  def create_book(self,form):
    import datetime
    author = Author.objects.get(id=form['book_author'])
    user = User.objects.get(id=form['user_id'])
    book = self.create(
      title = form['title'],
      user = user,
      author = author,
      created_at = datetime.datetime.now(),
      updated_at = datetime.datetime.now()
    )
    return book

class Author(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
  title = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name = "books_added")
  author = models.ForeignKey(Author, related_name = "books")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = BookManager()

class Review(models.Model):
  review = models.TextField()
  rating = models.IntegerField()
  user = models.ForeignKey(User, related_name = "books_reviewed")
  book = models.ForeignKey(Book, related_name = "book_reviews")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

