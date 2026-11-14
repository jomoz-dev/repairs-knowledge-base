from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
]
