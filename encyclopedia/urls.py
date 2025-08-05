from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("new_encyclopedia_entry", views.creatNewPage, name="creatNewPage"),
    path("random", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_entry"),
]
