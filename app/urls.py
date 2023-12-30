from django.urls import path
from app import views

urlpatterns = [

    path('', views.LoginPage, name = 'login'),
    path('login/', views.LoginPage, name = 'login'),
    path('register/', views.RegisterPage, name ='register'),
    path('logout/', views.LogoutPage, name = 'logout'),
    
    path('add/', views.add_task, name='add_task'),
    path('<str:current_tab>/', views.HomePage, name='home'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

]
