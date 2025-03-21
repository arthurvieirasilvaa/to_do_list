from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    
    path('task/<str:pk>', views.task, name="task"),
    
    path('update-task/<str:pk>', views.taskUpdate, name="update-task"),
    path('delete-task/<str:pk>', views.deleteTask, name="delete-task"),
    
    path('profile/<str:pk>', views.profilePage, name="profile"),
]