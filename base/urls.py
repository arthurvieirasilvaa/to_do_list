from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('task/<str:pk>', views.task, name="task"),
]