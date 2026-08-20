from django.urls import path

from . import views

urlpatterns = [
    path("apply/", views.apply_short_leave, name="apply_short_leave"),
    path("my-leaves/", views.my_leaves, name="my_leaves"),
]