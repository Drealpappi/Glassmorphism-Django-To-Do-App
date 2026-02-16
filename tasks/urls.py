from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_tasks, name='list'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('delete/<str:pk>/', views.delete_task, name='delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]