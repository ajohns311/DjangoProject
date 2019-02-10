from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name = "index"),
  url(r'^create_book_review/$', views.create_book_review, name = "create_book_review"),
  url(r'^add/$', views.add, name = "add"),
  url(r'^display/(?P<id>\d+)/$', views.display, name = "display"),
  url(r'^new_author/$', views.new_author, name = "new_author"),
  url(r'^add_review$', views.add_review, name = "add_review")
]